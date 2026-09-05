import pandas as pd
import numpy as np

def compute_system_metrics(input_file="evaluated_disputes.csv"):
    print(f"📊 Calculating performance and financial metrics from {input_file}...")
    df = pd.read_csv(input_file)

    y_true = df['is_fraud_label']
    y_pred = df['predicted_is_fraud']

    # Calculate Precision, Recall, F1
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tn = np.sum((y_true == 0) & (y_pred == 0))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Financial Impact Calculations
    defended_df = df[df['decision_action'] == 'DEFEND_NPCI_DISPUTE']
    total_defended_inr = defended_df['amount_inr'].sum()

    refunded_df = df[df['decision_action'] == 'AUTO_APPROVE_REFUND']
    total_refunded_inr = refunded_df['amount_inr'].sum()

    print("\n" + "="*50)
    print("      RAZORPAY SENTINEL - EVALUATION METRICS")
    print("="*50)
    print(f"  • Total Processed Disputes : {len(df)}")
    print(f"  • True Positives (Fraud)  : {tp}")
    print(f"  • True Negatives (Valid)  : {tn}")
    print(f"  • False Positives         : {fp}")
    print(f"  • False Negatives         : {fn}")
    print("-" * 50)
    print(f"  📈 Precision              : {precision:.4f} ({precision*100:.1f}%)")
    print(f"  📈 Recall                 : {recall:.4f} ({recall*100:.1f}%)")
    print(f"  📈 F1-Score               : {f1_score:.4f}")
    print("-" * 50)
    print(f"  💰 Net Revenue Defended   : ₹{total_defended_inr:,.2f}")
    print(f"  💳 Legitimate Auto-Refunds : ₹{total_refunded_inr:,.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    compute_system_metrics()
