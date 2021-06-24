from pathlib import Path
import os

import logging
logger = logging.getLogger(__name__)

class Config:

  @staticmethod
  def loadProfile(profile):
    logger.debug("loading configs for profile %s",profile)
    if not profile:
      return Config(profile, dict())

    configDir = Path.home().joinpath(".config","grizzly")
    locations = [Path.cwd(), configDir]

    confFileName = "grizzly.yml"

    path = None
    for loc in locations:
      p = loc.joinpath(confFileName)
      if p.exists():
        path = p
        logger.debug(f"found config file in: {str(path)}")
        break

    if not path: # as not found in expected locations
      logger.debug(f"Cannot find config file {confFileName} in {[str(l) for l in locations]} - creating default in {str(configDir)}...")
      # load packaged ressource
      import pkg_resources 
      my_data = pkg_resources.resource_string(__name__, "grizzly.yml").decode("utf-8") 
      
      filename = configDir.joinpath(confFileName)
      os.makedirs(os.path.dirname(filename), exist_ok=True) # create config directory
      with open(filename,'w') as target:
        target.writelines(my_data) # copy 

      logger.debug("done")
      path = filename # use below


    import yaml
    configs = None
    with open(path,"r") as configFile:
      configs = yaml.load(configFile, Loader=yaml.FullLoader)

    return Config(profile, configs[profile])


  def __init__(self, profile, config):
    self.profile = profile
    self.config = config

  def __contains__(self, key: str):
    return key in self.config

  def __getitem__(self, key: str):
    if key in self.config:
      return self.config[key]
    else:
      raise ValueError(f"Unsupported configuration key {key} in profile {self.profile}")