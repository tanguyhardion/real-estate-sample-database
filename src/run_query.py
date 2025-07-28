import sqlite3

# define the SQL query statement
QUERY_STATEMENT = "SELECT * FROM Tenant LIMIT 10;"

# connect to the database
connection = sqlite3.connect("database/real_estate.db")
cursor = connection.cursor()

# execute the query
cursor.execute(QUERY_STATEMENT)

# fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# close the connection
connection.close()
