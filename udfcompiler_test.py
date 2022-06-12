import random
import grizzly
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException, UDFParseException
from grizzly.udfcompiler import test_udfs

import cx_Oracle
import psycopg2

import logging

class TestPrepper:
    def __init__(self, con):
        self.con = con
        self.c = con.cursor()
    
    # Method to drop a table with a specified name
    def drop_test_table(self, table_name):
        try:
            self.c.execute(f'DROP TABLE {table_name}')
        except Exception as e:
            print("No Table deleted:", e)
        self.con.commit()

    # Method to create a table with predefined columns (test_id, test_text, test_number, test_float)
    def create_test_table(self, table_name):
        self.drop_test_table(table_name)
        self.c.execute(f"""CREATE TABLE {table_name} (
                test_id INT,
                test_text VARCHAR(255), 
                test_number INT,
                test_float FLOAT
            )
        """)

    # Method to insert data in the testtable
    def insert_test_data(self, table_name, start = 0, end = 20):
        rows = []
        rows2 = []
        # Prepare Data for insertion
        for i in range(start, end):
            rand_int = random.randint(25, 50)
            rand_float = random.uniform(25.0, 50.0)
            text = f"'{str(i)}. Entry'"
            rows.append(f"({i}, {text}, {rand_int}, {rand_float})")
            rows2.append((i, text, rand_int, rand_float))
        
        if type(self.con) == cx_Oracle.Connection:
            # Insert into oracle db
            self.c.executemany(
                f"""
                        INSERT INTO {table_name}(
                            test_id,
                            test_text,
                            test_number,
                            test_float
                            )
                        VALUES (:test_id, :test_text, :test_number, :test_float)
                """, rows2
            )
        else:
            # Insert into postgresql db
            values = ", ".join(map(str, rows))
            self.c.execute(f"""
                        INSERT INTO {table_name}(
                            test_id,
                            test_text,
                            test_number,
                            test_float
                        )
                        VALUES {values}
                """)

        self.con.commit()
        print(f"-- Inserted {end - start} rows to DB: {self.con.dsn}:{table_name}")


class Tester:
    def __init__(self, con, test_table):
        self.con = con
        self.c = con.cursor()
        self.test_table = test_table

    def prep_df(self):
        grizzly.use(RelationalExecutor(self.con))
        df = grizzly.read_table(self.test_table)
        df = df[["test_id", "test_text", "test_float", "test_number"]]
        
        return df

    def main_test(self):
        results = {}
        for func in test_udfs.all_funcs_two_param:
            try:
                df = self.prep_df()
                df["udf"] = df[["test_id", "test_number"]].map(func, lang='sql')
                df.show(limit = 1)
                results[func.__name__] = True
                #results[func.__name__] = df.shape == (5,20)
            except (UDFCompilerException, UDFParseException):
                results[func.__name__] = False
            except Exception as e:
                results[func.__name__] = e

        for func in test_udfs.all_funcs_two_param_str:
            try:
                df = self.prep_df()
                df["udf"] = df[["test_id", "test_text"]].map(func, lang='sql')
                df.show(limit = 1)
                results[func.__name__] = True
                #results[func.__name__] = df.shape == (5,20)
            except (UDFCompilerException, UDFParseException):
                results[func.__name__] = False
            except Exception as e:
                results[func.__name__] = e

        for func in test_udfs.all_funcs_one_param:
            try:
                df = self.prep_df()
                df["udf"] = df[["test_id"]].map(func, lang='sql')
                df.show(limit = 1)
                results[func.__name__] = True
                #results[func.__name__] = df.shape == (5,20)
            except (UDFCompilerException, UDFParseException):
                results[func.__name__] = False
            except Exception as e:
                results[func.__name__] = e

        for func in test_udfs.not_supported_funcs:
            try:
                df = self.prep_df()
                df["udf"] = df[["test_id"]].map(func, lang='sql', fallback=True)
                df.show(limit = 1)
                results[f'{func.__name__} (Fallback Mode)'] = True
                #results[f'{func.__name__} (Fallback Mode)'] = df.shape == (5,20)
            except (UDFCompilerException, UDFParseException):
                results[func.__name__] = False
            except Exception as e:
                results[func.__name__] = e

        self.con.close()
        return results

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)

    con2 = cx_Oracle.connect()
    con = psycopg2.connect()
    test_table = 'udf_test'

    tp = TestPrepper(con)
    tp.create_test_table(test_table)
    tp.insert_test_data(test_table)

    t = Tester(con, test_table)
    results = t.main_test()

    failed = 0
    print()
    for result in results:
        if results[result] == False:
            print(f'{result}:', end ='')
            print("\033[91m {}\033[00m".format('failed'))
            failed += 1
        elif results[result] == True:
            print(f'{result}:', end ='')
            print("\033[92m {}\033[00m".format('passed'))
        else:
            print(f'{result}:', end ='')
            print("\033[91m {}\033[00m".format(f'No compiling or parsing error: {results[result]}'))
            failed += 1
        
    print(f'\nfailed: {failed}, passed: {len(results)-failed}')
