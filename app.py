import streamlit as st
import polars as pl
import json, os

st.set_page_config(page_title="Hybrid WMS Dashboard", layout="wide")

DATA_FILE = "out/hybrid_report.json"
HISTORY_FILE = "out/history.csv"
PASSWORD = "admin123"

# -------------------------
# Login
# -------------------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login", key="login_btn") and pwd == PASSWORD:
        st.session_state.auth = True
        st.rerun()
    st.stop()

# -------------------------
# Dashboard
# -------------------------
st.title("🚚 Hybrid WMS Dashboard")

# ✅ Auto-generate data if missing
if not os.path.exists(DATA_FILE):
    st.info("⏳ Generating first report...")
    import run_hybrid_full
    run_hybrid_full.main()

# Load JSON → DataFrame
with open(DATA_FILE) as f:
    data = json.load(f)

df = pl.DataFrame(data)
df = df.with_columns(pl.col("run_time").str.strptime(pl.Datetime))

st.subheader("Latest Run")
st.dataframe(df)

# -------------------------
# History CSV
# -------------------------
if os.path.exists(HISTORY_FILE):
    hist = pl.read_csv(HISTORY_FILE)
else:
    hist = df
    hist.write_csv(HISTORY_FILE)

# -------------------------
# Chart
# -------------------------
st.subheader("📊 Total Issues by OU")
chart_df = df.select(["ou_name", "total_issues"]).to_pandas()
st.bar_chart(chart_df, x="ou_name", y="total_issues")

# -------------------------
# CSV Download
# -------------------------
csv = hist.write_csv()
st.download_button("Download History CSV", csv, "history.csv", "text/csv")
