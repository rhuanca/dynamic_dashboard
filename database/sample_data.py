"""
Generate realistic sample equipment data for demo purposes.

Creates 2000 equipment items across 6 categories with realistic business data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple
from database.db_manager import db_manager


# Equipment categories and their typical items
EQUIPMENT_DATA = {
    "IT Equipment": {
        "items": [
            ("Dell Latitude Laptop", "Dell", "Latitude 5520"),
            ("HP EliteBook Laptop", "HP", "EliteBook 840 G8"),
            ("Lenovo ThinkPad Laptop", "Lenovo", "ThinkPad X1 Carbon"),
            ("Apple MacBook Pro", "Apple", "MacBook Pro 16\""),
            ("Dell UltraSharp Monitor", "Dell", "U2720Q"),
            ("HP LaserJet Printer", "HP", "LaserJet Pro M404n"),
            ("Cisco Network Switch", "Cisco", "Catalyst 2960"),
            ("Dell PowerEdge Server", "Dell", "PowerEdge R740"),
            ("APC UPS Battery Backup", "APC", "Smart-UPS 1500VA"),
            ("Logitech Webcam", "Logitech", "Brio 4K"),
        ],
        "price_range": (300, 5000),
        "depreciation": 0.20
    },
    "Manufacturing Equipment": {
        "items": [
            ("CNC Milling Machine", "Haas", "VF-2"),
            ("Industrial Lathe", "Mazak", "Quick Turn 250"),
            ("Welding Machine", "Miller", "Syncrowave 250"),
            ("Hydraulic Press", "Greenerd", "H-50"),
            ("Air Compressor", "Atlas Copco", "GA 30"),
            ("Plasma Cutter", "Hypertherm", "Powermax 45"),
            ("Drill Press", "JET", "JDP-20MF"),
            ("Band Saw", "DoALL", "C-916A"),
            ("Grinder", "Baldor", "8\" Bench Grinder"),
            ("Forklift", "Toyota", "8FGU25"),
        ],
        "price_range": (2000, 150000),
        "depreciation": 0.10
    },
    "Office Equipment": {
        "items": [
            ("Ergonomic Office Chair", "Herman Miller", "Aeron"),
            ("Standing Desk", "Uplift", "V2"),
            ("Conference Table", "HON", "Preside 10ft"),
            ("Projector", "Epson", "PowerLite 1795F"),
            ("Whiteboard", "Quartet", "Prestige 2 6x4"),
            ("Paper Shredder", "Fellowes", "Powershred 99Ci"),
            ("Filing Cabinet", "HON", "4-Drawer Lateral"),
            ("Coffee Maker", "Bunn", "VPR Series"),
            ("Water Cooler", "Avalon", "A5"),
            ("Telephone System", "Cisco", "IP Phone 8861"),
        ],
        "price_range": (100, 3000),
        "depreciation": 0.15
    },
    "Medical Devices": {
        "items": [
            ("Patient Monitor", "Philips", "IntelliVue MX450"),
            ("Ultrasound Machine", "GE", "LOGIQ E9"),
            ("Defibrillator", "Zoll", "X Series"),
            ("Infusion Pump", "Baxter", "Sigma Spectrum"),
            ("ECG Machine", "Philips", "PageWriter TC70"),
            ("Surgical Light", "Stryker", "LED 3"),
            ("Examination Table", "Midmark", "Ritter 204"),
            ("Autoclave Sterilizer", "Tuttnauer", "EZ10"),
            ("Vital Signs Monitor", "Welch Allyn", "Connex VSM"),
            ("Wheelchair", "Invacare", "Tracer EX2"),
        ],
        "price_range": (500, 80000),
        "depreciation": 0.12
    },
    "Vehicles": {
        "items": [
            ("Delivery Van", "Ford", "Transit 250"),
            ("Pickup Truck", "Chevrolet", "Silverado 1500"),
            ("Company Sedan", "Toyota", "Camry"),
            ("SUV", "Honda", "CR-V"),
            ("Box Truck", "Isuzu", "NPR"),
            ("Service Van", "Mercedes-Benz", "Sprinter"),
            ("Cargo Van", "Ram", "ProMaster 1500"),
            ("Utility Vehicle", "John Deere", "Gator XUV"),
            ("Flatbed Truck", "Ford", "F-450"),
            ("Electric Vehicle", "Tesla", "Model 3"),
        ],
        "price_range": (25000, 75000),
        "depreciation": 0.18
    },
    "Tools": {
        "items": [
            ("Cordless Drill", "DeWalt", "DCD771C2"),
            ("Impact Driver", "Milwaukee", "M18 Fuel"),
            ("Circular Saw", "Makita", "5007MG"),
            ("Angle Grinder", "Bosch", "GWS13-50VS"),
            ("Reciprocating Saw", "Milwaukee", "Sawzall"),
            ("Nail Gun", "Bostitch", "F21PL"),
            ("Tool Chest", "Snap-on", "KRA2422"),
            ("Multimeter", "Fluke", "87V"),
            ("Torque Wrench", "Craftsman", "1/2 Drive"),
            ("Ladder", "Werner", "6ft Fiberglass"),
        ],
        "price_range": (50, 5000),
        "depreciation": 0.25
    }
}

# Departments
DEPARTMENTS = [
    "IT", "Engineering", "Manufacturing", "Operations", 
    "Facilities", "Medical", "Logistics", "Maintenance",
    "Research & Development", "Quality Assurance"
]

# Locations
LOCATIONS = [
    "Building A - Floor 1", "Building A - Floor 2", "Building A - Floor 3",
    "Building B - Floor 1", "Building B - Floor 2", 
    "Warehouse", "Production Floor", "Lab", "Office Area", "Storage Room"
]

# Status values
STATUSES = ["Active", "In Maintenance", "Out of Service", "Retired", "On Loan"]
STATUS_WEIGHTS = [70, 15, 5, 5, 5]  # Weighted probability

# Condition values
CONDITIONS = ["Excellent", "Good", "Fair", "Poor", "Needs Repair"]
CONDITION_WEIGHTS = [20, 50, 20, 7, 3]

# Employee names for assignment
EMPLOYEES = [
    "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis",
    "David Wilson", "Jennifer Martinez", "Robert Taylor", "Lisa Anderson",
    "James Thomas", "Mary Jackson", "William White", "Patricia Harris",
    "Richard Martin", "Linda Thompson", "Joseph Garcia", "Barbara Rodriguez"
]


def generate_serial_number() -> str:
    """Generate a realistic serial number."""
    return f"SN{random.randint(100000, 999999)}"


def generate_asset_tag(index: int) -> str:
    """Generate a unique asset tag."""
    return f"AST-{index:06d}"


def calculate_current_value(
    purchase_price: float,
    purchase_date: datetime,
    depreciation_rate: float
) -> float:
    """Calculate current value based on depreciation."""
    years_old = (datetime.now() - purchase_date).days / 365.25
    depreciation = purchase_price * depreciation_rate * years_old
    current_value = max(purchase_price - depreciation, purchase_price * 0.1)
    return round(current_value, 2)


def generate_maintenance_dates(
    purchase_date: datetime,
    status: str
) -> Tuple[datetime, datetime, int]:
    """Generate maintenance dates based on equipment age and status."""
    # Maintenance interval in days (90-365 days)
    interval = random.randint(90, 365)
    
    # Last maintenance: sometime between purchase and now
    days_since_purchase = (datetime.now() - purchase_date).days
    if days_since_purchase > 0:
        last_maintenance_days_ago = random.randint(0, min(days_since_purchase, 180))
        last_maintenance = datetime.now() - timedelta(days=last_maintenance_days_ago)
    else:
        last_maintenance = purchase_date
    
    # Next maintenance
    if status == "Out of Service" or status == "Retired":
        next_maintenance = None
    else:
        next_maintenance = last_maintenance + timedelta(days=interval)
    
    return last_maintenance, next_maintenance, interval


def generate_equipment_records(count: int = 2000) -> List[Tuple]:
    """Generate realistic equipment records.
    
    Args:
        count: Number of equipment items to generate
        
    Returns:
        List of tuples ready for database insertion
    """
    records = []
    items_per_category = count // len(EQUIPMENT_DATA)
    
    record_index = 1
    
    for category, cat_data in EQUIPMENT_DATA.items():
        items = cat_data["items"]
        price_min, price_max = cat_data["price_range"]
        depreciation_rate = cat_data["depreciation"]
        
        for _ in range(items_per_category):
            # Select random item from category
            name, manufacturer, model = random.choice(items)
            
            # Generate dates
            days_ago = random.randint(30, 1825)  # 1 month to 5 years old
            purchase_date = datetime.now() - timedelta(days=days_ago)
            
            # Financial data
            purchase_price = round(random.uniform(price_min, price_max), 2)
            current_value = calculate_current_value(
                purchase_price, purchase_date, depreciation_rate
            )
            
            # Location and assignment
            department = random.choice(DEPARTMENTS)
            location = random.choice(LOCATIONS)
            assigned_to = random.choice(EMPLOYEES + [None, None])  # Some unassigned
            
            # Status and condition
            status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
            condition = random.choices(CONDITIONS, weights=CONDITION_WEIGHTS)[0]
            
            # Maintenance dates
            last_maint, next_maint, interval = generate_maintenance_dates(
                purchase_date, status
            )
            
            # Warranty (1-3 years from purchase)
            warranty_years = random.choice([1, 2, 3])
            warranty_expiry = purchase_date + timedelta(days=365 * warranty_years)
            
            # Create record tuple
            record = (
                generate_asset_tag(record_index),  # asset_tag
                name,  # name
                category,  # category
                manufacturer,  # manufacturer
                model,  # model_number
                generate_serial_number(),  # serial_number
                purchase_date.date(),  # purchase_date
                purchase_price,  # purchase_price
                current_value,  # current_value
                depreciation_rate,  # depreciation_rate
                department,  # department
                location,  # location
                assigned_to,  # assigned_to
                status,  # status
                condition,  # condition
                last_maint.date() if last_maint else None,  # last_maintenance_date
                next_maint.date() if next_maint else None,  # next_maintenance_date
                interval,  # maintenance_interval_days
                warranty_expiry.date(),  # warranty_expiry_date
                None  # notes
            )
            
            records.append(record)
            record_index += 1
    
    return records


def populate_database(count: int = 2000) -> None:
    """Generate and insert sample equipment data into database.
    
    Args:
        count: Number of equipment items to generate
    """
    print(f"Generating {count} equipment records...")
    records = generate_equipment_records(count)
    
    insert_query = """
        INSERT INTO equipment (
            asset_tag, name, category, manufacturer, model_number, serial_number,
            purchase_date, purchase_price, current_value, depreciation_rate,
            department, location, assigned_to, status, condition,
            last_maintenance_date, next_maintenance_date, maintenance_interval_days,
            warranty_expiry_date, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    print("Inserting records into database...")
    affected = db_manager.execute_many(insert_query, records)
    print(f"✓ Successfully inserted {affected} equipment records")
    
    # Print summary statistics
    print("\n=== Database Summary ===")
    print(f"Total Equipment: {db_manager.get_equipment_count()}")
    print(f"Total Value: ${db_manager.get_total_equipment_value():,.2f}")
    print("\nEquipment by Department:")
    for dept in db_manager.get_equipment_by_department():
        print(f"  {dept['department']}: {dept['count']}")


if __name__ == "__main__":
    # Initialize database and populate with sample data
    db_manager.initialize_database()
    populate_database(2000)
