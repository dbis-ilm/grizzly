class RelationalExecutor(object):
  def __init__(self, connection):
    super().__init__()
    self.connection = connection

  def execute(self, sql):
    cursor = self.connection.cursor()
    cursor.execute(sql)
    return cursor

  def close(self):
    self.connection.close()

    