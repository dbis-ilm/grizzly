# Number of executed tupel (inserted into db before execution), Method of execution, execution time in seconds
udf_basic_times = [
    [10000,  'SQL' ,0.02],  [100000,  'SQL' , 0.141],  [1_000_000,  'SQL', 1.355],  [5000000, 'SQL', 7.050],
    [10000, 'PL/pgSQL', 0.064],  [100000, 'PL/pgSQL', 0.232],  [1_000_000, 'PL/pgSQL', 1.978],  [5000000, 'PL/pgSQL', 9.868],
    [10000, 'PL/pgSQL Parralel', 0.068],  [100000, 'PL/pgSQL Parralel', 0.235],  [1_000_000, 'PL/pgSQL Parralel', 1.298],  [5000000, 'PL/pgSQL Parralel', 5.988],
    [10000, 'PL/SQL Pragma' ,0.079],  [100000,  'PL/SQL Pragma' , 0.274],  [1_000_000,  'PL/SQL Pragma' , 1.29],  [5000000, 'PL/SQL Pragma', 5.989],
    [10000, 'Pandas' ,0.031],  [100000,  'Pandas' , 0.176],  [1_000_000,  'Pandas' , 1.671],  [500000, 'Pandas', 8.588],
    [10000, 'PL/Python', 0.102],  [100000, 'PL/Python', 0.367],  [1_000_000, 'PL/Python', 2.871],  [5000000, 'PL/Python', 14.217],
    [10000, 'PL/Python Parallel', 0.092],  [100000, 'PL/Python Parallel', 0.334],  [1_000_000, 'PL/Python Parallel', 1.732],  [5000000, 'PL/Python Parallel', 8.289],
    [10000,'PL/SQL', 0.086],  [100000, 'PL/SQL', 0.371],  [1_000_000, 'PL/SQL', 3.193],  [5000000, 'PL/SQL', 15.706],
    ]

# Number of executed tupel (inserted into db before execution), Method of execution, execution time in seconds
udf_isprime_times = [
    [10000, 'PL/Python', 0.137],  [100000, 'PL/Python', 0.402],  [1_000_000, 'PL/Python', 3.566],  [5000000, 'PL/Python', 18,348],
    [10000, 'PL/pgSQL', 0.145],  [100000, 'PL/pgSQL', 0.355],  [1_000_000, 'PL/pgSQL', 2.512],  [5000000, 'PL/pgSQL', 12.723],
    [10000,'PL/SQL', 0.154],  [100000, 'PL/SQL', 0.52],  [1_000_000, 'PL/SQL', 4.352],  [5000000, 'PL/SQL', 22,9535],
    [10000, 'PL/SQL Pragma' ,0.151],  [100000,  'PL/SQL Pragma' , 0.494],  [1_000_000,  'PL/SQL Pragma' , 3.775],  [5000000, 'PL/SQL Pragma', 17.988],
    [10000, 'Pandas',0.06],  [100000,  'Pandas' , 0.246],  [1_000_000,  'Pandas' , 2.368],  [5000000, 'Pandas', 11.789],
    [10000,'SQL', 0.546],  [100000,  'SQL' , 5.517],  [1_000_000,  'SQL', 54.420],  [5000000, 'SQL', 277.835],
    [10000, 'PL/Python Parallel', 0.106],  [100000, 'PL/Python Parallel', 0.391],  [1_000_000, 'PL/Python Parallel', 1.955],  [5000000, 'PL/Python Parallel', 9.808],
    [10000, 'PL/pgSQL Parralel', 0.171],  [100000, 'PL/pgSQL Parralel', 0.357],  [1_000_000, 'PL/pgSQL Parralel', 1.554],  [5000000, 'PL/pgSQL Parralel', 7.095]
    ]

# Number of executed tupel (inserted into db before execution), Method of execution, execution time in seconds
udf_cursor_loop_times = [ 
    [1000, 'PL/Python', 0.179],  [10000, 'PL/Python', 5.737],  [50000, 'PL/Python', 121.51],
    [1000, 'PL/pgSQL', 0.169],  [10000, 'PL/pgSQL', 5.174],  [50000, 'PL/pgSQL', 119.843],
    [1000,'PL/SQL', 0.165],  [10000, 'PL/SQL', 1.561],  [50000, 'PL/SQL', 30.820],
    [1000, 'PL/SQL Pragma' ,0.159],  [10000,  'PL/SQL Pragma' , 1.599],  [50000,  'PL/SQL Pragma' , 30.88],
    [1000, 'Pandas' ,0.279],  [10000,  'Pandas' , 7.608],  [50000,  'Pandas' , 131.718]
    ]