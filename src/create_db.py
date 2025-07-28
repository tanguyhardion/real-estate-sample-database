import sqlite3
import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker()

DB_PATH = "database/real_estate.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# drop existing tables to start fresh
tables_to_drop = [
    "Insurance",
    "LeaseRenewal",
    "PropertyAmenity",
    "Amenity",
    "MarketData",
    "TenantHistory",
    "Utility",
    "Inspection",
    "PropertyDocument",
    "Expense",
    "MaintenanceRequest",
    "Vendor",
    "PropertyManagerAssignment",
    "PropertyManager",
    "FundPerformance",
    "Payment",
    "Lease",
    "Tenant",
    "Property",
    "Fund",
]

print("Dropping existing tables...")
for table in tables_to_drop:
    c.execute(f"DROP TABLE IF EXISTS {table}")

print("Creating new tables...")

# schema
c.execute(
    """CREATE TABLE IF NOT EXISTS Fund (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    inception_date DATE,
    manager TEXT,
    total_assets REAL
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Property (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    city TEXT,
    state TEXT,
    zip TEXT,
    type TEXT,
    value REAL,
    fund_id INTEGER,
    FOREIGN KEY(fund_id) REFERENCES Fund(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Tenant (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Lease (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    tenant_id INTEGER,
    start_date DATE,
    end_date DATE,
    rent REAL,
    deposit REAL,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(tenant_id) REFERENCES Tenant(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Payment (
    id INTEGER PRIMARY KEY,
    lease_id INTEGER,
    payment_date DATE,
    amount REAL,
    FOREIGN KEY(lease_id) REFERENCES Lease(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS FundPerformance (
    id INTEGER PRIMARY KEY,
    fund_id INTEGER,
    date DATE,
    nav REAL,
    FOREIGN KEY(fund_id) REFERENCES Fund(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS PropertyManager (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    hire_date DATE,
    salary REAL,
    is_active BOOLEAN
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS PropertyManagerAssignment (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    manager_id INTEGER,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(manager_id) REFERENCES PropertyManager(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Vendor (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    rating REAL,
    is_active BOOLEAN
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS MaintenanceRequest (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    tenant_id INTEGER,
    vendor_id INTEGER,
    manager_id INTEGER,
    category TEXT,
    description TEXT,
    priority TEXT,
    status TEXT,
    created_date DATE,
    completed_date DATE,
    estimated_cost REAL,
    actual_cost REAL,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(tenant_id) REFERENCES Tenant(id),
    FOREIGN KEY(vendor_id) REFERENCES Vendor(id),
    FOREIGN KEY(manager_id) REFERENCES PropertyManager(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Expense (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    vendor_id INTEGER,
    category TEXT,
    description TEXT,
    amount REAL,
    expense_date DATE,
    invoice_number TEXT,
    is_recurring BOOLEAN,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(vendor_id) REFERENCES Vendor(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS PropertyDocument (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    document_type TEXT,
    document_name TEXT,
    file_path TEXT,
    upload_date DATE,
    expiry_date DATE,
    FOREIGN KEY(property_id) REFERENCES Property(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Inspection (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    inspector_name TEXT,
    inspection_type TEXT,
    inspection_date DATE,
    overall_rating TEXT,
    notes TEXT,
    next_inspection_date DATE,
    FOREIGN KEY(property_id) REFERENCES Property(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Utility (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    utility_type TEXT,
    provider TEXT,
    account_number TEXT,
    monthly_average REAL,
    is_tenant_responsibility BOOLEAN,
    FOREIGN KEY(property_id) REFERENCES Property(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS TenantHistory (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER,
    previous_address TEXT,
    employment_status TEXT,
    annual_income REAL,
    credit_score INTEGER,
    reference_contacts TEXT,
    background_check_date DATE,
    FOREIGN KEY(tenant_id) REFERENCES Tenant(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS MarketData (
    id INTEGER PRIMARY KEY,
    city TEXT,
    state TEXT,
    property_type TEXT,
    date DATE,
    avg_price_per_sqft REAL,
    vacancy_rate REAL,
    rental_yield REAL,
    appreciation_rate REAL
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Amenity (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS PropertyAmenity (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    amenity_id INTEGER,
    is_available BOOLEAN,
    additional_cost REAL,
    FOREIGN KEY(property_id) REFERENCES Property(id),
    FOREIGN KEY(amenity_id) REFERENCES Amenity(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS LeaseRenewal (
    id INTEGER PRIMARY KEY,
    lease_id INTEGER,
    renewal_date DATE,
    new_rent REAL,
    new_end_date DATE,
    renewal_terms TEXT,
    FOREIGN KEY(lease_id) REFERENCES Lease(id)
)"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS Insurance (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    insurance_type TEXT,
    provider TEXT,
    policy_number TEXT,
    start_date DATE,
    end_date DATE,
    premium_amount REAL,
    coverage_amount REAL,
    FOREIGN KEY(property_id) REFERENCES Property(id)
)"""
)

