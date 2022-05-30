# File contains classes of different complex udf types, with the times of executed performance tests

class udf_basic:
    # Function to display simple mathematical operations in UDF
    def udf_basic(a: int, b: float) -> float:
        m = a / b
        g = a * b
        l = a + b
        f = a - b
        return l

    udf_basic_sql = """
        CCREATE OR REPLACE FUNCTION udf_basic_sql(a int4, b float8) 
            RETURNS int4
        AS $$
            SELECT "return4".*
            FROM (LATERAL (SELECT ("a") / "b" AS "m_1") AS "let0"("m_1")
                LEFT OUTER JOIN
                (LATERAL (SELECT ("a") * "b" AS "g_1") AS "let1"("g_1")
                LEFT OUTER JOIN
                (LATERAL (SELECT ("a") + "b" AS "l_1") AS "let2"("l_1")
                    LEFT OUTER JOIN
                    (LATERAL (SELECT ("a") - "b" AS "f_1") AS "let3"("f_1")
                    LEFT OUTER JOIN
                    LATERAL (SELECT "f_1" AS "result") AS "return4"
                    ON True)
                    ON True)
                ON True)
                ON True)
        $$ LANGUAGE SQL;
    """
    udf_basic_pgplsql = """
        CREATE OR REPLACE FUNCTION udf_basic_pgplsql(a INTEGER,b FLOAT8) 
            RETURNS FLOAT8 
        AS $$ 
        DECLARE 
            m INTEGER;
            g INTEGER;
            l INTEGER;
            f INTEGER;
        BEGIN
            m := a / b;
            g := a * b;
            l := a + b;
            f := a - b;
            RETURN l;
        END; $$ LANGUAGE plpgsql;
    """

    udf_basic_pl_py="""
        CREATE OR REPLACE FUNCTION udf_basic_plpy(a INTEGER,b FLOAT8) 
            RETURNS FLOAT8 
        AS $$ 
            m = a / b
            g = a * b
            l = a + b
            f = a - b
            return l
        $$ LANGUAGE plpython3u;
    """

    udf_basic_pl_sql = """
        CREATE OR REPLACE FUNCTION udf_basic_plsql(a INTEGER,b FLOAT) 
            RETURN FLOAT 
        IS 
            m INTEGER;
            g INTEGER;
            l INTEGER;
            f INTEGER;
        BEGIN
            m := a / b;
            g := a * b;
            l := a + b;
            f := a - b;
            RETURN l;
        END;
    """
    
    udf_basic_pl_sql_pragma = """
        CREATE OR REPLACE FUNCTION udf_basic_plsql_pragma(a INTEGER,b FLOAT) 
            RETURN FLOAT 
        IS 
            PRAGMA UDF;
            m INTEGER;
            g INTEGER;
            l INTEGER;
            f INTEGER;
        BEGIN
            m := a / b;
            g := a * b;
            l := a + b;
            f := a - b;
            RETURN l;
        END;
    """
    
    # Number of executed tupels (inserted into db before execution), Method of execution, execution time in seconds
    udf_basic_times = [
    [1000, 'SQL', 0.018], [10000,  'SQL' ,0.019],  [100000,  'SQL' , 0.163],  [1_000_000,  'SQL', 1.794],  [5000000, 'SQL', 9.029],
    [1000, 'PL/pgSQL', 0.045], [10000, 'PL/pgSQL', 0.06],  [100000, 'PL/pgSQL', 0.227],  [1_000_000, 'PL/pgSQL', 2.118],  [5000000, 'PL/pgSQL', 9.83],
    [1000, 'PL/SQL Pragma', 0.077], [10000, 'PL/SQL Pragma' ,0.071],  [100000,  'PL/SQL Pragma' , 0.262],  [1_000_000,  'PL/SQL Pragma' , 2.308],  [5000000, 'PL/SQL Pragma', 11.329],
    [1000, 'Pandas', 0.02], [10000, 'Pandas' ,0.036],  [100000,  'Pandas' , 0.244],  [1_000_000,  'Pandas' , 2.452],  [500000, 'Pandas', 11.364],
    [1000, 'PL/Python', 0.037], [10000, 'PL/Python', 0.063],  [100000, 'PL/Python', 0.304],  [1_000_000, 'PL/Python', 2.768],  [5000000, 'PL/Python', 19.032],
    [1000, 'PL/SQL', 0.05], [10000,'PL/SQL', 0.077],  [100000, 'PL/SQL', 0.333],  [1_000_000, 'PL/SQL', 3.205],  [5000000, 'PL/SQL', 19.596]
    ]


