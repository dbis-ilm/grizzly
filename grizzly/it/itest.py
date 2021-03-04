import importlib
import sys
from typing import Dict
import docker
from docker.client import DockerClient
import logging
import yaml

import logging.config

with open('grizzly/it/logger.yml','rt') as f:
  config=yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger=logging.getLogger("test")

class TestFailedException(Exception):
  def __init__(self, *args: object) -> None:
      super().__init__(*args)

def startDockerContainer(dbName:str, settings, dockerClient: DockerClient):

  img = settings["image"]
  port = settings["port"]
  portsDict = {f"{port}/tcp": ('127.0.0.1',port)}
  env = settings.get("environment",{})

  logger.info(f"starting Docker container for {img}: Port: {portsDict}, env: {env}")

  container = dockerClient.containers.run(img, auto_remove = True, detach = True, ports = portsDict, name=f"grizzly_ittest_{dbName}",environment=env)
  
  return container
  
def connectDB(dbName: str,settings: Dict):

  # module = __import__(dbName) 
  import importlib
  module = importlib.import_module(f"grizzly.it.{dbName}")
  dbUser = settings["user"]
  dbPass = settings["password"]
  dbPort = settings["port"]
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

  for i in range (2,len(sys.argv)):
    dbName = sys.argv[i]
    settings = loadTestConfig(dbName)
    logger.debug(f"db config has {len(settings)} entries")
    
    container = None
    if startContainer:
      client = docker.from_env()
      container = startDockerContainer(dbName,settings, client)
      logger.debug(f"created container: {container}")

    try:
      (dbCon,alchemyCon) = connectDB(dbName, settings)
      logger.debug(f"connected: {dbCon}")

      logger.info("start running tests")

      # I don't know, but I cannot write "import testrunner" 
      # but this works...
      # runner = importlib.import_module("grizzly.it.testrunner")
      import grizzly.it.testrunner as runner
      failedTests = runner.run(dbName, dbCon, alchemyCon)
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
    raise TestFailedException(f"Tests failed for {fails}")