conn.commit()

# sample data generation using Faker
property_types = [
    "Apartment",
    "Office",
    "Retail",
    "Warehouse",
    "Industrial",
    "Mixed Use",
    "Hotel",
    "Student Housing",
]

# property manager data
manager_categories = ["Residential", "Commercial", "Mixed", "Industrial"]
maintenance_categories = [
    "Plumbing",
    "Electrical",
    "HVAC",
    "Roofing",
    "Painting",
    "Flooring",
    "Security",
    "Landscaping",
    "General Repair",
]
maintenance_priorities = ["Low", "Medium", "High", "Emergency"]
maintenance_statuses = ["Open", "In Progress", "Completed", "Cancelled"]
vendor_categories = [
    "Plumbing",
    "Electrical",
    "HVAC",
    "Construction",
    "Cleaning",
    "Security",
    "Landscaping",
    "Legal",
    "Insurance",
]
expense_categories = [
    "Maintenance",
    "Utilities",
    "Insurance",
    "Property Tax",
    "Management Fee",
    "Legal",
    "Marketing",
    "Supplies",
]
document_types = [
    "Deed",
    "Lease Agreement",
    "Insurance Policy",
    "Inspection Report",
    "Tax Document",
    "Permit",
    "Invoice",
]
inspection_types = [
    "Annual",
    "Move-in",
    "Move-out",
    "Maintenance",
    "Safety",
    "Insurance",
]
inspection_ratings = ["Excellent", "Good", "Fair", "Poor"]
utility_types = ["Electricity", "Gas", "Water", "Sewer", "Internet", "Cable", "Trash"]
employment_statuses = ["Employed", "Self-Employed", "Unemployed", "Student", "Retired"]
amenity_categories = [
    "Recreation",
    "Fitness",
    "Security",
    "Parking",
    "Technology",
    "Convenience",
]

# funds - increased from 10 to 25
for i in range(1, 26):
    name = fake.company() + " Real Estate Fund"
    inception = fake.date_between(start_date="-15y", end_date="-1y")
    manager = fake.name()
    assets = round(random.uniform(50_000_000, 2_000_000_000), 2)  # Increased range
    c.execute(
        "INSERT INTO Fund (id, name, inception_date, manager, total_assets) VALUES (?, ?, ?, ?, ?)",
        (i, name, inception, manager, assets),
    )

# properties - increased from 1000 to 5000
for i in range(1, 5001):
    address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zip_code = fake.zipcode()
    ptype = random.choice(property_types)
    value = round(random.uniform(100_000, 50_000_000), 2)  # Increased range
    fund_id = random.randint(1, 25)  # 25 funds
    c.execute(
        "INSERT INTO Property (id, address, city, state, zip, type, value, fund_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (i, address, city, state, zip_code, ptype, value, fund_id),
    )

