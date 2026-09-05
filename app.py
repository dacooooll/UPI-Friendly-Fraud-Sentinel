import streamlit as st
import pandas as pd
import subprocess
import os

# Page Configuration
st.set_page_config(
    page_title="Razorpay Sentinel - UPI Risk Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Layer using the MOON Color Palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #210635;
        color: #F5D5E0;
    }

    .stApp {
        background-color: #210635;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .sentinel-header {
        background-color: #420D4B;
        border: 1px solid #6667AB;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .sentinel-title {
        color: #F5D5E0;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .sentinel-subtitle {
        color: #6667AB;
        font-size: 14px;
        margin-top: 4px;
        margin-bottom: 0;
    }

    .metric-card {
        background-color: #420D4B;
        border: 1px solid #6667AB;
        border-radius: 8px;
        padding: 18px;
        text-align: left;
    }

    .metric-label {
        color: #6667AB;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #F5D5E0;
        font-size: 28px;
        font-weight: 700;
        margin-top: 6px;
    }

    .metric-sub {
        font-size: 12px;
        margin-top: 4px;
    }

    .text-emerald { color: #34D399; }
    .text-crimson { color: #F87171; }

    .stButton > button {
        background-color: #7B337E !important;
        color: #F5D5E0 !important;
        border: 1px solid #6667AB !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #6667AB !important;
        border-color: #F5D5E0 !important;
        color: #FFFFFF !important;
    }

    .stTextInput > div > div > input {
        background-color: #420D4B !important;
        color: #F5D5E0 !important;
        border: 1px solid #6667AB !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Evaluated Disputes Dataset
@st.cache_data
def load_data():
    if os.path.exists("evaluated_disputes.csv"):
        return pd.read_csv("evaluated_disputes.csv")
    return None

df = load_data()

# Header Banner
st.markdown("""
<div class="sentinel-header">
    <div class="sentinel-title">🛡️ RAZORPAY SENTINEL</div>
    <div class="sentinel-subtitle">Track 2: AI Risk Manager — First-Party UPI Friendly Fraud Defense System</div>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ `evaluated_disputes.csv` not found. Please run `data_generator.py` and `risk_engine.py` first.")
    st.stop()

# Detect Amount Column Name dynamically
amount_col = None
for candidate in ['amount_inr', 'claim_amount_inr', 'dispute_amount_inr', 'amount', 'dispute_amount']:
    if candidate in df.columns:
        amount_col = candidate
        break

if amount_col is None:
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    amount_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]

# Key Performance Indicators Row
tp = len(df[(df['is_fraud_label'] == 1) & (df['predicted_is_fraud'] == 1)]) if 'is_fraud_label' in df.columns and 'predicted_is_fraud' in df.columns else 0
fp = len(df[(df['is_fraud_label'] == 0) & (df['predicted_is_fraud'] == 1)]) if 'is_fraud_label' in df.columns and 'predicted_is_fraud' in df.columns else 0
fn = len(df[(df['is_fraud_label'] == 1) & (df['predicted_is_fraud'] == 0)]) if 'is_fraud_label' in df.columns and 'predicted_is_fraud' in df.columns else 0

precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0

net_defended = df[df['decision_action'] == 'DEFEND_NPCI_DISPUTE'][amount_col].sum() if 'decision_action' in df.columns else 0
auto_refunded = df[df['decision_action'] == 'AUTO_APPROVE_REFUND'][amount_col].sum() if 'decision_action' in df.columns else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Processed Disputes</div>
        <div class="metric-value">{len(df)}</div>
        <div class="metric-sub text-emerald">● Telemetry Stream Active</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Net Revenue Defended</div>
        <div class="metric-value">₹{net_defended:,.2f}</div>
        <div class="metric-sub text-emerald">🛡️ NPCI Defense Dossiers</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Legitimate Auto-Refunds</div>
        <div class="metric-value">₹{auto_refunded:,.2f}</div>
        <div class="metric-sub text-emerald">⚡ Instant Customer Credit</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Model Precision</div>
        <div class="metric-value">{precision:.1f}%</div>
        <div class="metric-sub text-emerald">Recall: {recall:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Layout: Left Table, Right Inspection Panel
left_col, right_col = st.columns([1.6, 1.0])

with left_col:
    st.markdown("### 📋 Live Dispute Audit Stream")

    search_query = st.text_input("🔍 Search RRN or Transaction ID", "", placeholder="e.g. TXN_UPI_ or 4209")

    display_df = df.copy()
    if search_query:
        display_df = display_df[
            display_df['transaction_id'].str.contains(search_query, case=False, na=False) |
            display_df['upi_rrn'].astype(str).str.contains(search_query, case=False, na=False)
        ] if 'transaction_id' in display_df.columns and 'upi_rrn' in display_df.columns else display_df

    avail_cols = [c for c in ['transaction_id', amount_col, 'risk_score', 'decision_action'] if c in display_df.columns]
    st.dataframe(
        display_df[avail_cols].head(15),
        use_container_width=True,
        hide_index=True,
        height=450
    )

with right_col:
    st.markdown("### 🔍 Case Telemetry Inspector")

    txn_list = display_df['transaction_id'].tolist() if 'transaction_id' in display_df.columns else []
    if txn_list:
        selected_txn = st.selectbox("Select Transaction Record", txn_list)
        row = df[df['transaction_id'] == selected_txn].iloc[0]

        st.markdown(f"""
        **Transaction ID:** `{row.get('transaction_id', 'N/A')}`
        **UPI RRN:** `{row.get('upi_rrn', 'N/A')}`
        **Claim Amount:** `₹{row.get(amount_col, 0):,.2f}`
        **Fraud Risk Score:** `{row.get('risk_score', 'N/A')}`
        **Action Taken:** `{row.get('decision_action', 'N/A')}`

        ---
        **Telemetry Verification:**
        * **Delivery Status:** `{row.get('delivery_status', 'N/A')}`
        * **Item Consumed:** `{'YES (Voucher Redeemed)' if row.get('item_consumed', False) else 'NO'}`
        * **Dispute Claim:** `{row.get('dispute_reason', 'N/A')}`

        ---
        **XAI Decision Explanation:**
        _{row.get('reason_code', 'N/A')}_
        """)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📄 Generate & Inspect Legal PDF Dossier"):
            with st.spinner("Compiling NPCI Defense Dossier..."):
                subprocess.run(["python", "pdf_generator.py"])
                st.success("✅ Legal Dispute Dossier generated!")

            if os.path.exists("sample_dispute_dossier.pdf"):
                with open("sample_dispute_dossier.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Legal Evidence PDF",
                        data=pdf_file,
                        file_name=f"NPCI_Defense_{selected_txn}.pdf",
                        mime="application/pdf"
                    )
