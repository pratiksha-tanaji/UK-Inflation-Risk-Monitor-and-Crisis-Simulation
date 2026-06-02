import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="UK INFLATION RISK MONITOR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLING
# ============================================================
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #07111f 0%, #0b1728 100%);
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] {
            background: #081222;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        .block-container {
            padding-top: 1.15rem;
            padding-bottom: 2rem;
            max-width: 1520px;
        }

        .hero {
            background: linear-gradient(
            135deg,
            rgba(18,39,85,0.96),
            rgba(8,58,74,0.92)
        );
        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 28px;

        padding: 34px 42px;

        margin-top: 14px;
        margin-bottom: 1.8rem;

        box-shadow: 0 10px 30px rgba(0,0,0,0.28);

        overflow: hidden;
    }

        .hero-title {
            font-size: 3.1rem;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1.05;
            letter-spacing: 1px;
            margin-bottom: 18px;
        }

        .hero-subtitle {
            font-size: 1.08rem;
            color: #C7D2E3;
            max-width: 920px;
            line-height: 1.7;
            margin-bottom: 20px;
        }

        .hero-audience {
            font-size: 1rem;
            font-weight: 600;
            color: #8FB8FF;
            line-height: 1.7;
        }

        .section-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 1rem;
        }

        .summary-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 18px;
            margin-bottom: 1rem;
        }

        .summary-block {
            margin-bottom: 16px;
        }

        .summary-block:last-child {
            margin-bottom: 0;
        }

        .summary-label {
            font-size: 0.95rem;
            color: #cbd5e1;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .summary-text {
            font-size: 1.02rem;
            line-height: 1.8;
            color: #f8fafc;
        }

        .kpi-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 20px;
            min-height: 112px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .kpi-label {
            font-size: 0.92rem;
            color: #cbd5e1;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .kpi-value {
            font-size: 2.15rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }

        .kpi-risk {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 54px;
            font-weight: 800;
            border-radius: 14px;
            font-size: 1rem;
            margin-top: 6px;
        }

        .risk-low, .risk-moderate, .risk-high, .risk-crisis {
            padding: 0.95rem 1rem;
            border-radius: 14px;
            font-weight: 800;
            text-align: center;
        }

        .risk-low {
            background: rgba(34,197,94,0.16);
            color: #86efac;
            border: 1px solid rgba(34,197,94,0.35);
        }

        .risk-moderate {
            background: rgba(245,158,11,0.16);
            color: #fde68a;
            border: 1px solid rgba(245,158,11,0.35);
        }

        .risk-high {
            background: rgba(249,115,22,0.16);
            color: #fdba74;
            border: 1px solid rgba(249,115,22,0.35);
        }

        .risk-crisis {
            background: rgba(239,68,68,0.16);
            color: #fca5a5;
            border: 1px solid rgba(239,68,68,0.35);
        }

        .insight-box {
            background: rgba(59,130,246,0.12);
            border: 1px solid rgba(59,130,246,0.22);
            border-radius: 14px;
            padding: 16px 18px;
            color: #dbeafe;
            line-height: 1.75;
        }

        .subtle-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 14px;
            padding: 14px 16px;
        }

        .assessment-box {
            border-radius: 16px;
            padding: 28px 18px;
            font-weight: 900;
            text-align: center;
            font-size: 1.9rem;
            line-height: 1.25;
            margin-bottom: 14px;
        }

        .assessment-low {
            background: rgba(34,197,94,0.16);
            color: #d1fae5;
            border: 1px solid rgba(34,197,94,0.35);
        }

        .assessment-moderate {
            background: rgba(245,158,11,0.16);
            color: #fde68a;
            border: 1px solid rgba(245,158,11,0.35);
        }

        .assessment-high {
            background: rgba(249,115,22,0.16);
            color: #fdba74;
            border: 1px solid rgba(249,115,22,0.35);
        }

        .assessment-crisis {
            background: rgba(239,68,68,0.16);
            color: #fecaca;
            border: 1px solid rgba(239,68,68,0.35);
        }

        .mini-metric {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 14px;
            padding: 16px 18px;
            min-height: 120px;
        }

        .mini-label {
            color: #cbd5e1;
            font-size: 0.92rem;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .mini-value {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .mini-subvalue {
            color: #fde68a;
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .scenario-compare-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 16px 18px;
        }

        .compare-title {
            font-size: 0.95rem;
            color: #cbd5e1;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .compare-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
        }

        button[data-baseweb="tab"] {
            font-size: 1.18rem !important;
            font-weight: 800 !important;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
            color: #E5E7EB !important;
            letter-spacing: 0.2px;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF4B4B !important;
        }
        .sidebar-upload-note {
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.6;
            margin-top: 4px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================
def classify_inflation_risk(inflation: float) -> str:
    if pd.isna(inflation):
        return "Unknown"
    if inflation < 3:
        return "Low Risk"
    elif inflation < 5:
        return "Moderate Risk"
    elif inflation < 8:
        return "High Risk"
    return "Crisis Level"


def risk_css_class(label: str) -> str:
    return {
        "Low Risk": "risk-low",
        "Moderate Risk": "risk-moderate",
        "High Risk": "risk-high",
        "Crisis Level": "risk-crisis",
    }.get(label, "risk-moderate")


def safe_read_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_base_files():
    master_df = safe_read_csv("data/master_dataset.csv")
    pred_df = safe_read_csv("data/inflation_predictions.csv")
    feat_df = safe_read_csv("data/feature_importance.csv")

    for df in [master_df, pred_df]:
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df.sort_values("Date", inplace=True)

    if not feat_df.empty and feat_df.shape[1] >= 2:
        feat_df.columns = ["Feature", "Importance"] + list(feat_df.columns[2:])

    return master_df, pred_df, feat_df


def latest_non_null(df: pd.DataFrame, col: str):
    if df.empty or col not in df.columns:
        return np.nan
    s = df[col].dropna()
    return s.iloc[-1] if not s.empty else np.nan


def build_plotly_layout(fig, height=400):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#e5e7eb"),
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="#111827", font_color="#ffffff", bordercolor="#374151"),
    )
    fig.update_xaxes(showgrid=False, color="#cbd5e1")
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.08)",
        color="#cbd5e1",
    )
    return fig


