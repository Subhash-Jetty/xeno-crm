import requests
import json
import time
import os

base_url = "https://xeno-backend.onrender.com/api"

def seed_data():
    seed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "seed"))
    
    print("Loading customers...")
    with open(os.path.join(seed_dir, "customers.json")) as f:
        customers = json.load(f)["customers"]

    print("Posting customers...")
    # Send in chunks to avoid payload too large issues
    chunk_size = 500
    for i in range(0, len(customers), chunk_size):
        chunk = customers[i:i+chunk_size]
        res = requests.post(f"{base_url}/customers/ingest", json={"customers": chunk})
        print(f"Customers {i} to {i+len(chunk)}: {res.status_code} {res.text}")
        if res.status_code != 200:
            print("Failed to post customers. Exiting.")
            return

    print("Loading orders...")
    with open(os.path.join(seed_dir, "orders.json")) as f:
        orders = json.load(f)["orders"]

    print("Posting orders...")
    chunk_size = 500
    for i in range(0, len(orders), chunk_size):
        chunk = orders[i:i+chunk_size]
        res = requests.post(f"{base_url}/orders/ingest", json={"orders": chunk})
        print(f"Orders {i} to {i+len(chunk)}: {res.status_code} {res.text}")
        if res.status_code != 200:
            print("Failed to post orders. Exiting.")
            return

if __name__ == "__main__":
    seed_data()