# tenants - increased from 500 to 2000
for i in range(1, 2001):
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()
    c.execute(
        "INSERT INTO Tenant (id, name, phone, email) VALUES (?, ?, ?, ?)",
        (i, name, phone, email),
    )

# property managers
for i in range(1, 16):  # 15 property managers
    name = fake.name()
    hire_date = fake.date_between(start_date="-8y", end_date="-1y")
    salary = round(random.uniform(45_000, 120_000), 2)
    email = fake.email()
    phone = fake.phone_number()
    is_active = random.choice([True, True, True, False])  # 75% active
    c.execute(
        "INSERT INTO PropertyManager (id, name, email, phone, hire_date, salary, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (i, name, email, phone, hire_date, salary, is_active),
    )

# property manager assignments
assignment_id = 1
for property_id in range(1, 5001):
    manager_id = random.randint(1, 15)  # 15 property managers
    start_date = fake.date_between(start_date="-5y", end_date="-1m")
    end_date = None
    if random.random() < 0.2:  # 20% have ended assignments
        end_date = fake.date_between(start_date=start_date, end_date="today")

    c.execute(
        "INSERT INTO PropertyManagerAssignment (id, property_id, manager_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
        (
            assignment_id,
            property_id,
            manager_id,
            start_date,
            end_date,
        ),
    )
    assignment_id += 1

# vendors
for i in range(1, 16):  # 15 vendors
    name = fake.company()
    category = random.choice(vendor_categories)
    contact_person = fake.name()
    phone = fake.phone_number()
    email = fake.company_email()
    address = fake.address()
    rating = round(random.uniform(2.5, 5.0), 1)
    is_active = random.choice([True, True, True, False])  # 75% active

    c.execute(
        "INSERT INTO Vendor (id, name, category, contact_person, phone, email, address, rating, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (i, name, category, contact_person, phone, email, address, rating, is_active),
    )

# amenities
amenities_data = [
    ("Swimming Pool", "Recreation", "Outdoor swimming pool with deck area"),
    ("Fitness Center", "Fitness", "Fully equipped gym with modern equipment"),
    ("Parking Garage", "Parking", "Covered parking spaces"),
    ("Security System", "Security", "24/7 surveillance and access control"),
    ("WiFi", "Technology", "High-speed internet access"),
    ("Laundry Facility", "Convenience", "On-site washing and drying machines"),
    ("Rooftop Terrace", "Recreation", "Common outdoor space with city views"),
    ("Conference Room", "Convenience", "Meeting space for residents/tenants"),
    ("Pet Area", "Recreation", "Designated area for pets"),
    ("Storage Units", "Convenience", "Additional storage space"),
]

for i, (name, category, description) in enumerate(amenities_data, 1):
    c.execute(
        "INSERT INTO Amenity (id, name, category, description) VALUES (?, ?, ?, ?)",
        (i, name, category, description),
    )

print("Creating leases and related data...")

# leases - more comprehensive lease generation
lease_id = 1
for property_id in range(1, 5001):
    num_leases = random.randint(1, 4)  # Increased potential leases per property
    for _ in range(num_leases):
        tenant_id = random.randint(1, 2000)  # Updated range for increased tenants
        start = fake.date_between(start_date="-5y", end_date="today")
        end = fake.date_between(start_date=start, end_date="+2y")
        rent = round(random.uniform(1000, 25000), 2)  # Increased range
        deposit = round(rent * random.uniform(0.5, 2), 2)
        c.execute(
            "INSERT INTO Lease (id, property_id, tenant_id, start_date, end_date, rent, deposit) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (lease_id, property_id, tenant_id, start, end, rent, deposit),
        )
        lease_id += 1