def prepare_feature_importance(feat_df: pd.DataFrame) -> pd.DataFrame:
    if feat_df.empty:
        return pd.DataFrame(columns=["Feature", "Importance"])

    temp = feat_df.copy()
    if "Feature" not in temp.columns and temp.shape[1] >= 2:
        temp = temp.reset_index()
        temp.columns = ["Feature", "Importance"] + list(temp.columns[2:])

    if "Importance" not in temp.columns and temp.shape[1] >= 2:
        temp.columns = ["Feature", "Importance"] + list(temp.columns[2:])

    temp = temp[["Feature", "Importance"]].copy()
    temp["Importance"] = pd.to_numeric(temp["Importance"], errors="coerce")
    return temp.dropna(subset=["Importance"]).sort_values("Importance", ascending=False)


def plain_language_driver_summary(feat_df: pd.DataFrame) -> str:
    if feat_df.empty:
        return "Key drivers summary unavailable."

    top = feat_df.head(3)["Feature"].tolist()
    mapping = {
        "Inflation_lag1": "recent inflation momentum",
        "Inflation_lag2": "short-term inflation persistence",
        "Inflation_lag3": "inflation momentum 3",
        "Inflation_lag6": "medium-term inflation persistence",
        "Inflation_lag12": "yearly inflation persistence",
        "GDP": "growth conditions",
        "GDP_growth": "economic growth",
        "GDP_Growth": "economic growth",
        "Unemployment": "labour market slack",
        "Bank_Rate": "interest rate conditions",
        "FTSE100": "market sentiment",
        "RSI": "retail sales activity",
        "Rate_Unemployment": "policy and labour interaction",
        "Market_Sentiment": "market and demand sentiment",
    }
    readable = [mapping.get(x, x.replace("_", " ").lower()) for x in top]
    if len(readable) == 1:
        return f"The forecast is currently influenced most by {readable[0]}."
    return f"The forecast is currently influenced most by {', '.join(readable[:-1])} and {readable[-1]}."


def proxy_future_prediction(row, history_row):
    base = float(history_row.get("Inflation_YoY", 4.0))
    pred = (
        base
        + 0.30 * (float(row["Bank_Rate"]) - float(history_row.get("Bank_Rate", row["Bank_Rate"])))
        + 0.35 * (float(row["Unemployment"]) - float(history_row.get("Unemployment", row["Unemployment"])))
        - 0.20 * (float(row["GDP_Growth"]) - float(history_row.get("GDP_Growth", row["GDP_Growth"])))
        - 0.02 * (float(row["RSI"]) - float(history_row.get("RSI", row["RSI"])))
        - 0.10 * (float(row["Market_Change"]) - float(history_row.get("Market_Change", row["Market_Change"])))
    )
    return round(pred, 2)


def make_history_reference(master_df: pd.DataFrame) -> pd.Series:
    defaults = {
        "Inflation_YoY": 4.0,
        "Bank_Rate": 5.0,
        "Unemployment": 4.5,
        "GDP_Growth": 2.0,
        "RSI": 100.0,
        "Market_Change": 0.0,
    }

    if master_df.empty:
        return pd.Series(defaults)

    hist = master_df.copy()

    if "GDP_Growth" not in hist.columns:
        if "GDP" in hist.columns:
            hist["GDP_Growth"] = pd.to_numeric(hist["GDP"], errors="coerce").pct_change() * 100
        else:
            hist["GDP_Growth"] = np.nan

    if "Market_Change" not in hist.columns:
        if "FTSE100" in hist.columns:
            hist["Market_Change"] = pd.to_numeric(hist["FTSE100"], errors="coerce").pct_change() * 100
        else:
            hist["Market_Change"] = 0.0

    if "Inflation_YoY" not in hist.columns:
        return pd.Series(defaults)

    hist = hist.dropna(subset=["Inflation_YoY"])
    if hist.empty:
        return pd.Series(defaults)

    latest = hist.iloc[-1]

    return pd.Series({
        "Inflation_YoY": float(latest.get("Inflation_YoY", defaults["Inflation_YoY"])),
        "Bank_Rate": float(latest.get("Bank_Rate", defaults["Bank_Rate"])),
        "Unemployment": float(latest.get("Unemployment", defaults["Unemployment"])),
        "GDP_Growth": float(latest.get("GDP_Growth", defaults["GDP_Growth"])) if not pd.isna(latest.get("GDP_Growth", np.nan)) else defaults["GDP_Growth"],
        "RSI": float(latest.get("RSI", defaults["RSI"])),
        "Market_Change": float(latest.get("Market_Change", defaults["Market_Change"])) if not pd.isna(latest.get("Market_Change", np.nan)) else defaults["Market_Change"],
    })


