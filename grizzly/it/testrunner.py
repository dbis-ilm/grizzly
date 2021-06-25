import logging
from pathlib import Path

from numpy import string_
import grizzly
from grizzly.dataframes.frame import DataFrame as GrizzlyDataFrame
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

import pandas as pd

import importlib

import unittest

logger = logging.getLogger("test")



class TestRunner(unittest.TestCase):

  def __init__(self):
    self.pandasResults = {}
  
  def run(self, dbName: str, con, alchemyCon):

    logger.debug("init Grizzly")
    gen = SQLGenerator(dbName)
    executor = RelationalExecutor(con, gen)
    grizzly.use(executor)


    logger.debug("now run tests")

    failedTests = []

    scriptsDir = "grizzly/it/resources/scripts"

    from os import walk
    _, _, scripts = next(walk(scriptsDir))

    grizzlyScripts = [s for s in scripts if s.startswith("grizzly_")]
    pandasScripts = [s for s in scripts if s.startswith("pandas_")]

    scripts = [ (g,p) for g in grizzlyScripts for p in pandasScripts if g[len("grizzly_"):].lower() == p[len("pandas_"):].lower()]

    for (gScript, pScript) in scripts:
      name = gScript[len("grizzly_"):].lower()

      try:
        if not pScript in self.pandasResults:
          logger.debug(f"did NOT find Pandas result in cache, compute it")
          pandasResult = TestRunner.execute(scriptsDir, pScript, con, alchemyCon)
          self.pandasResults[pScript] = pandasResult
        else:
          pandasResult = self.pandasResults[pScript]
          logger.debug(f"found Pandas result in cache: {pandasResult}")
      except Exception as e:
        logger.info(f"Pandas execution failed with {str(e)}")
        pandasResult = e

      try:
        grizzlyResult = TestRunner.execute(scriptsDir,gScript,con, alchemyCon)
        if isinstance(grizzlyResult, GrizzlyDataFrame):
          grizzlyResult = grizzlyResult.collect()
      except Exception as e:
        logger.info(f"Grizzly execution failed with {str(e)}")
        grizzlyResult = e


      if (isinstance(pandasResult, Exception) or isinstance(grizzlyResult, Exception)) or not self.compare(grizzlyResult, pandasResult):
        # logger.error(f"{gScript} vs. {pScript} : {grizzlyResult} vs {pandasResult}")
        failedTests.append((name, grizzlyResult, pandasResult))
      


    resultStr = "Passed" if len(failedTests) == 0 else "Failed"
    logger.info(f"finished tests [{len(scripts)}]: {resultStr}")
    return failedTests

  @staticmethod
  def execute(scriptDir, file,con, alchemyCon):
    p = Path.cwd().joinpath(scriptDir,file)
    logger.debug(f"executing file: {p}")

    s = scriptDir.replace("/",".")
    f = file[:file.index(".")]
    logger.debug(f"loading module {f} in {s}")

    mod = importlib.import_module(f"{s}.{f}")
    retVal = mod.run(con, alchemyCon)

    logger.debug(f"result is {retVal}")
    return retVal

  def compare(self, grizzlyResult, pandasResult) -> bool:
    logger.debug(f"Pandas result is of type {type(pandasResult)}")
    logger.debug(f"Grizzly result is of type {type(grizzlyResult)}")
    if isinstance(pandasResult,float):
      try:
        self.assertAlmostEqual(grizzlyResult, pandasResult,5)
        return True
      except Exception as e:
        logger.debug(f"failed to match float results: {e}")
        return False
    elif isinstance(pandasResult, pd.DataFrame) or isinstance(pandasResult, pd.Series):
      try:
        pList = pandasResult.values.tolist()
        
        self.assertListEqual(pList, grizzlyResult)
        return True
      except Exception as e:
        logger.debug(f"failed to match DF results results: {e}")
        return False
    else:
      return grizzlyResult == pandasResult
