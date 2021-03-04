import logging
from pathlib import Path
import grizzly
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

import importlib

logger = logging.getLogger("test")

def initTables(con):
  logger.debug("init DB")
  lines = []
  with open("grizzly/it/resources/tables.sql", "rt") as f:
    for line in f:
      lines.append(line)

  lines = "\n".join(lines)
  stmts = lines.split(";")
  stmts = list(filter(lambda x: len(x) > 1, stmts))
  logger.debug(f"setup script has {len(stmts)} entries")
  cnt = 0
  marker = len(stmts) // 10

  cursor = con.cursor()
  for stmt in stmts:
    # logger.debug(f"execute setup statement: {stmt}")
    
    cursor.execute(stmt)
    cnt += 1

    if cnt % marker == 0:
      p = cnt / marker
      logger.debug(f"setting up tables... {p*10}%")

  con.commit()
  logger.info(f"finished DB setup: {cnt}")

pandasResults = {}

def run(dbName: str, con, alchemyCon):

  initTables(con)

  logger.debug("init Grizzly")
  gen = SQLGenerator(dbName)
  executor = RelationalExecutor(con, gen)
  grizzly.use(executor)


  logger.info("now run tests")
  
  failedTests = []

  scriptsDir = "grizzly/it/resources/scripts"

  from os import walk
  _, _, scripts = next(walk(scriptsDir))

  grizzlyScripts = [s for s in scripts if s.startswith("grizzly_")]
  pandasScripts = [s for s in scripts if s.startswith("pandas_")]

  scripts = [ (g,p) for g in grizzlyScripts for p in pandasScripts if g[len("grizzly_"):].lower() == p[len("pandas_"):].lower()]

  for (gScript, pScript) in scripts:
    if not pScript in pandasResults:
      logger.debug(f"did NOT found Pandas result in cache, compute it")
      pandasResult = execute(scriptsDir, pScript, con, alchemyCon)
      pandasResults[pScript] = pandasResult
    else:
      pandasResult = pandasResults[pScript]
      logger.debug(f"found Pandas result in cache: {pandasResult}")

    grizzlyResult = execute(scriptsDir,gScript,con, alchemyCon)

    if not compare(grizzlyResult, pandasResult):
      logger.error(f"{gScript} vs. {pScript} : {grizzlyResult} vs {pandasResult}")

      name = gScript[len("grizzly_"):].lower()

      failedTests.append((name, grizzlyResult, pandasResult))


  resultStr = "Passed" if len(failedTests) == 0 else "Failed"
  logger.info(f"finished tests [{len(scripts)}]: {resultStr}")
  return failedTests

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

def compare(grizzlyResult, pandasResult) -> bool:
  return grizzlyResult == pandasResult