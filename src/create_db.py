import sqlite3
import random
from datetime import datetime, timedelta
import uuid

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

# sample data generation
fund_names = [f"Real Estate Fund {i}" for i in range(1, 26)]  # Increased to 25 funds
manager_names = [
    "John Smith",
    "Sarah Johnson",
    "Michael Brown",
    "Emma Davis",
    "James Wilson",
    "Lisa Anderson",
    "David Taylor",
    "Jennifer Martinez",
    "Robert Garcia",
    "Maria Rodriguez",
    "Christopher Lee",
    "Amanda White",
    "Daniel Harris",
    "Jessica Clark",
    "Matthew Lewis",
    "Ashley Walker",
    "Anthony Hall",
    "Stephanie Allen",
    "Joshua Young",
    "Nicole King",
]
cities = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Miami",
    "San Francisco",
    "Boston",
    "Seattle",
    "London",
    "Paris",
    "Berlin",
    "Madrid",
    "Rome",
    "Amsterdam",
    "Brussels",
    "Vienna",
    "Tokyo",
    "Osaka",
    "Seoul",
    "Beijing",
    "Shanghai",
    "Hong Kong",
    "Singapore",
    "Bangkok",
    "Sydney",
    "Melbourne",
    "Toronto",
    "Vancouver",
    "Montreal",
    "Calgary",
    "Ottawa",
    "Dubai",
    "Abu Dhabi",
    "Doha",
    "Kuwait City",
    "Riyadh",
    "Tel Aviv",
    "Istanbul",
    "Cape Town",
    "Johannesburg",
    "Moscow",
    "Saint Petersburg",
    "Warsaw",
    "Prague",
    "Mexico City",
    "São Paulo",
    "Buenos Aires",
    "Lima",
    "Santiago",
    "Bogotá",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Jakarta",
    "Kuala Lumpur",
    "Manila",
    "Cairo",
    "Atlanta",
    "Phoenix",
    "Dallas",
    "Philadelphia",
    "Washington DC",
    "Las Vegas",
    "Orlando",
]
states = [
    "NY",
    "CA",
    "IL",
    "TX",
    "FL",
    "WA",
    "MA",
    "GA",
    "AZ",
    "PA",
    "NV",
    "DC",
    "CO",
    "OR",
    "NC",
]
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
street_names = [
    "Main St",
    "Oak Ave",
    "Pine Rd",
    "Elm Dr",
    "Maple Ln",
    "Cedar Blvd",
    "First St",
    "Second Ave",
    "Park Rd",
    "Hill Dr",
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

# increased tenant count
tenant_first_names = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
    "David",
    "Barbara",
    "Richard",
    "Susan",
    "Joseph",
    "Jessica",
    "Thomas",
    "Sarah",
    "Christopher",
    "Karen",
    "Charles",
    "Nancy",
    "Daniel",
    "Lisa",
    "Matthew",
    "Betty",
    "Anthony",
    "Helen",
    "Mark",
    "Sandra",
    "Donald",
    "Donna",
    "Steven",
    "Carol",
    "Paul",
    "Ruth",
    "Andrew",
    "Sharon",
    "Joshua",
    "Michelle",
    "Kenneth",
    "Laura",
    "Kevin",
    "Sarah",
    "Brian",
    "Kimberly",
    "George",
    "Deborah",
    "Timothy",
    "Dorothy",
]
tenant_last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
]

# funds - increased from 10 to 25
for i, name in enumerate(fund_names, 1):
    inception = datetime(2010, 1, 1) + timedelta(days=random.randint(0, 4000))
    manager = random.choice(manager_names)
    assets = round(random.uniform(50_000_000, 2_000_000_000), 2)  # Increased range
    c.execute(
        "INSERT INTO Fund (id, name, inception_date, manager, total_assets) VALUES (?, ?, ?, ?, ?)",
        (i, name, inception.date(), manager, assets),
    )

# properties - increased from 1000 to 5000
for i in range(1, 5001):
    address = f"{random.randint(100,9999)} {random.choice(street_names)}"
    city = random.choice(cities)
    state = random.choice(states)
    zip_code = f"{random.randint(10000,99999)}"
    ptype = random.choice(property_types)
    value = round(random.uniform(100_000, 50_000_000), 2)  # Increased range
    fund_id = random.randint(1, len(fund_names))
    c.execute(
        "INSERT INTO Property (id, address, city, state, zip, type, value, fund_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (i, address, city, state, zip_code, ptype, value, fund_id),
    )

# tenants - increased from 500 to 2000
for i in range(1, 2001):
    first_name = random.choice(tenant_first_names)
    last_name = random.choice(tenant_last_names)
    name = f"{first_name} {last_name}"
    phone = f"({random.randint(100,999)})-{random.randint(100,999)}-{random.randint(1000,9999)}"
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    c.execute(
        "INSERT INTO Tenant (id, name, phone, email) VALUES (?, ?, ?, ?)",
        (i, name, phone, email),
    )

