class GrizzlyGenerator(object):
  """
  A wraper for the actually used generator
  """

  generator = None

  @staticmethod
  def generate(df):
    """
    Call the underlying code generator and produce the query text
    """
    return GrizzlyGenerator.generator.generate(df)

  @staticmethod
  def execute(df, delim, pretty, maxColWidth):
    """
    Call the underlying generator and execute the query
    """
    GrizzlyGenerator.generator.execute(df,delim,pretty,maxColWidth)

  @staticmethod
  def toString(df):
    return GrizzlyGenerator.generator.toString(df)

  @staticmethod
  def close():
    """
    Tell the underlying generator to close its connection to
    the data store
    """
    GrizzlyGenerator.generator.close()

    
  @staticmethod
  def aggregate(df, func, col):
    return GrizzlyGenerator.generator._execAgg(df, func, col)