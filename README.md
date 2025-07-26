# Real Estate Sample Database

This project demonstrates a simple SQLite database for managing real estate data. It includes Python scripts to create the database and query it.

## Files

- `createdb.py`: Script to create and populate the SQLite database.
- `query.py`: Script to query the database for specific information.
- `real_estate.db`: The SQLite database file.

## Usage

1. Run `createdb.py` to create and populate the database.
2. Run `query.py` to execute predefined queries and fetch results.

## Requirements

- Python 3.x
- SQLite

## Example Query

The `query.py` script fetches the tenant who has paid the highest total rent:

```sql
SELECT t.name, t.phone, t.email, SUM(l.rent) AS total_rent_paid 
FROM Tenant t 
JOIN Lease l ON t.id = l.tenant_id 
GROUP BY t.name 
ORDER BY total_rent_paid DESC 
LIMIT 1;
```
