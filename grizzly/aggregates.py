from enum import Enum
class AggregateType(Enum):
  MIN = 1
  MAX = 2
  MEAN = 3
  COUNT = 4
  SUM = 5

  @staticmethod
  def getName(v):
    if v == AggregateType.MIN:
      return "min"
    elif v == AggregateType.MAX:
      return "max"
    elif v == AggregateType.MEAN:
      return "mean"
    elif v == AggregateType.COUNT:
      return "count"
    elif v == AggregateType.SUM:
      return "sum"
    else:
      raise ValueError(f"Unknown aggregate type: {v}")