def forecast_future_inflation(uploaded_future_df: pd.DataFrame, history_ref: pd.Series) -> pd.DataFrame:
    scenario = uploaded_future_df.copy()
    scenario["Date"] = pd.to_datetime(scenario["Date"], errors="coerce")
    scenario = scenario.dropna(subset=["Date"]).sort_values("Date")

    preds = []
    current_ref = history_ref.copy()

    for _, row in scenario.iterrows():
        pred = proxy_future_prediction(row, current_ref)
        preds.append({
            "Date": row["Date"],
            "Predicted_Inflation": pred,
            "Lower_Bound": pred - 2.65,
            "Upper_Bound": pred + 2.65,
            "Risk_Level": classify_inflation_risk(pred),
        })

        current_ref["Inflation_YoY"] = pred
        current_ref["Bank_Rate"] = float(row["Bank_Rate"])
        current_ref["Unemployment"] = float(row["Unemployment"])
        current_ref["GDP_Growth"] = float(row["GDP_Growth"])
        current_ref["RSI"] = float(row["RSI"])
        current_ref["Market_Change"] = float(row["Market_Change"])

    return pd.DataFrame(preds)


def inflation_risk_score(inflation):
    if pd.isna(inflation):
        return 0
    if inflation >= 8:
        return 3
    if inflation >= 5:
        return 2
    if inflation >= 3:
        return 1
    return 0


def gdp_risk_score(gdp_growth):
    if pd.isna(gdp_growth):
        return 0
    if gdp_growth < 0:
        return 3
    if gdp_growth < 1:
        return 2
    if gdp_growth < 2:
        return 1
    return 0


def unemployment_risk_score(unemp):
    if pd.isna(unemp):
        return 0
    if unemp >= 6.5:
        return 3
    if unemp >= 5.5:
        return 2
    if unemp >= 5.0:
        return 1
    return 0


def bank_rate_risk_score(rate):
    if pd.isna(rate):
        return 0
    if rate >= 5.25:
        return 3
    if rate >= 4.0:
        return 2
    if rate >= 3.0:
        return 1
    return 0


def retail_risk_score(rsi):
    if pd.isna(rsi):
        return 0
    if rsi < 95:
        return 3
    if rsi < 100:
        return 2
    if rsi < 102:
        return 1
    return 0


def market_risk_score(market_change):
    if pd.isna(market_change):
        return 0
    if market_change <= -10:
        return 3
    if market_change <= -5:
        return 2
    if market_change < 0:
        return 1
    return 0


def crisis_status(total_score):
    if total_score <= 3:
        return "No Crisis"
    if total_score <= 6:
        return "Low Risk Crisis Detected"
    if total_score <= 10:
        return "Moderate Risk Crisis Detected"
    return "High Risk Crisis Detected"


def crisis_status_css(status):
    if "No Crisis" in status:
        return "assessment-low"
    if "Low Risk" in status:
        return "assessment-moderate"
    if "Moderate Risk" in status:
        return "assessment-high"
    return "assessment-crisis"


def triggered_conditions_text(inflation_score, gdp_score, unemp_score, bank_score, retail_score, market_score):
    triggers = []

    if inflation_score == 3:
        triggers.append("inflation is at crisis level")
    elif inflation_score == 2:
        triggers.append("inflation is elevated")

    if gdp_score == 3:
        triggers.append("GDP growth is deeply negative")
    elif gdp_score == 2:
        triggers.append("GDP growth is weak")

    if unemp_score == 3:
        triggers.append("unemployment is at a critical level")
    elif unemp_score == 2:
        triggers.append("unemployment is high")

    if bank_score == 3:
        triggers.append("bank rate is at a highly restrictive level")
    elif bank_score == 2:
        triggers.append("bank rate is elevated")

    if retail_score == 3:
        triggers.append("retail sales are sharply declining")
    elif retail_score == 2:
        triggers.append("retail sales are weak")

    if market_score == 3:
        triggers.append("market conditions are under severe stress")
    elif market_score == 2:
        triggers.append("market conditions are weakening")

    if not triggers:
        return "All selected indicators are within normal or mild-risk range."

    return "Crisis risk is indicated because " + ", ".join(triggers) + "."


