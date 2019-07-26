import random
import string

class Query(object):
  def __init__(self, *args, **kwargs):
    """
    Construct a new empty query
    """
    super().__init__(*args, **kwargs)
    self.filters = []
    self.projList = []
    self.froms = ""
    self.groupcols = []
    self.groupagg = None
    self.joins = []
    self.distinct = ""
  
  def sql(self):
    """
    Produce a SQL string for this query
    """

    # if no explicit projection, we want to do SELECT *
    projs = ""
    if not self.projList:
      projs = "*"
    else:
      projs = ','.join(self.projList)


    # if we have multiple filters, we combine them by AND
    filters = ""
    if self.filters:
      filters = " WHERE " +  " AND ".join([str(f) for f in self.filters])

    # we can group on several columns but need to make sure to
    # adjust the projection if it was * and also add aggregation
    # functions to the result
    groups = ""
    if self.groupcols:
      colStr = ", ".join(self.groupcols)
      groups = " GROUP BY " + colStr

      if projs == "*":
        projs = colStr

      if self.groupagg:
        projs += f", {self.groupagg}"

    # joins are performed using explicit INNER/OUTER ... ON operations
    joins = ""
    if self.joins:
      # give every sub-query a tuplevar (short name)
      tupleVars = self.generateTupleVar(len(self.joins))
      joinsNames = zip(self.joins, tupleVars)

      leftName = self.froms
      for j,rightName in joinsNames:
        # the Join operator will produce the SQL string for itself
        joins += " "+j.sql(leftName, rightName)
        leftName = rightName


    # we always have SELECT ... FROM. Everything else is optional
    return f"SELECT {self.distinct} {projs} FROM {self.froms} {joins} {filters} {groups}"
  

  # create random but unique strings to be used as tuple vars.
  def generateTupleVar(self,nums, length = 5):
    ids = set()
    while len(ids) < nums:
      ids.add(''.join(random.choices(string.ascii_uppercase, k=length)))  
    
    return ids
    