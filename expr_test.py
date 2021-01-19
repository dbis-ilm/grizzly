from grizzly.expression import And, ColRef, Eq, Gt, Le, Ne, Or
import unittest
import grizzly

class ExpressionTest(unittest.TestCase):

  def test_parantheses(self):
    df = grizzly.read_table("t1")
    expr = (df['a'] == df['b']) & ((df['c'] <= df['d']) | ((df.f > 3) & (df.e != None)))

    self.assertIsInstance(expr, And, "top expression should be AND")
    self.assertIsInstance(expr.left, Eq, "first left should be EQ")
    self.assertIsInstance(expr.right, Or, "first right should be OR")

    andL = expr.left
    self.assertIsInstance(andL.left, ColRef, "left of EQ should be a ColRef")
    self.assertEqual(andL.left.column, "a", "left of EQ colref should be column a")

    self.assertIsInstance(andL.right, ColRef, "right of EQ should be a ColRef")
    self.assertEqual(andL.right.column, "b", "right of EQ colref should be column b")

    andR = expr.right
    self.assertIsInstance(andR.left, Le, "left of OR should be a LE")
    self.assertIsInstance(andR.right, And, "right of OR should be another AND")

    self.assertIsInstance(andR.left.left, ColRef, "left of LE should be a ColRef")
    self.assertIsInstance(andR.left.right, ColRef, "right of LE should be a ColRef")
    self.assertEqual(andR.left.left.column, "c")
    self.assertEqual(andR.left.right.column, "d")

    innerAnd = expr.right.right
    self.assertIsInstance(innerAnd.left, Gt)
    self.assertIsInstance(innerAnd.left.left, ColRef)
    self.assertEqual(innerAnd.left.left.column, "f")
    self.assertIsInstance(innerAnd.left.right, int)
    self.assertEqual(innerAnd.left.right, 3)

    self.assertIsInstance(innerAnd.right, Ne)
    self.assertIsInstance(innerAnd.right.left, ColRef)
    self.assertEqual(innerAnd.right.left.column, "e")
    self.assertIsNone(innerAnd.right.right)

    

