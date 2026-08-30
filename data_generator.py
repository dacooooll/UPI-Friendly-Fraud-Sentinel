import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_upi_dataset(num_records=500):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    base_time = datetime.now() - timedelta(days=30)
    
    for i in range(1, num_records + 1):
        txn_id = f"TXN_{100000 + i}"
        upi_rrn = f"{random.randint(400000000000, 499999999999)}"
        amount = round(random.uniform(100, 15000), 2)
        txn_time = base_time + timedelta(minutes=random.randint(1, 43200))
        
        # Scenario split: 60% Legitimate, 25% Friendly Fraud, 15% System Failure
        scenario_type = np.random.choice(
            ["Legitimate_Delivered", "Friendly_Fraud", "System_Failure"], 
            p=[0.60, 0.25, 0.15]
        )
        
        if scenario_type == "Legitimate_Delivered":
            delivery_status = "DELIVERED"
            item_consumed = True
            delivery_delay_sec = random.randint(1, 15)
            claim_filed = False
            dispute_reason = "NONE"
            is_fraud = 0
            
        elif scenario_type == "Friendly_Fraud":
            delivery_status = "DELIVERED"
            item_consumed = True  # Voucher/Product was used, but customer lied to bank
            delivery_delay_sec = random.randint(1, 30)
            claim_filed = True
            dispute_reason = "PAID_BUT_NOT_RECEIVED"
            is_fraud = 1
            
        else: # True System_Failure
            delivery_status = "FAILED"
            item_consumed = False
            delivery_delay_sec = 0
            claim_filed = True
            dispute_reason = "PAID_BUT_NOT_RECEIVED"
            is_fraud = 0

        data.append({
            "transaction_id": txn_id,
            "upi_rrn": upi_rrn,
            "amount_inr": amount,
            "timestamp": txn_time.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_status": delivery_status,
            "item_consumed": item_consumed,
            "delivery_delay_sec": delivery_delay_sec,
            "claim_filed": claim_filed,
            "dispute_reason": dispute_reason,
            "is_fraud_label": is_fraud
        })
        
    df = pd.DataFrame(data)
    df.to_csv("upi_disputes.csv", index=False)
    print(f"✅ Created synthetic dataset with {num_records} records -> upi_disputes.csv")

if __name__ == "__main__":
    generate_upi_dataset()
