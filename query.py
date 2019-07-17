class Query(object):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.Filters = []
    self.ProjList = []
    self.From = []
  
  def sql(self):
    projs = ""
    if not self.ProjList:
      projs = "*"
    else:
      projs = ','.join(self.ProjList)

    froms = ",".join(self.From)

    filters = ""
    if self.Filters:
      filters = " WHERE " +  " AND ".join([str(f) for f in self.Filters])


    return f"SELECT {projs} FROM {froms} {filters}"
  