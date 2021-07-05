import os
import sys
from typing import Dict

import logging
import yaml

import time

import logging.config

with open('grizzly/it/logger.yml','rt') as f:
  config=yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger=logging.getLogger("test")

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

  existingContainers = dockerClient.containers.list(all=True, filters={"name":containerName}) #, "status":"exited"

  wasRunning = False

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
      logger.debug(f"existing container is already running...")
      wasRunning = True

    time.sleep(3)    

  else:
    logger.debug("no existing container found, creating a new one")
    container = dockerClient.containers.run(img, auto_remove = False, detach = True, ports = portsDict, \
      name=containerName,environment=env, volumes= {f'{os.getcwd()}/grizzly/it/resources':{'bind':"/resources", "mode":"ro"}})

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

      #set up directories for test resources
      

    except Exception as e:
      logger.error(f"failed to run container setup: {str(e)}")
      if container is not None:
        dockerClient.containers.stop(container)
        dockerClient.containers.remove(container)
  
  return (container, isNewContainer,wasRunning)
  
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

def setupDB(con):
  logger.debug("init DB")
  files = [\
            "grizzly/it/resources/tables.sql",\
            "grizzly/it/resources/tpch-scripts/create_tables.sql",\
            "grizzly/it/resources/tpch/customer.sql",\
            "grizzly/it/resources/tpch/lineitem.sql",\
            "grizzly/it/resources/tpch/nation.sql",\
            "grizzly/it/resources/tpch/orders.sql",\
            "grizzly/it/resources/tpch/part.sql",\
            "grizzly/it/resources/tpch/partsupp.sql",\
            "grizzly/it/resources/tpch/region.sql",\
            "grizzly/it/resources/tpch/supplier.sql",\
            "grizzly/it/resources/tpch-scripts/create_pk.sql",\
            "grizzly/it/resources/tpch-scripts/create_fk.sql"]
  
  
  cnt = 0
  for file in files:
    logger.debug(f"processing {file}")

    lines = []
    with open(file, "rt") as f:
      for line in f:
        if len(line.strip()) > 1 and (not line.startswith("--")):
          lines.append(line)

    

    lines = "".join(lines)
    stmts = lines.split(";")
    stmts = list(filter(lambda x: len(x.strip()) > 1, stmts))
    # logger.debug(f"setup script has {len(stmts)} entries")
    

    cursor = con.cursor()
    for stmt in stmts:
      # logger.debug(stmt)
      cursor.execute(stmt)
      cnt += 1

  con.commit()

  logger.debug("now loading data into tables")



  logger.info(f"finished DB setup: {cnt}")

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
    wasRunning = False

    print(f"[{dbName}] ",end='')
    if startContainer:

      import docker

      client = docker.from_env()
      (container,needsSetup,wasRunning) = startDockerContainer(dbName,settings, client)
      logger.debug(f"created container: {container}")

    try:
      (dbCon,alchemyCon) = connectDB(dbName, settings)
      logger.debug(f"connected: {dbCon}")

      logger.info("start running tests")


      if needsSetup:
        setupDB(dbCon)
      
      start = time.time()

      failedTests = runner.run(dbName, dbCon, alchemyCon)

      end = time.time()

      if failedTests:
        print(" \U0001F92C",end='')
      else:
        print(" \U0001F43B", end='')

      print(f"\t{(end - start):.5f} secs")  
      logger.info("finished running tests")


      summary[dbName] = failedTests

    finally:
      if container is not None and not wasRunning:
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