import math
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator
class IsPrime:
    # Function to determine if an given input integer is a prime number and if not which is the first divisor
    def isprime(a: int) -> str:
        if a % 2 == 0 and a != 2:
            return 'Factor: ' + str(2)
        elif a % 3 == 0 and a != 3:
            return 'Factor: ' + str(3)
        else:
            m = math.sqrt(a) + 1
            if a > 1:
                for i in range(2,int(m)):
                    if (a%i) == 0:
                        return 'Factor: ' + str(i)
            else:
                return 'No Prime Number'
        return 'Prime number'
    
    isprime_sql="""
        CREATE OR REPLACE FUNCTION isprime_sql(a int4) 
            RETURNS varchar
        AS $$
            WITH RECURSIVE run("rec?", "label", "res", "a", "i", "m") AS
            (
                (SELECT "ifresult10".*
                FROM (LATERAL
                    (SELECT (("a" % 2) = 0 AND "a" <> 2) AS "q4_1") AS "let9"("q4_1")
                    LEFT OUTER JOIN
                    LATERAL
                    ((SELECT False, 
                                NULL :: text, 
                                (SELECT concat('Faktor: ', 2) AS "concat") AS "result", 
                                NULL, 
                                NULL, 
                                NULL
                        WHERE "q4_1")
                        UNION ALL
                        (SELECT "ifresult13".*
                        FROM (LATERAL
                            (SELECT (("a" % 3) = 0 AND "a" <> 3) AS "q9_2") AS "let12"("q9_2")
                            LEFT OUTER JOIN
                            LATERAL
                            ((SELECT False, 
                                        NULL :: text, 
                                        (SELECT concat('Faktor: ', 3) AS "concat") AS "result", 
                                        NULL, 
                                        NULL, 
                                        NULL
                                WHERE "q9_2")
                                UNION ALL
                                (SELECT "ifresult17".*
                                FROM (LATERAL (SELECT (sqrt("a")) + (1) AS "m_3") AS "let15"("m_3")
                                    LEFT OUTER JOIN
                                    (LATERAL (SELECT "a" > 1 AS "q14_3") AS "let16"("q14_3")
                                        LEFT OUTER JOIN
                                        LATERAL
                                        ((SELECT True, 
                                                'fori15_head', 
                                                NULL :: varchar, 
                                                "a", 
                                                (SELECT 2 AS "?column?"), 
                                                "m_3"
                                        WHERE "q14_3")
                                        UNION ALL
                                        (SELECT False, 
                                                NULL :: text, 
                                                (SELECT 'Keine' AS "?column?") AS "result", 
                                                NULL, 
                                                NULL, 
                                                NULL
                                        WHERE NOT "q14_3")
                                        ) AS "ifresult17"
                                        ON True)
                                    ON True)
                                WHERE NOT "q9_2")
                            ) AS "ifresult13"
                            ON True)
                        WHERE NOT "q4_1")
                    ) AS "ifresult10"
                    ON True))
                UNION ALL
                (SELECT "result".*
                FROM run AS "run"("rec?", "label", "res", "a", "i", "m"), 
                    LATERAL
                    (SELECT "ifresult2".*
                    FROM (LATERAL (SELECT "m" AS "q16_5") AS "let0"("q16_5")
                            LEFT OUTER JOIN
                            (LATERAL (SELECT "i" <= "q16_5" AS "pred_5") AS "let1"("pred_5")
                            LEFT OUTER JOIN
                            LATERAL
                            ((SELECT "ifresult4".*
                                FROM (LATERAL (SELECT ("a" % "i") = 0 AS "q20_6") AS "let3"("q20_6")
                                    LEFT OUTER JOIN
                                    LATERAL
                                    ((SELECT False, 
                                            NULL :: text, 
                                            (SELECT concat('Faktor: ', "i") AS "concat") AS "result", 
                                            "run"."a", 
                                            "run"."i", 
                                            "run"."m"
                                        WHERE "q20_6")
                                        UNION ALL
                                    (SELECT "return7".*
                                        FROM (LATERAL (SELECT "i" + 1 AS "i_8") AS "let6"("i_8")
                                            LEFT OUTER JOIN
                                            LATERAL
                                            (SELECT True, 'fori15_head', NULL :: varchar, "a", "i_8", "m"
                                            ) AS "return7"
                                            ON True)
                                        WHERE NOT "q20_6")
                                    ) AS "ifresult4"
                                    ON True)
                                WHERE "pred_5")
                                UNION ALL
                            (SELECT False, 
                                    NULL :: text, 
                                    (SELECT 'Prim!' AS "?column?") AS "result", 
                                    "run"."a", 
                                    "run"."i", 
                                    "run"."m"
                                WHERE NOT "pred_5")
                            ) AS "ifresult2"
                            ON True)
                            ON True)
                    WHERE "run"."label" = 'fori15_head'
                    ) AS "result"
                WHERE "run"."rec?" = True)
            )
            SELECT "run"."res" AS "res"
            FROM run AS "run"
            WHERE "run"."rec?" = False
        $$ LANGUAGE SQL;
    """

    isprime_plpy= """
        CREATE OR REPLACE FUNCTION isprime(a INTEGER) 
            RETURNS VARCHAR 
        AS $$ 
            import math
            if a % 2 == 0 and a != 2:
                return 'Factor: ' + str(2)
            elif a % 3 == 0 and a != 3:
                return 'Factor: ' + str(3)
            else:
                m = math.sqrt(a) + 1
                if a > 1:
                    for i in range(2,int(m)):
                        if (a%i) == 0:
                            return 'Factor: ' + str(i)
                else:
                    return 'No Prime Number'
            return 'Prime number'
        $$ LANGUAGE plpython3u;
        """

    isprime_plpgsql = """
        CREATE OR REPLACE FUNCTION isprime_pgplsql(a integer)
            RETURNS VARCHAR
        AS $$
        DECLARE 
            m INTEGER;
            i INTEGER;
        BEGIN
            IF MOD(a,2) = 0 and a != 2 THEN
                RETURN CONCAT('Factor: ', CAST(2 AS VARCHAR));
            ELSIF MOD(a,3) = 0 and a != 3 THEN
                RETURN CONCAT('Factor: ', CAST(3 AS VARCHAR));
            ELSE
                m := sqrt(a) + 1;
            IF a > 1 THEN
                FOR i IN 2..CAST(m AS INTEGER) LOOP
                    IF (MOD(a,i)) = 0 THEN
                        RETURN CONCAT('Factor: ', CAST(i AS VARCHAR2));
                    END IF;
                END LOOP;
            ELSE
                RETURN 'Not a Prime Number';
            END IF;
            END IF;
            RETURN 'Prime number';
        END; 
        $$; LANGUAGE 'plpgsql'
    """
    # Removed typecasting in for loop iteration
    def isprime_orcl(a: int) -> str:
        if a != 2 and a % 2 == 0:
            return 'Factor: ' + str(2)
        elif a != 3 and a % 3 == 0:
            return 'Factor: ' + str(3)
        else:
            m = math.sqrt(a) + 1
            if a > 1:
                for i in range(2, m):
                    if (a%i) == 0:
                        return 'Factor: ' + str(i)
            else:
                return 'No Prime Number'
        return 'Prime number'
    
    isprime_plsql = """
        CREATE OR REPLACE FUNCTION isprime_plsql(a INTEGER) 
            RETURN VARCHAR2 
        IS 
            m INTEGER;
            i INTEGER;
        BEGIN
            IF MOD(a,2) = 0 and a != 2 THEN
                RETURN CONCAT('Factor: ', CAST(2 AS VARCHAR2));
            ELSIF MOD(a,3) = 0 and a != 3 THEN
                RETURN CONCAT('Factor: ', CAST(3 AS VARCHAR2));;
            ELSE
                m := sqrt(a) + 1;
            IF a > 1 THEN
                FOR i IN 2..m LOOP
                    IF (MOD(a,i)) = 0 THEN
                        RETURN CONCAT('Factor: ', CAST(i AS VARCHAR2));
                    END IF;
                END LOOP;
            ELSE
                RETURN 'Not a Prime Number';
            END IF;
            END IF;
            RETURN 'Prime number';
        END;
    """

    # Removed typecasting in for loop iteration
    isprime_plsql_pragma = """
        CREATE OR REPLACE FUNCTION isprime_pl_pragma(a INTEGER) 
            RETURN VARCHAR2 
        IS 
            PRAGMA UDF;
            m INTEGER;
            i INTEGER;
        BEGIN
            IF MOD(a,2) = 0 and a != 2 THEN
                RETURN CONCAT('Factor: ', CAST(2 AS VARCHAR2));
            ELSIF MOD(a,3) = 0 and a != 3 THEN
                RETURN CONCAT('Factor: ', CAST(3 AS VARCHAR2));;
            ELSE
                m := sqrt(a) + 1;
            IF a > 1 THEN
                FOR i IN 2..m LOOP
                    IF (MOD(a,i)) = 0 THEN
                        RETURN CONCAT('Factor: ', CAST(i AS VARCHAR2));
                    END IF;
                END LOOP;
            ELSE
                RETURN 'Not a Prime Number';
            END IF;
            END IF;
            RETURN 'Prime number';
        END;
    """

    # Number of executed tupels (inserted into db before execution), Method of execution, execution time in seconds
    udf_isprime_times = [
    [1000, 'PL/Python', 0.05], [10000, 'PL/Python', 0.074],  [100000, 'PL/Python', 0.379],  [1_000_000, 'PL/Python', 3.521],  [5000000, 'PL/Python', 17.245],
    [1000, 'PL/pgSQL',0.131], [10000, 'PL/pgSQL', 0.152],  [100000, 'PL/pgSQL', 0.349],  [1_000_000, 'PL/pgSQL', 2.384],  [5000000, 'PL/pgSQL', 12.799],
    [1000, 'PL/SQL', 0.132], [10000,'PL/SQL', 0.154],  [100000, 'PL/SQL', 0.52],  [1_000_000, 'PL/SQL', 4.352],  [5000000, 'PL/SQL', 19.73],
    [1000, 'PL/SQL Pragma', 0.128], [10000, 'PL/SQL Pragma' ,0.151],  [100000,  'PL/SQL Pragma' , 0.446],  [1_000_000,  'PL/SQL Pragma' , 3.209],  [5000000, 'PL/SQL Pragma', 13.906],
    [1000, 'Pandas', 0.021], [10000, 'Pandas',0.043],  [100000,  'Pandas' , 0.321],  [1_000_000,  'Pandas' , 3.185],  [5000000, 'Pandas', 16.906],
    [1000, 'SQL', 0.114], [10000,'SQL', 0.514],  [100000,  'SQL' , 6.033],  [1_000_000,  'SQL', 50.120],  [5000000, 'SQL', 302.955]
    ]


