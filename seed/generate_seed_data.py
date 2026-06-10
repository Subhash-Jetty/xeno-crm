import json
import random
from datetime import datetime, timedelta
import uuid

# Configuration
NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000

# Data pools
FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Ayaan", "Krishna", "Ishaan", "Shaurya",
               "Diya", "Isha", "Riya", "Aanya", "Aadhya", "Navya", "Kavya", "Myra", "Saanvi", "Kiara",
               "John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", "Alexander", "Isabella"]
LAST_NAMES = ["Sharma", "Singh", "Kumar", "Patel", "Gupta", "Reddy", "Rao", "Jain", "Das", "Shah",
              "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "company.com"]

PRODUCTS = [
    {"name": "Espresso Blend", "price": 12.50},
    {"name": "Colombian Single Origin", "price": 15.00},
    {"name": "French Roast", "price": 13.00},
    {"name": "Cold Brew Maker", "price": 35.00},
    {"name": "Ceramic Mug", "price": 18.00},
    {"name": "Coffee Grinder", "price": 45.00},
    {"name": "Caramel Syrup", "price": 9.50},
    {"name": "Subscription - 1 Month", "price": 25.00},
]

CHANNELS = ["online", "in-store", "app"]

# Generate Customers
customers = []
for _ in range(NUM_CUSTOMERS):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(DOMAINS)}"
    phone = f"+9198{random.randint(10000000, 99999999)}"
    
    tags = []
    if random.random() < 0.2:
        tags.append("vip")
    if random.random() < 0.3:
        tags.append("newsletter_subscriber")
    if random.random() < 0.1:
        tags.append("wholesale")
        
    customers.append({
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "phone": phone,
        "tags": tags
    })

# Generate Orders
orders = []
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=365)  # Orders over the last year

for _ in range(NUM_ORDERS):
    customer = random.choice(customers)
    
    # Skew dates so some customers are recent and some are old
    days_ago = int(random.triangular(0, 365, 30))
    created_at = end_date - timedelta(days=days_ago)
    
    # Select items
    num_items = random.randint(1, 4)
    items = []
    amount = 0
    for _ in range(num_items):
        prod = random.choice(PRODUCTS)
        qty = random.randint(1, 3)
        item_total = prod["price"] * qty
        items.append({
            "name": prod["name"],
            "quantity": qty,
            "price": prod["price"]
        })
        amount += item_total
        
    orders.append({
        "id": str(uuid.uuid4()),
        "customer_id": customer["id"],
        "customer_email": customer["email"], # Useful for ingestion fallback
        "order_number": f"ORD-{random.randint(10000, 99999)}",
        "amount": round(amount, 2),
        "items": items,
        "channel": random.choice(CHANNELS),
        "status": "completed" if random.random() < 0.95 else "refunded",
        "created_at": created_at.isoformat()
    })

# Save to JSON files
with open("customers.json", "w") as f:
    json.dump({"customers": customers}, f, indent=2)

with open("orders.json", "w") as f:
    json.dump({"orders": orders}, f, indent=2)

print(f"Generated {len(customers)} customers and {len(orders)} orders.")
print("Saved to customers.json and orders.json")