def confidence_of_indication(total_score):
    return int(round(min(95, max(35, 35 + total_score * 6))))


def confidence_level_label(conf_pct):
    if conf_pct < 50:
        return "Low Confidence"
    if conf_pct < 75:
        return "Moderate Confidence"
    return "High Confidence"


def indicator_status_label(score):
    return {
        0: "Normal",
        1: "Mild Risk",
        2: "Elevated",
        3: "Critical",
    }.get(score, "Normal")


def inflation_vs_target(inflation, target=2.0):
    if pd.isna(inflation):
        return np.nan
    return round(inflation - target, 2)


def risk_direction(pred_df):
    if pred_df.empty or "Predicted_Inflation" not in pred_df.columns:
        return "Stable"
    recent = pred_df["Predicted_Inflation"].dropna().tail(6)
    if len(recent) < 2:
        return "Stable"
    diff = recent.iloc[-3:].mean() - recent.iloc[:3].mean()
    if diff > 0.25:
        return "Worsening"
    if diff < -0.25:
        return "Easing"
    return "Stable"


def most_pressured_indicators(score_map):
    if not score_map:
        return "None"
    max_score = max(score_map.values())
    if max_score <= 0:
        return "None"
    return ", ".join([k for k, v in score_map.items() if v == max_score])


def policy_view_text(risk_label, forecast_inflation):
    if pd.isna(forecast_inflation):
        return "Policy view unavailable."
    if risk_label == "Low Risk":
        return "Inflation remains near manageable territory with limited near-term stress."
    if risk_label == "Moderate Risk":
        return "Inflation remains above target and should be monitored for persistence."
    if risk_label == "High Risk":
        return "Inflation pressure is materially elevated and may require sustained policy restraint."
    return "Inflation conditions are severe and consistent with crisis-level stress."


def market_view_text(direction):
    if direction == "Worsening":
        return "Recent forecasts suggest risk is building rather than easing."
    if direction == "Easing":
        return "Recent forecasts suggest inflation stress may be moderating."
    return "Recent forecasts suggest broadly stable inflation conditions."


def scenario_summary_text(status, scenario_pred, conf_pct, stressed):
    return (
        f"Scenario outcome: {status}. Forecast inflation is {scenario_pred:.2f}%, "
        f"with confidence of indication at {conf_pct}%. Most pressured indicator(s): {stressed}."
    )


def create_snapshot_text(current_inflation, forecast_inflation, forecast_range_text, risk_label, target_gap, direction):
    lines = [
        "UK INFLATION RISK MONITOR SNAPSHOT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Current Inflation: {current_inflation:.2f}%" if not pd.isna(current_inflation) else "Current Inflation: N/A",
        f"Forecast Inflation: {forecast_inflation:.2f}%" if not pd.isna(forecast_inflation) else "Forecast Inflation: N/A",
        f"Forecast Range: {forecast_range_text}",
        f"Risk Level: {risk_label}",
        f"Inflation vs 2% Target: {target_gap:+.2f} pp" if not pd.isna(target_gap) else "Inflation vs 2% Target: N/A",
        f"Risk Direction: {direction}",
    ]
    return "\n".join(lines)


def create_template_csv():
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    template_df = pd.DataFrame({
        "Date": dates.strftime("%Y-%m-%d"),
        "GDP_Growth": [""] * 12,
        "Unemployment": [""] * 12,
        "Bank_Rate": [""] * 12,
        "RSI": [""] * 12,
        "Market_Change": [""] * 12,
    })
    return template_df.to_csv(index=False).encode("utf-8")


# ============================================================
# LOAD DATA
# ============================================================
master_df, pred_df, feat_df = load_base_files()
feat_df = prepare_feature_importance(feat_df)

if master_df.empty or pred_df.empty:
    st.error("Required files missing. Please ensure master_dataset.csv and inflation_predictions.csv are inside the data/ folder.")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Designed for policy and market-facing users.")

show_confidence = st.sidebar.toggle("Show forecast range", value=True)
show_crisis_bands = st.sidebar.toggle("Show crisis periods", value=True)

min_date, max_date = None, None
for df in [master_df, pred_df]:
    if not df.empty and "Date" in df.columns:
        cur_min, cur_max = df["Date"].min(), df["Date"].max()
        min_date = cur_min if min_date is None else min(min_date, cur_min)
        max_date = cur_max if max_date is None else max(max_date, cur_max)

if min_date is not None and max_date is not None:
    date_range = st.sidebar.date_input(
        "Select analysis period",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
    )
else:
    date_range = None

st.sidebar.markdown("---")
st.sidebar.subheader("Future Scenario Upload")
st.sidebar.markdown(
    '<div class="sidebar-upload-note">Download the template, fill in your scenario assumptions, and upload the completed CSV for simulation.</div>',
    unsafe_allow_html=True,
)

st.sidebar.download_button(
    label="Download Scenario Template",
    data=create_template_csv(),
    file_name="scenario_template.csv",
    mime="text/csv",
)