import grizzly
class cursor_loop:
    # Function to iterate over 10 tupels of table speedtest in UDF
    # Connect to db putside udf
    import psycopg2
    con_pd = psycopg2.connect()
    grizzly.use(RelationalExecutor(con_pd, SQLGenerator('oracle')))
    def cursor_loop(a: int) -> int:
        g_df1 = grizzly.read_table("speedtest")
        g_df1 = g_df1[g_df1.test_id < 10] 
        g_df1 = g_df1[["test_number", "test_float"]]

        f = 0
        for tuple in g_df1:
            try:
                if tuple.test_number % a > 2:
                    f = f + tuple.test_number
                else:
                    f = f - tuple.test_number
            except ZeroDivisionError:
                f = f-1
        return f
    
    cursor_loop_plpgsql = """
        CREATE OR REPLACE FUNCTION cursor_loop_pgplsql(a INTEGER) 
            RETURNS INTEGER
        AS $$ 
        DECLARE 
            f INTEGER;
            r FLOAT8;
            g_df1 CURSOR FOR SELECT t14.test_number,t14.test_float FROM (SELECT * FROM (SELECT * FROM speedtest t12) t13 WHERE t13.test_id < 10) t14;
        BEGIN      
            f := 0;
            FOR tuple IN g_df1 LOOP
                BEGIN
                    IF MOD(tuple.test_number,a) > 2 THEN
                        f := f + tuple.test_number;
                    ELSE
                        f := f - tuple.test_number;
                    END IF;
                EXCEPTION
                    WHEN division_by_zero THEN
                        f := f - 1;
                END;
            END LOOP;
            RETURN f;
        END; $$ LANGUAGE plpgsql;
    """

    cursor_loop_plsql = """
        CREATE OR REPLACE FUNCTION cursor_loop_plsql(a INTEGER) 
            RETURN INTEGER
        IS 
            f INTEGER;
            r FLOAT;
            CURSOR g_df1 IS SELECT t15.test_number,t15.test_float FROM (SELECT * FROM (SELECT * FROM speedtest t13) t14 WHERE t14.test_id < 10) t15;
        BEGIN
            f := 0;
            FOR tuple IN g_df1 LOOP
                BEGIN
                    IF MOD(tuple.test_number,a) > 2 THEN
                        f := f + tuple.test_number;
                    ELSE
                        f := f - tuple.test_number;
                    END IF;
                EXCEPTION
                    WHEN Zero_Divide THEN
                        f := f - 1;
                END;
            END LOOP;
            RETURN f;
        END;
    """

    cursor_loop_plsql_pragma = """
        CREATE OR REPLACE FUNCTION cursor_loop_plsql_pragma(a INTEGER) 
            RETURN INTEGER
        IS 
            PRAGMA UDF;
            f INTEGER;
            r FLOAT;
            CURSOR g_df1 IS SELECT t15.test_number,t15.test_float FROM (SELECT * FROM (SELECT * FROM speedtest t13) t14 WHERE t14.test_id < 10) t15;
        BEGIN
            f := 0;
            FOR tuple IN g_df1 LOOP
                BEGIN
                    IF MOD(tuple.test_number,a) > 2 THEN
                        f := f + tuple.test_number;
                    ELSE
                        f := f - tuple.test_number;
                    END IF;
                EXCEPTION
                    WHEN Zero_Divide THEN
                        f := f - 1;
                END;
            END LOOP;
            RETURN f;
        END;
    """

    # Added plpy cursor instead of grizzly connection
    cursor_loop_plpy = """
        CREATE OR REPLACE FUNCTION cursor_loop_plpy(a INTEGER)
            RETURNS INTEGER
        AS $$

            g_df1 = plpy.cursor("SELECT t14.test_number,t14.test_float FROM (SELECT * FROM (SELECT * FROM speedtest t12) t13 WHERE t13.test_id < 10) t14;")
            f = 0
            for tuple in g_df1:
                try:
                    if tuple['test_number'] % a > 2:
                        f = f + tuple['test_number']
                    else:
                        f = f - tuple['test_number']
                except ZeroDivisionError:
                    f = f-1
            return f
        $$ LANGUAGE plpython3u;
    """

    # Number of executed tupels (inserted into db before execution), Method of execution, execution time in seconds
    udf_cursor_loop_times = [ 
    [100, 'PL/Python', 0.126], [1000, 'PL/Python', 0.162],  [10000, 'PL/Python', 5.626],  [50000, 'PL/Python', 120.829],
    [100, 'PL/pgSQL',0.158], [1000, 'PL/pgSQL', 0.179],  [10000, 'PL/pgSQL', 4.847],  [50000, 'PL/pgSQL', 113.877],
    [100, 'PL/SQL', 0.124], [1000,'PL/SQL', 0.158],  [10000, 'PL/SQL', 1.545],  [50000, 'PL/SQL', 28.96],
    [100, 'PL/SQL Pragma', 0.141], [1000, 'PL/SQL Pragma' ,0.152],  [10000,  'PL/SQL Pragma' , 1.542],  [50000,  'PL/SQL Pragma' , 30.305],
    [100, 'Pandas', 0.035], [1000, 'Pandas' ,0.271],  [10000,  'Pandas' , 7.432],  [50000,  'Pandas' , 182.665]

    ]

