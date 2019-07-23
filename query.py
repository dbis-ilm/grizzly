import random
import string

class Query(object):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.filters = []
    self.projList = []
    self.froms = ""
    self.groupcols = []
    self.groupagg = None
    self.joins = []
  
  def sql(self):
    projs = ""
    if not self.projList:
      projs = "*"
    else:
      projs = ','.join(self.projList)

    filters = ""
    if self.filters:
      filters = " WHERE " +  " AND ".join([str(f) for f in self.filters])

    groups = ""
    if self.groupcols:
      colStr = ", ".join(self.groupcols)
      groups = " GROUP BY " + colStr

      if projs == "*":
        projs = colStr

      if self.groupagg:
        projs += f", {self.groupagg}"


    joins = ""
    if self.joins:
      tupleVars = self.generateTupleVar(len(self.joins))
      joinsNames = zip(self.joins, tupleVars)

      leftName = self.froms
      for j,rightName in joinsNames:
        joins += " "+j.sql(leftName, rightName)
        leftName = rightName


    return f"SELECT {projs} FROM {self.froms} {joins} {filters} {groups}"
  

  def generateTupleVar(self,nums, length = 5):
    ids = set()
    while len(ids) < nums:
      ids.add(''.join(random.choices(string.ascii_uppercase, k=length)))  
    
    return ids
    