# payments
print("Creating payments data...")
payment_id = 1
for lease in c.execute("SELECT id, start_date, end_date, rent FROM Lease"):
    lease_id, start_date, end_date, rent = lease
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # Calculate number of months in the lease
    current_date = start
    while current_date <= end:
        # Add some variability - some late payments, some early
        pay_date = current_date
        if random.random() < 0.05:  # 5% late payments
            pay_date = current_date + timedelta(days=random.randint(1, 15))
        
        amount = rent
        # Sometimes partial payments
        if random.random() < 0.02:  # 2% partial payments
            amount = round(rent * random.uniform(0.3, 0.9), 2)
        
        c.execute(
            "INSERT INTO Payment (id, lease_id, payment_date, amount) VALUES (?, ?, ?, ?)",
            (payment_id, lease_id, pay_date, amount),
        )
        payment_id += 1
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

# maintenance requests
print("Creating maintenance requests...")
request_id = 1
for _ in range(8000):  # Generate 8000 maintenance requests
    property_id = random.randint(1, 5000)
    tenant_id = (
        random.randint(1, 2000) if random.random() < 0.7 else None
    )  # 70% from tenants
    vendor_id = (
        random.randint(1, 15) if random.random() < 0.6 else None
    )  # 60% assigned vendor
    manager_id = random.randint(1, 15)  # 15 property managers
    category = random.choice(maintenance_categories)
    priority = random.choice(maintenance_priorities)
    status = random.choice(maintenance_statuses)

    created_date = fake.date_between(start_date="-5y", end_date="today")
    completed_date = None
    if status == "Completed":
        completed_date = fake.date_between(start_date=created_date, end_date="today")

    estimated_cost = round(random.uniform(50, 5000), 2)
    actual_cost = None
    if status == "Completed":
        actual_cost = round(estimated_cost * random.uniform(0.8, 1.3), 2)

    description = fake.sentence(nb_words=6)

    c.execute(
        """INSERT INTO MaintenanceRequest 
                 (id, property_id, tenant_id, vendor_id, manager_id, category, description, priority, status, 
                  created_date, completed_date, estimated_cost, actual_cost) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            request_id,
            property_id,
            tenant_id,
            vendor_id,
            manager_id,
            category,
            description,
            priority,
            status,
            created_date,
            completed_date,
            estimated_cost,
            actual_cost,
        ),
    )
    request_id += 1

# expenses
print("Creating expenses...")
expense_id = 1
for _ in range(15000):  # Generate 15000 expenses
    property_id = random.randint(1, 5000)
    vendor_id = random.randint(1, 15) if random.random() < 0.8 else None
    category = random.choice(expense_categories)
    amount = round(random.uniform(25, 10000), 2)
    expense_date = fake.date_between(start_date="-5y", end_date="today")
    invoice_number = fake.bothify(text="INV-######")
    is_recurring = random.choice([True, False])

    description = fake.sentence(nb_words=4)

    c.execute(
        """INSERT INTO Expense 
                 (id, property_id, vendor_id, category, description, amount, expense_date, invoice_number, is_recurring) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            expense_id,
            property_id,
            vendor_id,
            category,
            description,
            amount,
            expense_date,
            invoice_number,
            is_recurring,
        ),
    )
    expense_id += 1

# property documents
print("Creating property documents...")
doc_id = 1
for property_id in range(1, 5001):
    num_docs = random.randint(2, 8)  # 2-8 documents per property
    for _ in range(num_docs):
        doc_type = random.choice(document_types)
        doc_name = f"{doc_type.replace(' ', '_')}_{property_id}_{fake.random_int(min=1000, max=9999)}.pdf"
        file_path = f"/documents/property_{property_id}/{doc_name}"
        upload_date = fake.date_between(start_date="-5y", end_date="today")
        expiry_date = None
        if doc_type in ["Insurance Policy", "Permit", "Lease Agreement"]:
            expiry_date = fake.date_between(start_date=upload_date, end_date="+3y")

        c.execute(
            """INSERT INTO PropertyDocument 
                     (id, property_id, document_type, document_name, file_path, upload_date, expiry_date) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                doc_id,
                property_id,
                doc_type,
                doc_name,
                file_path,
                upload_date,
                expiry_date,
            ),
        )
        doc_id += 1

# inspections
print("Creating inspections...")
inspection_id = 1
for _ in range(6000):  # Generate 6000 inspections
    property_id = random.randint(1, 5000)
    inspector_name = fake.name()
    inspection_type = random.choice(inspection_types)
    inspection_date = fake.date_between(start_date="-5y", end_date="today")
    overall_rating = random.choice(inspection_ratings)
    notes = fake.text(max_nb_chars=200)
    next_inspection_date = fake.date_between(start_date=inspection_date, end_date="+1y")

    c.execute(
        """INSERT INTO Inspection 
                 (id, property_id, inspector_name, inspection_type, inspection_date, overall_rating, notes, next_inspection_date) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            inspection_id,
            property_id,
            inspector_name,
            inspection_type,
            inspection_date,
            overall_rating,
            notes,
            next_inspection_date,
        ),
    )
    inspection_id += 1

