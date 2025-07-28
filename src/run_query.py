import sqlite3

# define the SQL query statement
QUERY_STATEMENT = "SELECT t.name, t.phone, t.email, SUM(l.rent) AS total_rent_paid FROM Tenant t JOIN Lease l ON t.id = l.tenant_id GROUP BY t.name ORDER BY total_rent_paid DESC LIMIT 1;"

# connect to the database
connection = sqlite3.connect("real_estate.db")
cursor = connection.cursor()

# execute the query
cursor.execute(QUERY_STATEMENT)

# fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# close the connection
connection.close()