scenario_file = st.sidebar.file_uploader(
    "Upload future scenario CSV",
    type=["csv"],
    key="scenario"
)

# ============================================================
# FILTER DATA
# ============================================================
filtered_master = master_df.copy()
filtered_pred = pred_df.copy()

if date_range and isinstance(date_range, tuple) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    if "Date" in filtered_master.columns:
        filtered_master = filtered_master[(filtered_master["Date"] >= start_date) & (filtered_master["Date"] <= end_date)]
    if "Date" in filtered_pred.columns:
        filtered_pred = filtered_pred[(filtered_pred["Date"] >= start_date) & (filtered_pred["Date"] <= end_date)]

# ============================================================
# KPI VALUES
# ============================================================
current_inflation = latest_non_null(filtered_pred, "Actual_Inflation")
if pd.isna(current_inflation):
    current_inflation = latest_non_null(filtered_master, "Inflation_YoY")

forecast_inflation = latest_non_null(filtered_pred, "Predicted_Inflation")
forecast_lower = latest_non_null(filtered_pred, "Lower_Bound")
forecast_upper = latest_non_null(filtered_pred, "Upper_Bound")
risk_label = classify_inflation_risk(forecast_inflation)

forecast_range_text = "N/A" if pd.isna(forecast_lower) or pd.isna(forecast_upper) else f"{forecast_lower:.2f}% – {forecast_upper:.2f}%"
driver_summary = plain_language_driver_summary(feat_df)
target_gap = inflation_vs_target(forecast_inflation)
direction = risk_direction(filtered_pred)
policy_text = policy_view_text(risk_label, forecast_inflation)
market_text = market_view_text(direction)
snapshot_text = create_snapshot_text(current_inflation, forecast_inflation, forecast_range_text, risk_label, target_gap, direction)
target_gap_text = "N/A" if pd.isna(target_gap) else f"{target_gap:+.2f} pp"