# utilities
print("Creating utilities...")
utility_id = 1
for property_id in range(1, 5001):
    num_utilities = random.randint(3, 7)  # 3-7 utilities per property
    selected_utilities = random.sample(utility_types, num_utilities)
    for utility_type in selected_utilities:
        provider_names = {
            "Electricity": ["PowerCorp", "ElectricCo", "Energy Plus"],
            "Gas": ["GasCorp", "Natural Gas Co", "Gas Solutions"],
            "Water": ["City Water", "Water Works", "Aqua Services"],
            "Sewer": ["City Sewer", "Waste Management", "Sewer Services"],
            "Internet": ["FastNet", "WebCorp", "ConnectCo"],
            "Cable": ["CableCorp", "TV Plus", "MediaCo"],
            "Trash": ["Waste Corp", "Clean Services", "Garbage Co"],
        }
        provider = random.choice(provider_names.get(utility_type, ["Generic Provider"]))
        account_number = f"{utility_type[:3].upper()}-{random.randint(100000, 999999)}"
        monthly_average = round(random.uniform(25, 500), 2)
        is_tenant_responsibility = random.choice([True, False])

        c.execute(
            """INSERT INTO Utility 
                     (id, property_id, utility_type, provider, account_number, monthly_average, is_tenant_responsibility) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                utility_id,
                property_id,
                utility_type,
                provider,
                account_number,
                monthly_average,
                is_tenant_responsibility,
            ),
        )
        utility_id += 1

# tenant history
print("Creating tenant history...")
for tenant_id in range(1, 2001):
    if random.random() < 0.8:  # 80% of tenants have history
        previous_address = fake.address()
        employment_status = random.choice(employment_statuses)
        annual_income = round(random.uniform(25000, 150000), 2)
        credit_score = random.randint(300, 850)
        references = f"{fake.name()}, {fake.name()}"
        background_check_date = fake.date_between(start_date="-5y", end_date="today")

        c.execute(
            """INSERT INTO TenantHistory 
                     (tenant_id, previous_address, employment_status, annual_income, credit_score, reference_contacts, background_check_date) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                tenant_id,
                previous_address,
                employment_status,
                annual_income,
                credit_score,
                references,
                background_check_date,
            ),
        )

