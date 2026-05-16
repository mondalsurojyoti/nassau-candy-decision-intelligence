
import streamlit as st
import pandas as pd

from data_prep import load_and_prep_data
from model import train_lead_time_model
from optimizer import simulate_reallocation, compute_kpis
from config import PRODUCT_MAPPING, DIVISION_MAP, KPI_DEFINITIONS

st.set_page_config(
    page_title="Nassau Candy — Decision Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PROFESSIONAL STYLING ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global */
html, body, .main, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding: 1.8rem 2rem 2rem 2rem; max-width: 1400px; }
h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; }

/* Header bar */
.hero-bar {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-bar h1 { color: #f8fafc; font-size: 1.6rem; margin: 0; font-weight: 800; letter-spacing: -0.5px; }
.hero-bar p  { color: #94a3b8; font-size: 0.85rem; margin: 0.25rem 0 0 0; }
.hero-badge {
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    padding: 6px 16px;
    border-radius: 24px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Section headers */
.sec-head {
    font-size: 1.05rem; font-weight: 700; color: #0f172a;
    margin: 0 0 0.6rem 0; padding-bottom: 0.45rem;
    border-bottom: 2px solid #6366f1;
    display: flex; align-items: center; gap: 8px;
}

/* KPI strip */
.kpi-strip { display: flex; gap: 14px; margin-bottom: 1.2rem; }
.kpi-item {
    flex: 1;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 14px;
    padding: 1.1rem 1rem;
    text-align: center;
    color: #fff;
    box-shadow: 0 6px 20px rgba(99,102,241,0.25);
    transition: transform 0.2s;
}
.kpi-item:hover { transform: translateY(-3px); }
.kpi-val  { font-size: 1.75rem; font-weight: 800; margin: 0; line-height: 1.1; }
.kpi-name { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.6px; opacity: 0.92; margin: 4px 0 0 0; }
.kpi-sub  { font-size: 0.65rem; opacity: 0.65; margin-top: 2px; }

/* Card containers */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] label { color: #94a3b8 !important; font-weight: 500; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1e293b; border-color: #334155;
}

/* Table polish */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Metric tweaks */
[data-testid="stMetric"] {
    background: #f8fafc; border-radius: 10px; padding: 0.8rem; border: 1px solid #e2e8f0;
}

/* Divider override */
hr { border-color: #e2e8f0 !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── INIT ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def initialize_system():
    df = load_and_prep_data("Nassau Candy Distributor.csv")
    if df is not None:
        model, metrics = train_lead_time_model(df)
        return df, model, metrics
    return None, None, None

df, model, metrics = initialize_system()

# ── HERO HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-bar">
    <div>
        <h1>🏭 Nassau Candy — Decision Intelligence</h1>
        <p>Factory Reallocation & Shipping Optimization Dashboard</p>
    </div>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ Dataset 'Nassau Candy Distributor.csv' not found.")
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Controls")

products = list(PRODUCT_MAPPING.keys())
selected_product = st.sidebar.selectbox("Product", products)
division = DIVISION_MAP.get(selected_product, "Other")

regions = sorted(df['Region'].unique())
selected_region = st.sidebar.selectbox("Region", regions)

ship_modes = sorted(df['Ship Mode'].unique())
selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_modes)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🎯 Priority")
speed_priority = st.sidebar.slider(
    "Speed ↔ Profit", min_value=0.0, max_value=1.0, value=0.5, step=0.05,
    help="0 = Profit Focus | 1 = Speed Focus"
)
label = "⚡ Speed" if speed_priority > 0.6 else ("💰 Profit" if speed_priority < 0.4 else "⚖️ Balanced")
st.sidebar.info(f"Mode: **{label}**")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📊 Model Metrics")
m1, m2 = st.sidebar.columns(2)
m1.metric("R²", f"{metrics['R2']:.3f}")
m2.metric("MAE", f"{metrics['MAE']:.1f}d")
st.sidebar.metric("RMSE", f"{metrics['RMSE']:.1f} days")
st.sidebar.caption(f"Train {metrics['train_size']} · Test {metrics['test_size']}")

# ── KPIs ──────────────────────────────────────────────────────────────────────
@st.cache_data
def get_kpis(_model, prods, regs, modes):
    return compute_kpis(df, _model, prods, regs, modes)

with st.spinner("Computing KPIs..."):
    kpis = get_kpis(model, products, regions, ship_modes)

items = [
    (f"{kpis['Lead Time Reduction (%)']:.1f}%", "Lead Time Reduction", "Operational Gain"),
    (f"{kpis['Profit Impact Stability']:.1f}%", "Profit Stability", "Financial Safety"),
    (f"{kpis['Scenario Confidence Score']:.1f}%", "Confidence Score", "Reliability"),
    (f"{kpis['Recommendation Coverage']:.1f}%", "Reco. Coverage", "Scalability"),
]

html = '<div class="kpi-strip">'
for val, name, sub in items:
    html += f'<div class="kpi-item"><p class="kpi-val">{val}</p><p class="kpi-name">{name}</p><p class="kpi-sub">{sub}</p></div>'
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

# ── SIMULATION ────────────────────────────────────────────────────────────────
sim = simulate_reallocation(model, selected_product, division, selected_region, selected_ship_mode, speed_priority)

cur_row = sim[sim['Is Current']]
if not cur_row.empty:
    cur_factory = cur_row['Factory'].values[0]
    cur_lt = cur_row['Predicted Lead Time (Days)'].values[0]
else:
    cur_factory = PRODUCT_MAPPING.get(selected_product, "Unknown")
    cur_lt = sim['Predicted Lead Time (Days)'].median()

best = sim.iloc[0]

# ── ROW 1: SIMULATOR + WHAT-IF ───────────────────────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<p class="sec-head">🏭 Factory Optimization Simulator</p>', unsafe_allow_html=True)
    st.markdown(f"**{selected_product}** → **{selected_region}** via **{selected_ship_mode}**")
    st.info(f"📍 Current: **{cur_factory}**  ·  Est. **{cur_lt:.1f}** Days")

    tbl = sim[['Factory','Predicted Lead Time (Days)','Margin Impact (%)','Distance (km)','Composite Score']].copy()
    tbl.insert(0, 'Rank', range(1, len(tbl)+1))
    tbl = tbl.reset_index(drop=True)

    styled = tbl.style.highlight_min(
        subset=['Predicted Lead Time (Days)'], color='#dcfce7'
    ).highlight_max(
        subset=['Composite Score'], color='#dbeafe'
    ).format({
        'Predicted Lead Time (Days)': '{:.1f}',
        'Margin Impact (%)': '{:+.2f}',
        'Distance (km)': '{:.0f}',
        'Composite Score': '{:.2f}'
    })
    st.dataframe(styled, width='stretch', hide_index=True)

with c2:
    st.markdown('<p class="sec-head">🔄 What-If Analysis</p>', unsafe_allow_html=True)

    if best['Factory'] == cur_factory:
        st.success("✅ Current factory is **already optimal** for this route.")
        st.metric("Current Lead Time", f"{cur_lt:.1f} Days")
    else:
        st.warning("⚠️ **Reallocation Recommended**")
        dt = cur_lt - best['Predicted Lead Time (Days)']
        pct = (dt / cur_lt * 100) if cur_lt > 0 else 0

        mc1, mc2 = st.columns(2)
        mc1.metric("Time Saved", f"{dt:.1f}d", delta=f"-{dt:.1f}d", delta_color="inverse")
        mc2.metric("Reduction", f"{pct:.1f}%")
        st.metric("Margin Impact", f"{best['Margin Impact (%)']:+.2f}%", delta=f"{best['Margin Impact (%)']:+.2f}%")

    st.markdown("**Lead Time Comparison**")
    chart = sim[['Factory','Predicted Lead Time (Days)']].set_index('Factory')
    st.bar_chart(chart, color="#6366f1")

# ── ROW 2: RECOMMENDATIONS + RISK ────────────────────────────────────────────
st.markdown("---")
c3, c4 = st.columns(2)

with c3:
    st.markdown('<p class="sec-head">📋 Recommendation Dashboard</p>', unsafe_allow_html=True)

    if best['Factory'] != cur_factory:
        st.success(f"**🔁 Action:** Move **{selected_product}** ({selected_region}) → **{best['Factory']}**")

        dt = cur_lt - best['Predicted Lead Time (Days)']
        dd = (cur_row['Distance (km)'].values[0] if not cur_row.empty else 0) - best['Distance (km)']
        g1, g2 = st.columns(2)
        g1.metric("⏱️ Time Saved", f"{dt:.1f}d")
        g2.metric("📏 Distance Δ", f"{dd:+.0f} km")

        st.caption("Leverages machine learning to minimise geographic drag while balancing freight costs.")
        st.markdown("**Ranked Alternatives**")
        for i, (_, r) in enumerate(sim.iterrows()):
            medal = ["🥇","🥈","🥉"][i] if i < 3 else "▫️"
            tag = " *(current)*" if r['Is Current'] else ""
            st.write(f"{medal} **{r['Factory']}** — {r['Predicted Lead Time (Days)']:.1f}d | {r['Margin Impact (%)']:+.2f}%{tag}")
    else:
        st.info(f"✅ **Maintain** current assignment to **{cur_factory}**.")

with c4:
    st.markdown('<p class="sec-head">⚠️ Risk & Impact Panel</p>', unsafe_allow_html=True)

    margin = best['Margin Impact (%)']
    dt = cur_lt - best['Predicted Lead Time (Days)']

    st.markdown("**💰 Profit Assessment**")
    if margin < -1.5:
        st.error("🚨 **High Margin Erosion** — Requires executive override.")
    elif margin < 0:
        st.warning("⚠️ **Moderate Risk** — Review with finance.")
    else:
        st.success("✅ **Stable** — Margins safely maintained.")

    st.markdown("**🔒 Operational Risks**")
    risks = []
    if abs(dt) < 1.0:
        risks.append("⚡ Negligible gain (<1 day) — switching cost may outweigh benefit.")
    if best['Distance (km)'] > 2000:
        risks.append("🌍 Long-haul route (>2,000 km) — supply chain fragility risk.")
    if margin < -1.0 and dt > 5:
        risks.append("⚖️ Speed vs Cost tradeoff — consider hybrid strategy.")
    if not risks:
        st.info("No significant operational risks identified.")
    for r in risks:
        st.markdown(f"- {r}")

    st.markdown("---")
    spread = sim['Predicted Lead Time (Days)'].max() - sim['Predicted Lead Time (Days)'].min()
    conf = min(spread / max(cur_lt, 1) * 100, 100)
    if conf > 5:
        st.success(f"🎯 **Confidence: {conf:.1f}%** — Clear factory differentiation.")
    elif conf > 1:
        st.warning(f"🎯 **Confidence: {conf:.1f}%** — Moderate differentiation.")
    else:
        st.error(f"🎯 **Confidence: {conf:.1f}%** — Low differentiation.")

# ── KPI TABLE ─────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📖 KPI Definitions"):
    st.table(pd.DataFrame([{"KPI": k, "Description": v} for k, v in KPI_DEFINITIONS.items()]))

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Nassau Candy Decision Intelligence  ·  Streamlit  ·  © 2024")