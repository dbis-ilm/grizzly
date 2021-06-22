import sys
from typing import Dict

import logging
import yaml

import logging.config

with open('grizzly/it/logger.yml','rt') as f:
  config=yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger=logging.getLogger("test")

# class TestFailedException(Exception):
#   def __init__(self, *args: object) -> None:
#       super().__init__(*args)

def startDockerContainer(dbName:str, settings, dockerClient):

  img = settings["image"]
  port = settings["port"]
  if isinstance(port,list):
    portsDict = {}
    for p in port:
      portsDict[f"{p}/tcp"] = ('127.0.0.1',p)
  else:
    portsDict = {f"{port}/tcp": ('127.0.0.1',port)}

  env = settings.get("environment",{})

  logger.info(f"starting Docker container for {img}: Port: {portsDict}, env: {env}")

  containerName = f"grizzly_ittest_{dbName}"

  isNewContainer = True

  existingContainers = dockerClient.containers.list(filters={"name":containerName, "status":"exited"})
  if len(existingContainers) >= 1:

    logger.debug(f"found existing containers: {existingContainers}")

    container = existingContainers[0]
    isNewContainer = False

    if len(existingContainers) > 1:
      logger.warning(f"there seem to be multiple containers with name {containerName}, we'll use the first one")

    logger.debug(f"found existing container: {container}")
    if container.status != "running":
      logger.debug(f"existing container is not running, trying to start it")
      container.start()

  else:
    logger.debug("no existing container found, creating a new one")
    container = dockerClient.containers.run(img, auto_remove = False, detach = True, ports = portsDict, name=containerName,environment=env)

    try:
      if "container_setup" in settings:
        commands = settings["container_setup"]
        logger.info(f"run container setup commands: {commands}")

        # loop over setup commands 
        for cmd in commands:
          logger.debug(f"Executing inside container: '{cmd}'")
          (ret, stream) = container.exec_run(cmd, user="root")
          if ret != 0:
            logger.debug(f"Command failed? Return code is {ret}")
            logger.debug(f"\tOutput: {stream}")
    except Exception as e:
      logger.error(f"failed to run container setup: {str(e)}")
      if container is not None:
        dockerClient.containers.stop(container)
        dockerClient.containers.remove(container)
  
  return (container, isNewContainer)
  
def connectDB(dbName: str,settings: Dict):

  # module = __import__(dbName) 
  import importlib
  module = importlib.import_module(f"grizzly.it.{dbName}")
  dbUser = settings["user"]
  dbPass = settings["password"]
  dbPort = settings["port"]
  if isinstance(dbPort, list):
    dbPort = dbPort[0]
    
  dbDB = settings["db"]

  logger.info(f"connect to DB with {dbUser}:{dbPass} @ {dbDB} on port {dbPort}")

  connection = module.connect(dbUser, dbPass, dbDB, dbPort)
  
  return connection

def loadTestConfig(dbName):
  
  configs = None
  with open("grizzly/it/itconfig.yml","r") as configFile:
    configs = yaml.load(configFile, Loader=yaml.FullLoader)
    logger.debug(f"loadded config file with {len(configs)} entries total")
    dbConf = configs[dbName]
    
    return dbConf

if __name__ == "__main__":

  logger.info("starting test setup")
  if len(sys.argv) < 3:
    print(f"Please provide flag to indicate container start [docker] and the DB names! Got: {sys.argv}")
    exit(1)

  startContainer = sys.argv[1].strip().lower() != "nodocker"

  summary = {}

  from grizzly.it.testrunner import TestRunner
  runner = TestRunner()

  for i in range (2,len(sys.argv)):
    dbName = sys.argv[i]
    settings = loadTestConfig(dbName)
    logger.debug(f"db config has {len(settings)} entries")
    
    container = None
    needsSetup = startContainer
    if startContainer:

      import docker

      client = docker.from_env()
      (container,needsSetup) = startDockerContainer(dbName,settings, client)
      logger.debug(f"created container: {container}")

    try:
      (dbCon,alchemyCon) = connectDB(dbName, settings)
      logger.debug(f"connected: {dbCon}")

      logger.info("start running tests")

      failedTests = runner.run(dbName, dbCon, alchemyCon, needsSetup = needsSetup)
      logger.info("finished running tests")

      summary[dbName] = failedTests

    finally:
      if container is not None:
        logger.debug("cleaning up")
        container.stop()
        logger.info(f"stopped container {container}")

  fails = []
  for (db, failedTests) in summary.items():
    if len(failedTests) > 0:
      for (testName, gResult, pResult) in failedTests:
        logger.error(f"FAILED: [{db}] -- {testName}: Grizzly: {gResult} vs. Pandas: {pResult}")
      
      fails.append(db)

  if len(fails) > 0:
    logger.fatal(f"Tests failed for {fails}")
    sys.exit(1)
    # raise TestFailedException(f"Tests failed for {fails}")