def doit():
    import urllib
    sql = "Select * from customer"
    customer = pd.read_sql(sql,"postgresql://postgres:password123@localhost:5432/tpch")
    orders = pd.read_csv("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", sep="|")
    #j1 = orders.join(customer.set_index("c_custkey"))
    j1 = orders.merge(customer, left_on='o_custkey', right_on='c_custkey')
    a = j1.groupby(["c_mktsegment"])["o_orderkey"].count()
    print(a)

if __name__ == '__main__':
    import os
#    os.environ["MODIN_CPUS"] = "12"
    os.environ["MODIN_OUT_OF_CORE"] = "true"
    os.environ["MODIN_ENGINE"] = "ray"
    import modin.pandas as pd
    doit()