# property managers
property_manager_names = [
    "Alice Cooper",
    "Bob Thompson",
    "Carol Davis",
    "David Wilson",
    "Eva Martinez",
    "Frank Garcia",
    "Grace Brown",
    "Henry Lee",
    "Ivy Johnson",
    "Jack Smith",
    "Kate Anderson",
    "Leo Rodriguez",
    "Maya Patel",
    "Noah Williams",
    "Olivia Jones",
]

for i, name in enumerate(property_manager_names, 1):
    hire_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
    salary = round(random.uniform(45_000, 120_000), 2)
    email = f"{name.lower().replace(' ', '.')}@company.com"
    phone = f"({random.randint(100,999)})-{random.randint(100,999)}-{random.randint(1000,9999)}"
    is_active = random.choice([True, True, True, False])  # 75% active
    c.execute(
        "INSERT INTO PropertyManager (id, name, email, phone, hire_date, salary, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (i, name, email, phone, hire_date.date(), salary, is_active),
    )

# property manager assignments
assignment_id = 1
for property_id in range(1, 5001):
    manager_id = random.randint(1, len(property_manager_names))
    start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
    end_date = None
    if random.random() < 0.2:  # 20% have ended assignments
        end_date = start_date + timedelta(days=random.randint(180, 1000))

    c.execute(
        "INSERT INTO PropertyManagerAssignment (id, property_id, manager_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
        (
            assignment_id,
            property_id,
            manager_id,
            start_date.date(),
            end_date.date() if end_date else None,
        ),
    )
    assignment_id += 1

# vendors
vendor_names = [
    "ABC Plumbing",
    "Quick Fix Electric",
    "Cool Air HVAC",
    "Builder's Best",
    "Clean Pro Services",
    "Secure Guard Systems",
    "Green Lawn Care",
    "Legal Eagles",
    "Safe Insurance Co",
    "Fast Repair LLC",
    "Elite Contractors",
    "Perfect Paint Co",
    "Floor Masters",
    "Roof Experts",
    "Tech Support Plus",
]

for i, name in enumerate(vendor_names, 1):
    category = random.choice(vendor_categories)
    contact_person = (
        f"{random.choice(tenant_first_names)} {random.choice(tenant_last_names)}"
    )
    phone = f"({random.randint(100,999)})-{random.randint(100,999)}-{random.randint(1000,9999)}"
    email = f"contact@{name.lower().replace(' ', '').replace("'", '')}.com"
    address = f"{random.randint(100,9999)} {random.choice(street_names)}, {random.choice(cities)}"
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
        start = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
        end = start + timedelta(days=random.randint(180, 720))
        rent = round(random.uniform(1000, 25000), 2)  # Increased range
        deposit = round(rent * random.uniform(0.5, 2), 2)
        c.execute(
            "INSERT INTO Lease (id, property_id, tenant_id, start_date, end_date, rent, deposit) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (lease_id, property_id, tenant_id, start.date(), end.date(), rent, deposit),
        )
        lease_id += 1

# payments
print("Creating payments data...")
payment_id = 1
for lease in c.execute("SELECT id, start_date, end_date, rent FROM Lease"):
    lease_id, start_date, end_date, rent = lease
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    months = (end.year - start.year) * 12 + (end.month - start.month)
    for m in range(months):
        pay_date = start + timedelta(days=30 * m)
        # Add some variability - some late payments, some early
        if random.random() < 0.05:  # 5% late payments
            pay_date += timedelta(days=random.randint(1, 15))
        amount = rent
        # Sometimes partial payments
        if random.random() < 0.02:  # 2% partial payments
            amount = round(rent * random.uniform(0.3, 0.9), 2)
        c.execute(
            "INSERT INTO Payment (id, lease_id, payment_date, amount) VALUES (?, ?, ?, ?)",
            (payment_id, lease_id, pay_date.date(), amount),
        )
        payment_id += 1

