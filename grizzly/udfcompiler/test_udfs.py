import math
import grizzly
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException

# Test functions for testing the translation of the compiler

def udf_bool(a: int) -> str:
    if a+5/2 > 10:
        f = True
    else:
        f = False
    if f == True:
        return 'True'
    return 'hi'

def udf_exceptions(a: int) -> str:
    try:
        m = str(a)
        if a / 30 > 3:
            raise
        return 'success'
    except:
        return 'general exception'

def repeat(a: int, b: str) -> str:
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
    for i in range(a):
        m = m+i
    return m

def udf_forif(a: int, b:float) -> int:
    m= a + 2
    for i in range(m):
        if i > b:
            return 20 * a
        elif a <= 2:
            return 0
    return m

def lists(a: int) -> str:
    int_lst = [3, 5 ,10]
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

def typecast(a: int) -> str:
    m = '23'
    f = int(m)
    return str(a)

def exceptions(a: int) -> float:
    try:
        if a == 3:
            raise UDFCompilerException
        return 19.0 / a
    except ZeroDivisionError:
        return 0
    except UDFCompilerException:
        return 99
    except:
        return 1

def castings(a:int) -> str:
    i: int = 0
    l: int
    t = True
    f = 'False'

    k = str(i)
    p = str(f)
    v = bool(f)
    return p

def funccalls(a: int) -> float:
    f: int = while_loop(5, 2.3)
    a = math.sqrt(a)
    return a + f

def udf_grizzly(a: int, b:float) -> str:
    f = 0
    g_df1 = grizzly.read_table("speedtest")
    g_df1 = g_df1[g_df1.test_float == 40] 
    g_df1 = g_df1[["test_float", "test_number", "test_id"]]

    for tuple in g_df1:
        if tuple.test_float > tuple.test_number:
            continue
        elif tuple.test_id > a:
            break
        if tuple.test_number > 20:
            f = f + tuple.test_number
    return f


def udf_embedded_loops(a: int) -> str:
    f = 0
    # Kommentar
    g_df1 = grizzly.read_table("speedtest")
    g_df1 = g_df1[g_df1.test_id == 5] 

    for row in g_df1:
        for i in range(a):
            if row.test_id >= a -2:
                if row.test_id <= a +2:
                    if row.test_number > 40:
                        f = f + row.test_number
    return f