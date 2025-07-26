import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = 'real_estate.db'

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Schema
c.execute('''CREATE TABLE IF NOT EXISTS Fund (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    inception_date DATE,
    manager TEXT,
    total_assets REAL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Property (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    city TEXT,
    state TEXT,
    zip TEXT,
    type TEXT,
    value REAL,
    fund_id INTEGER,
    FOREIGN KEY(fund_id) REFERENCES Fund(id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Tenant (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Lease (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    tenant_id INTEGER,
    start_date DATE,
    end_date DATE,
    rent REAL,
    deposit REAL,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(tenant_id) REFERENCES Tenant(id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Payment (
    id INTEGER PRIMARY KEY,
    lease_id INTEGER,
    payment_date DATE,
    amount REAL,
    FOREIGN KEY(lease_id) REFERENCES Lease(id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS FundPerformance (
    id INTEGER PRIMARY KEY,
    fund_id INTEGER,
    date DATE,
    nav REAL,
    FOREIGN KEY(fund_id) REFERENCES Fund(id)
)''')

conn.commit()

# Sample Data Generation
fund_names = [f"Fund {i}" for i in range(1, 11)]
manager_names = [f"Manager {i}" for i in range(1, 6)]
cities = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami',
    'London', 'Paris', 'Berlin', 'Madrid', 'Rome',
    'Tokyo', 'Osaka', 'Seoul', 'Beijing', 'Shanghai',
    'Sydney', 'Melbourne', 'Toronto', 'Vancouver', 'Montreal',
    'Dubai', 'Abu Dhabi', 'Singapore', 'Hong Kong', 'Bangkok',
    'Cape Town', 'Johannesburg', 'Moscow', 'Saint Petersburg', 'Istanbul',
    'Mexico City', 'São Paulo', 'Buenos Aires', 'Lima', 'Santiago',
    'Delhi', 'Mumbai', 'Bangalore', 'Jakarta', 'Kuala Lumpur',
    'Cairo', 'Riyadh', 'Tel Aviv', 'Warsaw', 'Prague',
    'Vienna', 'Zurich', 'Geneva', 'Brussels', 'Amsterdam'
]
property_types = ['Apartment', 'Office', 'Retail', 'Warehouse', 'Industrial']
tenant_names = [f"Tenant {i}" for i in range(1, 501)]

# Funds
for i, name in enumerate(fund_names, 1):
    inception = datetime(2010, 1, 1) + timedelta(days=random.randint(0, 4000))
    manager = random.choice(manager_names)
    assets = round(random.uniform(10_000_000, 500_000_000), 2)
    c.execute('INSERT INTO Fund (id, name, inception_date, manager, total_assets) VALUES (?, ?, ?, ?, ?)',
              (i, name, inception.date(), manager, assets))

# Properties
for i in range(1, 1001):
    address = f"{random.randint(100,9999)} Main St"
    city = random.choice(cities)
    state = random.choice(['NY', 'CA', 'IL', 'TX', 'FL'])
    zip_code = f"{random.randint(10000,99999)}"
    ptype = random.choice(property_types)
    value = round(random.uniform(100_000, 10_000_000), 2)
    fund_id = random.randint(1, len(fund_names))
    c.execute('INSERT INTO Property (id, address, city, state, zip, type, value, fund_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (i, address, city, state, zip_code, ptype, value, fund_id))

# Tenants
for i, name in enumerate(tenant_names, 1):
    phone = f"({random.randint(100,999)})-{random.randint(100,999)}-{random.randint(1000,9999)}"
    email = f"tenant{i}@example.com"
    c.execute('INSERT INTO Tenant (id, name, phone, email) VALUES (?, ?, ?, ?)',
              (i, name, phone, email))

# Leases
lease_id = 1
for property_id in range(1, 1001):
    num_leases = random.randint(1, 3)
    for _ in range(num_leases):
        tenant_id = random.randint(1, len(tenant_names))
        start = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
        end = start + timedelta(days=random.randint(180, 720))
        rent = round(random.uniform(1000, 20000), 2)
        deposit = round(rent * random.uniform(0.5, 2), 2)
        c.execute('INSERT INTO Lease (id, property_id, tenant_id, start_date, end_date, rent, deposit) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (lease_id, property_id, tenant_id, start.date(), end.date(), rent, deposit))
        lease_id += 1

# Payments
for lease in c.execute('SELECT id, start_date, end_date, rent FROM Lease'):
    lease_id, start_date, end_date, rent = lease
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    months = (end.year - start.year) * 12 + (end.month - start.month)
    for m in range(months):
        pay_date = start + timedelta(days=30*m)
        amount = rent
        c.execute('INSERT INTO Payment (lease_id, payment_date, amount) VALUES (?, ?, ?)',
                  (lease_id, pay_date.date(), amount))

# Fund Performance
for fund_id in range(1, len(fund_names)+1):
    for d in range(0, 1825, 30):  # 5 years, monthly
        date = datetime(2020, 1, 1) + timedelta(days=d)
        nav = round(random.uniform(10_000_000, 500_000_000), 2)
        c.execute('INSERT INTO FundPerformance (fund_id, date, nav) VALUES (?, ?, ?)',
                  (fund_id, date.date(), nav))

conn.commit()
conn.close()

print('Database created and populated with sample data.')
