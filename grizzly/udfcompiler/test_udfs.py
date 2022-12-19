import math
import grizzly
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException

class Test_funcs:
    # Test functions for testing the translation of the compiler

    def repeat(a: int, b: str) -> str:
        #print(a)
        return a * b

    def if_expr(a: int, b: str) -> str:
        if a % 2 ==0:
            return 'Faktor 2'
        elif a < len(b):
            return 'A < b'
        else:
            return 'a%2=' + (a%2)

    def for_loop(a: int) -> int:
        m = 0
        for i in range(m, a):
            m = m+i
        return m

    def for_if(a: int, b:float) -> int:
        m= a + 2
        for i in range(m):
            if i > b:
                return 20 * a
            elif a <= 2:
                return 0
        return m

    def bool(a: int) -> str:
        if a+5/2 > 10:
            f = True
        else:
            f = False
        if f == True:
            return 'True'
        return 'hi'

    def lists(a: int) -> str:
        int_lst = [3, 5, a]
        str_lst = ["first", "second"]
        bool_list = [True, False]
        float_lst = [1.2, 4.6]
        str_lst[0] = 'changed'
        m = int_lst[1]
        b = bool_list[0]
        for i in int_lst:
            m = m + i 
        return str_lst[0] + str(m) + str(b)

    def while_loop(a: int, b: float) -> int:
        i = 0
        while i+b < a:
            i = i + a
        return i

    def while_True(a: int, b: float) -> int:
        i = 0
        while True:
            i = i * a+1
            if i > a+b or a == 0:
                break
        return i

    def exceptions(a: int) -> int:
        try:
            if a == 3:
                raise UDFCompilerException
            elif a == 4:
                raise
            return 19.0 / a
        except ZeroDivisionError:
            return 0
        except UDFCompilerException:
            return 99
        except:
            return 1

    def typecast(a:int) -> str:
        i = "34"
        t = True
        f = 'False'
        k = int(i)
        l = str(a)
        # Works not for oracle:
        #p = str(t)
        #v = bool(f)
        return l

    def funccalls(a: int) -> float:
        f: int = while_loop(5, 2.3)
        b: float = math.sqrt(a)
        return b + f

    def grizzly_cursor_loop(a: int, b:float) -> str:
        f = 0
        g_df1 = grizzly.read_table("speedtest")
        g_df1 = g_df1[g_df1.test_id < 10] 
        g_df1 = g_df1[["test_float", "test_number", "test_id"]]

        for tuple in g_df1:
            if tuple.test_float > tuple.test_number:
                continue
            elif tuple.test_id > a:
                break
            if tuple.test_number > 20:
                f = f + tuple.test_number
        return f

    def embedded_loops(a: int) -> int:
        f = 0
        # Comment
        for i in range(a):
            for j in range(0,10):
                f = f + i - j / (i + 1)
        return f
    
    def unspported_list_compr(a: int) -> str:
        k = [str(x) for x in range(10)]
        return k

    def unspported_exceptions(a: int) -> str:
        try:
            m = 2 / a
        except:
            return 'Error'
        else:
            return 'No Error'
        finally:
            return a

all_funcs_two_param = [Test_funcs.grizzly_cursor_loop, Test_funcs.while_loop, Test_funcs.while_True, Test_funcs.for_if]
all_funcs_two_param_str = [Test_funcs.repeat, Test_funcs.if_expr]
all_funcs_one_param = [Test_funcs.embedded_loops, Test_funcs.funccalls, Test_funcs.typecast, Test_funcs.exceptions, Test_funcs.lists, Test_funcs.bool, Test_funcs.for_loop]
not_supported_funcs = [Test_funcs.unspported_list_compr, Test_funcs.unspported_exceptions]