# market data
print("Creating market data...")
market_id = 1
cities_sample = [fake.city() for _ in range(20)]  # Generate 20 cities
for city in cities_sample:
    state = fake.state_abbr()
    for prop_type in property_types:
        for month in range(0, 60, 3):  # 5 years, quarterly data
            date = fake.date_between(start_date="-5y", end_date="today")
            avg_price_per_sqft = round(random.uniform(50, 800), 2)
            vacancy_rate = round(random.uniform(0.02, 0.15), 3)
            rental_yield = round(random.uniform(0.03, 0.12), 3)
            appreciation_rate = round(random.uniform(-0.05, 0.15), 3)

            c.execute(
                """INSERT INTO MarketData 
                         (id, city, state, property_type, date, avg_price_per_sqft, vacancy_rate, rental_yield, appreciation_rate) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    market_id,
                    city,
                    state,
                    prop_type,
                    date,
                    avg_price_per_sqft,
                    vacancy_rate,
                    rental_yield,
                    appreciation_rate,
                ),
            )
            market_id += 1

# property amenities
print("Creating property amenities...")
amenity_id = 1
for property_id in range(1, 5001):
    num_amenities = random.randint(2, 8)  # 2-8 amenities per property
    selected_amenities = random.sample(range(1, 11), num_amenities)  # Amenity IDs 1-10
    for amenity_db_id in selected_amenities:
        is_available = random.choice([True, True, True, False])  # 75% available
        additional_cost = 0
        if random.random() < 0.3:  # 30% have additional cost
            additional_cost = round(random.uniform(10, 200), 2)

        c.execute(
            """INSERT INTO PropertyAmenity 
                     (id, property_id, amenity_id, is_available, additional_cost) 
                     VALUES (?, ?, ?, ?, ?)""",
            (amenity_id, property_id, amenity_db_id, is_available, additional_cost),
        )
        amenity_id += 1

# fund performance - expanded
print("Creating fund performance data...")
performance_id = 1
for fund_id in range(1, 26):  # 25 funds
    for d in range(0, 2190, 7):  # 6 years, weekly data
        date = fake.date_between(start_date="-6y", end_date="today")
        # More realistic NAV progression with some volatility
        base_nav = random.uniform(50_000_000, 2_000_000_000)
        nav = round(base_nav * (1 + random.uniform(-0.1, 0.1)), 2)
        c.execute(
            "INSERT INTO FundPerformance (id, fund_id, date, nav) VALUES (?, ?, ?, ?)",
            (performance_id, fund_id, date, nav),
        )
        performance_id += 1

# lease renewals
print("Creating lease renewals...")
renewal_id = 1
for lease in c.execute(
    'SELECT id, rent, end_date FROM Lease WHERE end_date < date("now")'
):
    lease_id, current_rent, end_date = lease
    if random.random() < 0.6:  # 60% of expired leases get renewed
        # Convert string date to date object
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        renewal_date = fake.date_between(start_date=end_date_obj, end_date="today")
        new_rent = round(current_rent * random.uniform(1.0, 1.15), 2)  # 0-15% increase
        new_end_date = fake.date_between(start_date=renewal_date, end_date="+2y")
        renewal_terms = random.choice(
            [
                "Standard renewal",
                "Early renewal discount",
                "Rent increase applied",
                "Extended term",
            ]
        )

        c.execute(
            """INSERT INTO LeaseRenewal 
                     (id, lease_id, renewal_date, new_rent, new_end_date, renewal_terms) 
                     VALUES (?, ?, ?, ?, ?, ?)""",
            (
                renewal_id,
                lease_id,
                renewal_date,
                new_rent,
                new_end_date,
                renewal_terms,
            ),
        )
        renewal_id += 1

# insurance
print("Creating insurance data...")
insurance_id = 1
for property_id in range(1, 5001):
    num_policies = random.randint(1, 3)  # 1-3 insurance policies per property
    insurance_types = ["Property", "Liability", "Flood", "Earthquake", "Umbrella"]
    for _ in range(num_policies):
        insurance_type = random.choice(insurance_types)
        provider = fake.company()
        policy_number = fake.bothify(text="POL-#######")
        start_date = fake.date_between(start_date="-3y", end_date="today")
        end_date = fake.date_between(start_date=start_date, end_date="+1y")
        premium_amount = round(random.uniform(500, 15000), 2)
        coverage_amount = round(random.uniform(100000, 10000000), 2)

        c.execute(
            """INSERT INTO Insurance 
                     (id, property_id, insurance_type, provider, policy_number, start_date, end_date, premium_amount, coverage_amount) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                insurance_id,
                property_id,
                insurance_type,
                provider,
                policy_number,
                start_date,
                end_date,
                premium_amount,
                coverage_amount,
            ),
        )
        insurance_id += 1

conn.commit()
conn.close()
