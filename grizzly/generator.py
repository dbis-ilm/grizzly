class GrizzlyGenerator(object):
  """
  A wraper for the actually used generator
  """

  _backend = None
  tVarCounter = 0

  @staticmethod
  def _incrAndGetTupleVar():
    tVar = f"_t{GrizzlyGenerator.tVarCounter}"
    GrizzlyGenerator.tVarCounter += 1
    return tVar

  @staticmethod
  def generate(df):
    """
    Call the underlying code generator and produce the query text
    """
    return GrizzlyGenerator._backend.generate(df)

  @staticmethod
  def collect(df, includeHeader):
    return GrizzlyGenerator._backend.collect(df, includeHeader)


  @staticmethod
  def toString(df, delim=",", pretty=False, maxColWidth=20, limit=20):
    """
    Call the underlying generator, execute the query and return string representation
    """
    return GrizzlyGenerator._backend.toString(df,delim,pretty,maxColWidth,limit)

  @staticmethod
  def table(df):
    """
    Call the underlying generator, execute the query and return string representation
    as a beautiful table...
    """
    return GrizzlyGenerator._backend.table(df)

  @staticmethod
  def close():
    """
    Tell the underlying generator to close its connection to
    the data store
    """
    GrizzlyGenerator._backend.close()

    
  @staticmethod
  def aggregate(df, col, func):
    return GrizzlyGenerator._backend._execAgg(df, col, func)

  @staticmethod
  def _gen_aggregate(df, col, func):
    return GrizzlyGenerator._backend._gen_agg(df, col, func)