# maintenance requests
print("Creating maintenance requests...")
request_id = 1
for _ in range(8000):  # Generate 8000 maintenance requests
    property_id = random.randint(1, 5000)
    tenant_id = (
        random.randint(1, 2000) if random.random() < 0.7 else None
    )  # 70% from tenants
    vendor_id = (
        random.randint(1, len(vendor_names)) if random.random() < 0.6 else None
    )  # 60% assigned vendor
    manager_id = random.randint(1, len(property_manager_names))
    category = random.choice(maintenance_categories)
    priority = random.choice(maintenance_priorities)
    status = random.choice(maintenance_statuses)

    created_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
    completed_date = None
    if status == "Completed":
        completed_date = created_date + timedelta(days=random.randint(1, 30))

    estimated_cost = round(random.uniform(50, 5000), 2)
    actual_cost = None
    if status == "Completed":
        actual_cost = round(estimated_cost * random.uniform(0.8, 1.3), 2)

    descriptions = [
        f"{category} issue in unit",
        f"Repair needed for {category.lower()}",
        f"Maintenance required - {category.lower()}",
        f"Emergency {category.lower()} problem",
        f"Routine {category.lower()} service",
    ]
    description = random.choice(descriptions)

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
            created_date.date(),
            completed_date.date() if completed_date else None,
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
    vendor_id = random.randint(1, len(vendor_names)) if random.random() < 0.8 else None
    category = random.choice(expense_categories)
    amount = round(random.uniform(25, 10000), 2)
    expense_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
    invoice_number = f"INV-{random.randint(100000, 999999)}"
    is_recurring = random.choice([True, False])

    descriptions = [
        f"{category} expense",
        f"Monthly {category.lower()}",
        f"Annual {category.lower()}",
        f"Emergency {category.lower()}",
        f"Routine {category.lower()}",
    ]
    description = random.choice(descriptions)

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
            expense_date.date(),
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
        doc_name = f"{doc_type.replace(' ', '_')}_{property_id}_{random.randint(1000, 9999)}.pdf"
        file_path = f"/documents/property_{property_id}/{doc_name}"
        upload_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
        expiry_date = None
        if doc_type in ["Insurance Policy", "Permit", "Lease Agreement"]:
            expiry_date = upload_date + timedelta(
                days=random.randint(365, 1095)
            )  # 1-3 years

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
                upload_date.date(),
                expiry_date.date() if expiry_date else None,
            ),
        )
        doc_id += 1

# inspections
print("Creating inspections...")
inspection_id = 1
for _ in range(6000):  # Generate 6000 inspections
    property_id = random.randint(1, 5000)
    inspector_name = (
        f"{random.choice(tenant_first_names)} {random.choice(tenant_last_names)}"
    )
    inspection_type = random.choice(inspection_types)
    inspection_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
    overall_rating = random.choice(inspection_ratings)
    notes = f"{inspection_type} inspection completed. Overall condition: {overall_rating.lower()}."
    next_inspection_date = inspection_date + timedelta(days=random.randint(180, 365))

    c.execute(
        """INSERT INTO Inspection 
                 (id, property_id, inspector_name, inspection_type, inspection_date, overall_rating, notes, next_inspection_date) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            inspection_id,
            property_id,
            inspector_name,
            inspection_type,
            inspection_date.date(),
            overall_rating,
            notes,
            next_inspection_date.date(),
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
        previous_address = f"{random.randint(100,9999)} {random.choice(street_names)}, {random.choice(cities)}"
        employment_status = random.choice(employment_statuses)
        annual_income = round(random.uniform(25000, 150000), 2)
        credit_score = random.randint(300, 850)
        references = f"{random.choice(tenant_first_names)} {random.choice(tenant_last_names)}, {random.choice(tenant_first_names)} {random.choice(tenant_last_names)}"
        background_check_date = datetime(2020, 1, 1) + timedelta(
            days=random.randint(0, 1800)
        )

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
                background_check_date.date(),
            ),
        )

# market data
print("Creating market data...")
market_id = 1
for city in cities[:20]:  # Use first 20 cities
    state = random.choice(states)
    for prop_type in property_types:
        for month in range(0, 60, 3):  # 5 years, quarterly data
            date = datetime(2020, 1, 1) + timedelta(days=month * 30)
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
                    date.date(),
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
for fund_id in range(1, len(fund_names) + 1):
    for d in range(0, 2190, 7):  # 6 years, weekly data
        date = datetime(2019, 1, 1) + timedelta(days=d)
        # More realistic NAV progression with some volatility
        base_nav = random.uniform(50_000_000, 2_000_000_000)
        nav = round(base_nav * (1 + random.uniform(-0.1, 0.1)), 2)
        c.execute(
            "INSERT INTO FundPerformance (id, fund_id, date, nav) VALUES (?, ?, ?, ?)",
            (performance_id, fund_id, date.date(), nav),
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
        renewal_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=random.randint(-30, 30)
        )
        new_rent = round(current_rent * random.uniform(1.0, 1.15), 2)  # 0-15% increase
        new_end_date = renewal_date + timedelta(
            days=random.randint(365, 730)
        )  # 1-2 years
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
                renewal_date.date(),
                new_rent,
                new_end_date.date(),
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
        providers = [
            "SafeGuard Insurance",
            "Reliable Coverage",
            "Premium Protect",
            "SecureShield",
            "TrustCorp Insurance",
        ]
        provider = random.choice(providers)
        policy_number = f"POL-{random.randint(1000000, 9999999)}"
        start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1095))
        end_date = start_date + timedelta(days=365)  # 1 year policies
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
                start_date.date(),
                end_date.date(),
                premium_amount,
                coverage_amount,
            ),
        )
        insurance_id += 1

conn.commit()
conn.close()