class Repeat:
    # equivalent to udf repeat used in grizzly papaer (https://www.cidrdb.org/cidr2021/papers/cidr2021_paper07.pdf)
    def udf_repeat(a: int, b: str) -> str:
        return a * b
    
    udf_simple_plpy = """"
        CREATE OR REPLACE FUNCTION udf_repeat(a INTEGER,b VARCHAR) 
            RETURNS VARCHAR 
        AS $$ 
            return a * b
        $$ LANGUAGE plpython3u;
    """

    udf_simple_plpgsql = """
        CREATE OR REPLACE FUNCTION udf_repeat(a INTEGER,b VARCHAR) 
            RETURNS VARCHAR 
        AS $$ 
        DECLARE 
        BEGIN
            RETURN REPEAT(b, a);
        END; 
        $$ LANGUAGE plpgsql;
    """

    # Use of datatype CLOB for oracle DB
    udf_simple_plsql = """
        CREATE OR REPLACE FUNCTION udf_repeat(a INTEGER,b VARCHAR2) 
            RETURN CLOB
        IS 
        BEGIN
            RETURN RPAD(b, LENGTH(b)*a, b);
        END;
    """

    udf_simple_plsql_pragma = """
        CREATE OR REPLACE FUNCTION udf_repeat(a INTEGER,b VARCHAR2) 
            RETURN CLOB
        IS 
            PRAGMA UDF;
        BEGIN
            RETURN RPAD(b, LENGTH(b)*a, b);
        END;
    """