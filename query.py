class Query(object):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.filters = []
    self.projList = []
    self.froms = []
    self.groupcols = []
    self.groupagg = None
  
  def sql(self):
    projs = ""
    if not self.projList:
      projs = "*"
    else:
      projs = ','.join(self.projList)

    froms = ",".join(self.froms)

    filters = ""
    if self.filters:
      filters = " WHERE " +  " AND ".join([str(f) for f in self.Filters])

    groups = ""
    if self.groupcols:
      colStr = ", ".join(self.groupcols)
      groups = " GROUP BY " + colStr

      if projs == "*":
        projs = colStr

      if self.groupagg:
        projs += f", {self.groupagg}"

    return f"SELECT {projs} FROM {froms} {filters} {groups}"
  