# ============================================================
# MINIMAL HERO HEADER
# ============================================================
hero_html = (
    '<div class="hero">'
    '<div class="hero-title">UK INFLATION RISK MONITOR 📊</div>'
    '<div class="hero-subtitle">'
    'Early-warning dashboard for inflation forecasting, crisis detection, '
    'and forward-looking macroeconomic risk assessment.'
    '</div>'
    '<div class="hero-audience">'
    'Designed for: Central Banks • Financial Institutions • Policy Analysts • Economic Researchers'
    '</div>'
    '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)

# ============================================================
# KPI ROW - CLEAN FIRST VIEW
# ============================================================
k1, k2, k3, k4 = st.columns(4, gap="large")

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Current Inflation</div>
            <div class="kpi-value">{current_inflation:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Forecast Inflation</div>
            <div class="kpi-value">{forecast_inflation:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Risk Level</div>
            <div class="kpi-risk {risk_css_class(risk_label)}">{risk_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Forecast Range</div>
            <div class="kpi-value" style="font-size:1.75rem;">{forecast_range_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "Executive Overview",
    "Scenario Simulator",
    "Market & Policy Signals",
])

# ============================================================
# TAB 1: EXECUTIVE OVERVIEW
# ============================================================
with tab1:
    left, right = st.columns([2.25, 1], gap="large")

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Inflation Outlook: Actual vs Forecast")

        fig = go.Figure()

        if "Actual_Inflation" in filtered_pred.columns:
            fig.add_trace(go.Scatter(
                x=filtered_pred["Date"],
                y=filtered_pred["Actual_Inflation"],
                mode="lines",
                name="Actual Inflation",
                line=dict(width=2.5, color="#cbd5e1"),
                hovertemplate="<b>Actual Inflation</b><br>Date: %{x|%b %Y}<br>Value: %{y:.2f}%<extra></extra>",
            ))

        if "Predicted_Inflation" in filtered_pred.columns:
            fig.add_trace(go.Scatter(
                x=filtered_pred["Date"],
                y=filtered_pred["Predicted_Inflation"],
                mode="lines",
                name="Forecast Inflation",
                line=dict(width=2.0, color="#3b82f6"),
                hovertemplate="<b>Forecast Inflation</b><br>Date: %{x|%b %Y}<br>Value: %{y:.2f}%<extra></extra>",
            ))

        if show_confidence and {"Lower_Bound", "Upper_Bound"}.issubset(filtered_pred.columns):
            fig.add_trace(go.Scatter(
                x=filtered_pred["Date"],
                y=filtered_pred["Upper_Bound"],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            ))
            fig.add_trace(go.Scatter(
                x=filtered_pred["Date"],
                y=filtered_pred["Lower_Bound"],
                mode="lines",
                fill="tonexty",
                opacity=0.12,
                line=dict(width=0),
                name="Forecast Range",
                hovertemplate="<b>Forecast Range</b><br>Date: %{x|%b %Y}<br>Lower Bound: %{y:.2f}%<extra></extra>",
            ))

        if show_crisis_bands:
            fig.add_vrect(x0="2020-03-01", x1="2021-06-01", fillcolor="gray", opacity=0.12, line_width=0)
            fig.add_vrect(x0="2022-01-01", x1="2023-12-01", fillcolor="red", opacity=0.08, line_width=0)

        fig.add_hline(y=2, line_dash="dot", line_color="#22c55e", opacity=0.9, annotation_text="BoE 2% Target", annotation_position="top left")
        fig.add_hline(y=3, line_dash="dash", opacity=0.35)
        fig.add_hline(y=5, line_dash="dash", opacity=0.35)
        fig.add_hline(y=8, line_dash="dash", opacity=0.35)

        build_plotly_layout(fig, height=430)
        fig.update_yaxes(title="Inflation (%)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.subheader("Current Risk Summary")

        summary_text = f"The latest forecast suggests a {risk_label.lower()} outlook, with forecast inflation at {forecast_inflation:.2f}%."

        interpretation = "Inflation remains relatively contained."
        if risk_label == "Moderate Risk":
            interpretation = "Inflation is above comfort levels and should be monitored closely."
        elif risk_label == "High Risk":
            interpretation = "Inflation pressures are materially elevated and could affect policy and market stability."
        elif risk_label == "Crisis Level":
            interpretation = "Inflation conditions are severe and consistent with crisis-level stress."

        st.markdown(
            f"""
            <div class="summary-block">
                <div class="summary-label">Latest Assessment</div>
                <div class="summary-text">{summary_text}</div>
            </div>

            <div class="summary-block">
                <div class="subtle-box">
                    <div class="summary-label">Inflation vs 2% Target</div>
                    <div class="summary-text">{target_gap_text}</div>
                </div>
            </div>

            <div class="summary-block">
                <div class="subtle-box">
                    <div class="summary-label">Risk Direction</div>
                    <div class="summary-text">{direction}</div>
                </div>
            </div>

            <div class="summary-block">
                <div class="insight-box">{interpretation}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] div:has(> div.element-container > div.stPlotlyChart) {
        margin-bottom: -70px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    lower_left, lower_mid, lower_right = st.columns([1.25, 1.05, 1], gap="large")

    with lower_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Risk Trend Over Time")

        risk_fig = go.Figure()
        if {"Date", "Predicted_Inflation"}.issubset(filtered_pred.columns):
            risk_fig.add_trace(go.Scatter(
                x=filtered_pred["Date"],
                y=filtered_pred["Predicted_Inflation"],
                mode="lines+markers",
                name="Forecast Inflation",
                line=dict(color="#60a5fa", width=2.0),
            ))
            risk_fig.add_hline(y=3, line_dash="dash")
            risk_fig.add_hline(y=5, line_dash="dash")
            risk_fig.add_hline(y=8, line_dash="dash")

        build_plotly_layout(risk_fig, height=240)
        risk_fig.update_yaxes(title="Forecast Inflation (%)")
        st.plotly_chart(risk_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with lower_mid:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Technical Detail")
        st.write("For user-facing decisions, the dashboard emphasizes inflation level, risk classification, and scenario outcomes rather than technical model diagnostics.")
        with st.expander("View model driver chart"):
            if not feat_df.empty:
                top_features = feat_df.head(8).sort_values("Importance", ascending=True)
                bar_fig = px.bar(top_features, x="Importance", y="Feature", orientation="h", title="Key Forecast Drivers")
                build_plotly_layout(bar_fig, height=300)
                st.plotly_chart(bar_fig, use_container_width=True)
            else:
                st.info("Driver chart unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)

    with lower_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Snapshot & Export")
        st.markdown(f"<div class='insight-box'>{snapshot_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        st.download_button(
            label="Download Snapshot (.txt)",
            data=snapshot_text.encode("utf-8"),
            file_name="uk_inflation_risk_snapshot.txt",
            mime="text/plain",
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB 2: SCENARIO SIMULATOR
# ============================================================
with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Scenario Simulator")
    st.write("Adjust scenario assumptions to assess inflation outlook and crisis risk under future macroeconomic conditions.")

    history_ref = make_history_reference(master_df)

    sim_left, sim_right = st.columns([1.0, 1.55], gap="large")

    with sim_left:
        st.markdown("### Inputs")
        sim_gdp_growth = st.slider("GDP Growth (%)", -8.0, 8.0, float(np.clip(history_ref["GDP_Growth"], -8, 8)), 0.1)
        sim_unemp = st.slider("Unemployment (%)", 2.0, 12.0, float(np.clip(history_ref["Unemployment"], 2, 12)), 0.1)
        sim_rate = st.slider("Bank Rate (%)", 0.0, 10.0, float(np.clip(history_ref["Bank_Rate"], 0, 10)), 0.1)
        sim_rsi = st.slider("Retail Sales Index", 85.0, 110.0, float(np.clip(history_ref["RSI"], 85, 110)), 0.1)
        sim_market_change = st.slider("Market Change (%)", -15.0, 15.0, float(np.clip(history_ref["Market_Change"], -15, 15)), 0.1)

    scenario_row = pd.Series({
        "GDP_Growth": sim_gdp_growth,
        "Unemployment": sim_unemp,
        "Bank_Rate": sim_rate,
        "RSI": sim_rsi,
        "Market_Change": sim_market_change,
    })

    scenario_pred = proxy_future_prediction(scenario_row, history_ref)

    inf_score = inflation_risk_score(scenario_pred)
    gdp_score = gdp_risk_score(sim_gdp_growth)
    unemp_score = unemployment_risk_score(sim_unemp)
    bank_score = bank_rate_risk_score(sim_rate)
    retail_score = retail_risk_score(sim_rsi)
    market_score = market_risk_score(sim_market_change)

    total_score = inf_score + gdp_score + unemp_score + bank_score + retail_score + market_score
    status = crisis_status(total_score)
    explanation = triggered_conditions_text(inf_score, gdp_score, unemp_score, bank_score, retail_score, market_score)

    conf_pct = confidence_of_indication(total_score)
    conf_label = confidence_level_label(conf_pct)
    progress_value = min(conf_pct / 100, 1.0)

    score_map = {
        "Inflation Outlook": inf_score,
        "GDP Growth": gdp_score,
        "Unemployment": unemp_score,
        "Bank Rate": bank_score,
        "Retail Sales Index": retail_score,
        "Market Conditions": market_score,
    }
    stressed = most_pressured_indicators(score_map)

    base_status = crisis_status(
        inflation_risk_score(history_ref["Inflation_YoY"])
        + gdp_risk_score(history_ref["GDP_Growth"])
        + unemployment_risk_score(history_ref["Unemployment"])
        + bank_rate_risk_score(history_ref["Bank_Rate"])
        + retail_risk_score(history_ref["RSI"])
        + market_risk_score(history_ref["Market_Change"])
    )
    base_pred = history_ref["Inflation_YoY"]

    with sim_right:
        st.markdown("### Crisis Assessment")
        st.markdown(f'<div class="assessment-box {crisis_status_css(status)}">{status}</div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns([1, 1, 1.15], gap="medium")

        with m1:
            st.markdown(
                f"""
                <div class="mini-metric">
                    <div class="mini-label">Scenario Forecast Inflation</div>
                    <div class="mini-value">{scenario_pred:.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="mini-metric">
                    <div class="mini-label">Confidence of Indication (%)</div>
                    <div class="mini-value">{conf_pct}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m3:
            st.markdown(
                f"""
                <div class="mini-metric">
                    <div class="mini-label">Confidence Level</div>
                    <div class="mini-subvalue">{conf_label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.progress(progress_value)

        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:
            st.markdown(
                f"""
                <div class="scenario-compare-card">
                    <div class="compare-title">Base Scenario Status</div>
                    <div class="compare-value" style="font-size:1.25rem;">{base_status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            delta_pred = scenario_pred - base_pred
            st.markdown(
                f"""
                <div class="scenario-compare-card">
                    <div class="compare-title">Base vs Stressed Inflation</div>
                    <div class="compare-value">{delta_pred:+.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="scenario-compare-card">
                    <div class="compare-title">Most Pressured Indicator</div>
                    <div class="compare-value" style="font-size:1.25rem;">{stressed}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Why this result?")
        st.markdown(f"<div class='insight-box'>{explanation}</div>", unsafe_allow_html=True)

        st.markdown("### Scenario Summary")
        st.markdown(f"<div class='insight-box'>{scenario_summary_text(status, scenario_pred, conf_pct, stressed)}</div>", unsafe_allow_html=True)

    breakdown_df = pd.DataFrame({
        "Indicator": ["Inflation Outlook", "GDP Growth", "Unemployment", "Bank Rate", "Retail Sales Index", "Market Conditions"],
        "Status": [
            indicator_status_label(inf_score),
            indicator_status_label(gdp_score),
            indicator_status_label(unemp_score),
            indicator_status_label(bank_score),
            indicator_status_label(retail_score),
            indicator_status_label(market_score),
        ],
        "Risk Score": [inf_score, gdp_score, unemp_score, bank_score, retail_score, market_score],
    })

    st.markdown("### Indicator Risk Breakdown")
    st.caption("Shows how each scenario input is classified against crisis thresholds.")
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

    if scenario_file is not None:
        st.markdown("### Uploaded Future Scenario Results")
        scenario_df = pd.read_csv(scenario_file)
        st.write("Scenario preview")
        st.dataframe(scenario_df.head(), use_container_width=True)

        required = ["Date", "GDP_Growth", "Unemployment", "Bank_Rate", "RSI", "Market_Change"]
        missing = [c for c in required if c not in scenario_df.columns]

        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}")
        else:
            future_results = forecast_future_inflation(scenario_df, history_ref)

            future_results["Inflation_Risk_Score"] = future_results["Predicted_Inflation"].apply(inflation_risk_score)
            future_results["GDP_Risk_Score"] = scenario_df["GDP_Growth"].apply(gdp_risk_score)
            future_results["Unemployment_Risk_Score"] = scenario_df["Unemployment"].apply(unemployment_risk_score)
            future_results["BankRate_Risk_Score"] = scenario_df["Bank_Rate"].apply(bank_rate_risk_score)
            future_results["Retail_Risk_Score"] = scenario_df["RSI"].apply(retail_risk_score)
            future_results["Market_Risk_Score"] = scenario_df["Market_Change"].apply(market_risk_score)

            future_results["Total_Crisis_Score"] = (
                future_results["Inflation_Risk_Score"]
                + future_results["GDP_Risk_Score"]
                + future_results["Unemployment_Risk_Score"]
                + future_results["BankRate_Risk_Score"]
                + future_results["Retail_Risk_Score"]
                + future_results["Market_Risk_Score"]
            )

            future_results["Crisis_Status"] = future_results["Total_Crisis_Score"].apply(crisis_status)
            future_results["Confidence_of_Indication_%"] = future_results["Total_Crisis_Score"].apply(confidence_of_indication)
            future_results["Confidence_Level"] = future_results["Confidence_of_Indication_%"].apply(confidence_level_label)

            st.success("Scenario forecast generated.")
            st.dataframe(future_results, use_container_width=True)

            scen_fig = go.Figure()
            scen_fig.add_trace(go.Scatter(
                x=future_results["Date"],
                y=future_results["Predicted_Inflation"],
                mode="lines+markers",
                name="Scenario Forecast Inflation",
                line=dict(color="#3b82f6", width=2.5),
                hovertemplate="<b>Scenario Forecast Inflation</b><br>Date: %{x|%b %Y}<br>Value: %{y:.2f}%<extra></extra>",
            ))
            scen_fig.add_hline(y=2, line_dash="dot", line_color="#22c55e", annotation_text="BoE 2% Target", annotation_position="top left")
            scen_fig.add_hline(y=3, line_dash="dash")
            scen_fig.add_hline(y=5, line_dash="dash")
            scen_fig.add_hline(y=8, line_dash="dash")
            build_plotly_layout(scen_fig, height=420)
            st.plotly_chart(scen_fig, use_container_width=True)

            st.download_button(
                label="Download Scenario Results",
                data=future_results.to_csv(index=False).encode("utf-8"),
                file_name="scenario_results.csv",
                mime="text/csv",
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 3: MARKET & POLICY SIGNALS
# ============================================================
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Market & Policy Signals")

    feature_choices = [
        c for c in ["Inflation_YoY", "GDP", "Unemployment", "RSI", "Bank_Rate", "FTSE100"]
        if c in filtered_master.columns
    ]

    selected_feature = st.selectbox("Select signal", feature_choices)

    signal_fig = px.line(filtered_master, x="Date", y=selected_feature, title=f"{selected_feature} Over Time")
    if show_crisis_bands:
        signal_fig.add_vrect(x0="2020-03-01", x1="2021-06-01", fillcolor="gray", opacity=0.14, line_width=0)
        signal_fig.add_vrect(x0="2022-01-01", x1="2023-12-01", fillcolor="red", opacity=0.10, line_width=0)
    if selected_feature == "Inflation_YoY":
        signal_fig.add_hline(y=2, line_dash="dot", line_color="#22c55e", annotation_text="BoE 2% Target", annotation_position="top left")
    build_plotly_layout(signal_fig, height=440)
    st.plotly_chart(signal_fig, use_container_width=True)

    latest_signal_value = latest_non_null(filtered_master, selected_feature)
    signal_note = {
        "Inflation_YoY": "Shows current inflation pressure across the selected period.",
        "GDP": "Shows how broad economic output has evolved over time.",
        "Unemployment": "Shows labour market pressure and slack.",
        "RSI": "Shows consumer spending and retail demand conditions.",
        "Bank_Rate": "Shows monetary policy stance over time.",
        "FTSE100": "Shows broad market direction and sentiment.",
    }.get(selected_feature, "Signal interpretation unavailable.")

    s1, s2, s3 = st.columns([1, 1, 2], gap="large")

    with s1:
        st.markdown(
            f"""
            <div class="mini-metric">
                <div class="mini-label">Latest {selected_feature}</div>
                <div class="mini-value">{latest_signal_value:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        if selected_feature == "Inflation_YoY":
            sig_gap = inflation_vs_target(latest_signal_value)
            sig_gap_txt = f"{sig_gap:+.2f} pp" if not pd.isna(sig_gap) else "N/A"
            st.markdown(
                f"""
                <div class="mini-metric">
                    <div class="mini-label">Signal vs 2% Target</div>
                    <div class="mini-value">{sig_gap_txt}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="mini-metric">
                    <div class="mini-label">Signal Assessment</div>
                    <div class="mini-value" style="font-size:1.4rem;">Context View</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with s3:
        st.markdown(f"<div class='insight-box'>{signal_note}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("User-facing dashboard version for policy and financial decision support. The scenario workflow uses a downloadable template plus sidebar upload for structured future assumptions.")