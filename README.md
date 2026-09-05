# 🛡️ UPI Friendly Fraud Sentinel

An automated FinTech risk engine built for **Razorpay AI Buildathon (Track 2: AI Risk Manager)**. It detects, evaluates, and auto-defends against **UPI First-Party Friendly Fraud** where buyers redeem digital products/vouchers and submit false "Payment Deducted but Order Failed" chargeback claims to acquiring banks.

## 🚀 Key Features

1. **Deterministic Telemetry Verification Engine:** Cross-references UPI Retrieval Reference Numbers (RRN), delivery execution logs, and item consumption webhooks.
2. **AI Evidence & XAI Reasoner:** Calculates risk scores (0.00 to 1.00) and produces human-readable explainable reason codes.
3. **Automated NPCI Legal Dispute Bundle:** Generates formatted PDF evidence dossiers containing merchant telemetry, delivery signatures, and defense statements.
4. **False Positive Cost Mitigation:** Automatically approves refunds for genuine system timeouts while gating high-risk disputes.

## 📊 Benchmark & Business Impact Performance

Evaluating on 500 simulated UPI dispute events:

- **Precision:** 98.3%
- **Recall:** 92.7%
- **F1-Score:** 0.9544
- **Net Revenue Defended:** ₹809,276.66
- **Legitimate Auto-Refunds:** ₹672,500.30

## 📂 Project Structure

- `data_generator.py` - Generates synthetic UPI dispute benchmarks (`upi_disputes.csv`).
- `risk_engine.py` - Evaluates claims and produces risk actions (`evaluated_disputes.csv`).
- `pdf_generator.py` - Builds printable PDF legal dispute dossiers (`sample_dispute_dossier.pdf`).
- `metrics.py` - Computes Precision, Recall, F1-score, and net revenue impact metrics.

## 🏃 Quickstart Guide

1. Clone repository: `git clone https://github.com/dacooooll/UPI-Friendly-Fraud-Sentinel.git`
2. Install dependencies: `pip install fpdf2 pandas numpy`
3. Execute pipeline: `python data_generator.py && python risk_engine.py && python pdf_generator.py && python metrics.py`
