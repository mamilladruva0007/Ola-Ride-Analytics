import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from html import escape
from PIL import Image

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="OLA Ride Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. PATHS AND COLORS
# =========================================================
LOGO_PATH = Path(r"C:\Users\mamil\Desktop\OLA-Ride-Analytics-Big-Data-Cloud\project-screenshots\ola-seeklogo.png")

DATA_PATHS = [
    Path(__file__).resolve().parent / "Bookings_Cleaned.csv",
    Path.cwd() / "Bookings_Cleaned.csv",
    Path(r"C:\Users\mamil\Downloads\Bookings_Cleaned.csv"),
    Path(r"C:\Users\mamil\Desktop\BDA\Bookings_Cleaned.csv"),
]

GREEN = "#22C55E"
DARK_GREEN = "#15803D"
LIGHT_GREEN = "#F0FDF4"
PALE_GREEN = "#DCFCE7"
GRID_GREEN = "#86EFAC"
BLACK = "#000000"
WHITE = "#FFFFFF"
BLUE = "#08A9EF"

# =========================================================
# 3. CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>
    /* Main application */
    .stApp {
        background: #F1F1F1 !important;
        color: #000000 !important;
    }

    [data-testid="stHeader"] {
        background: #F1F1F1 !important;
    }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 3.5rem 1.5rem 2rem 1.5rem !important;
        overflow: visible !important;
        box-sizing: border-box !important;
    }

    /* Main content text */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp strong,
    .stApp small,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stMarkdownContainer"] * {
        color: #000000 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #252525 !important;
        border-right: 2px solid #22C55E !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.7rem !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #FFFFFF !important;
    }

    /* Logo */
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        background: #FFFFFF !important;
        padding: 10px !important;
        border-radius: 12px !important;
        border-bottom: 3px solid #22C55E !important;
        margin: 8px 0 12px 0 !important;
        box-sizing: border-box !important;
    }

    section[data-testid="stSidebar"] [data-testid="stImage"] img {
        display: block !important;
        width: 100% !important;
        max-height: 115px !important;
        object-fit: contain !important;
    }

    .logo-fallback {
        background: #FFFFFF !important;
        color: #000000 !important;
        padding: 25px 12px !important;
        text-align: center !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border-bottom: 3px solid #22C55E !important;
        margin-bottom: 15px !important;
    }

    .sidebar-section-label {
        padding: 10px 8px 14px !important;
        color: #FFFFFF !important;
        font-size: 11px !important;
        letter-spacing: 3px !important;
        font-weight: 800 !important;
        text-align: center !important;
    }

    /* Navigation buttons */
    section[data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        min-height: 54px !important;
        height: 54px !important;
        padding: 0 16px !important;
        margin: 0 0 8px 0 !important;
        border-radius: 12px !important;
        border: 1px solid #414141 !important;
        background: #303030 !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.25s ease !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #414141 !important;
        border: 1px solid #22C55E !important;
        color: #FFFFFF !important;
        transform: translateX(3px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.18) !important;
    }

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: #8FD14F !important;
        color: #000000 !important;
        border: 1px solid #8FD14F !important;
        border-left: 5px solid #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }

    /* Sidebar collapse and expand controls */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarExpandButton"] {
        opacity: 1 !important;
        visibility: visible !important;
        z-index: 999999 !important;
    }

    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarExpandButton"] button {
        background: #252525 !important;
        border: 2px solid #22C55E !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarExpandButton"] svg {
        color: #FFFFFF !important;
        fill: none !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Dashboard title */
    .dashboard-title {
        display: block !important;
        color: #000000 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        line-height: 1.5 !important;
        margin: 12px 0 !important;
        padding: 6px 0 !important;
        overflow-wrap: anywhere !important;
        overflow: visible !important;
    }

    .dashboard-caption {
        color: #000000 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
        margin-bottom: 24px !important;
    }

    /* KPI cards */
    .kpi-card {
        background: #F0FDF4 !important;
        border: 1px solid #BBF7D0 !important;
        border-left: 6px solid #22C55E !important;
        border-radius: 14px !important;
        padding: 20px 16px !important;
        min-height: 120px !important;
        height: 100% !important;
        box-shadow: 0 3px 12px rgba(34, 197, 94, 0.12) !important;
        box-sizing: border-box !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        animation: kpiFadeIn 0.55s ease both;
    }

    .kpi-card:hover {
        background: #DCFCE7 !important;
        transform: translateY(-5px) scale(1.01) !important;
        box-shadow: 0 10px 24px rgba(34, 197, 94, 0.22) !important;
    }

    .kpi-title {
        color: #166534 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        line-height: 1.5 !important;
    }

    .kpi-value {
        color: #15803D !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
        overflow-wrap: anywhere !important;
    }

    @keyframes kpiFadeIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Date filter */
    [data-testid="stDateInput"] label {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stDateInput"] input {
        color: #000000 !important;
        background: #FFFFFF !important;
    }

    /* =====================================================
       TABLE THEME
       White background + black text + green grid lines
       ===================================================== */

    /* Table wrapper */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background: #FFFFFF !important;
        border: 2px solid #22C55E !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 3px 12px rgba(34, 197, 94, 0.08) !important;
        width: 100% !important;
    }

    /* Streamlit dataframe grid container */
    [data-testid="stDataFrame"] > div,
    [data-testid="stDataFrame"] iframe {
        background: #FFFFFF !important;
    }

    /* Remove dark header and replace with light green */
    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stDataFrame"] [role="columnheader"] *,
    [data-testid="stDataFrame"] [role="columnheader"] div {
        background-color: #F0FDF4 !important;
        color: #166534 !important;
        border-right: 1px solid #22C55E !important;
        border-bottom: 2px solid #22C55E !important;
        font-weight: 700 !important;
    }

    /* Body cells */
    [data-testid="stDataFrame"] [role="gridcell"],
    [data-testid="stDataFrame"] [role="gridcell"] * {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-right: 1px solid #22C55E !important;
        border-bottom: 1px solid #86EFAC !important;
    }

    /* Dataframe row hover */
    [data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"],
    [data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] * {
        background-color: #F0FDF4 !important;
        color: #000000 !important;
    }

    /* Static HTML table */
    [data-testid="stTable"] table {
        background-color: #FFFFFF !important;
        border-collapse: collapse !important;
        border-spacing: 0 !important;
        width: 100% !important;
        border: 1px solid #22C55E !important;
    }

    [data-testid="stTable"] thead th {
        background-color: #F0FDF4 !important;
        color: #166534 !important;
        font-weight: 700 !important;
        border: 1px solid #22C55E !important;
        padding: 12px !important;
    }

    [data-testid="stTable"] tbody td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #22C55E !important;
        padding: 10px 12px !important;
    }

    [data-testid="stTable"] tbody tr:hover td {
        background-color: #F0FDF4 !important;
        color: #000000 !important;
    }

    /* Table toolbar controls */
    [data-testid="stDataFrame"] button {
        color: #166534 !important;
        background: #FFFFFF !important;
    }

    /* Plotly chart text */
    .js-plotly-plot .gtitle,
    .js-plotly-plot .xtitle,
    .js-plotly-plot .ytitle,
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .legend text,
    .js-plotly-plot .annotation-text {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* Responsive layout */
    @media (max-width: 900px) {
        .block-container {
            padding: 3rem 1rem 1.5rem 1rem !important;
        }

        .dashboard-title {
            font-size: 27px !important;
        }

        .kpi-value {
            font-size: 22px !important;
        }
    }

    @media (max-width: 600px) {
        .block-container {
            padding: 2.5rem 0.7rem 1rem 0.7rem !important;
        }

        .dashboard-title {
            font-size: 23px !important;
        }

        .dashboard-caption {
            font-size: 14px !important;
        }

        section[data-testid="stSidebar"] .stButton button {
            min-height: 52px !important;
            height: 52px !important;
            font-size: 15px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 4. NAVIGATION
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "Overall"


def navigate_to(page_name):
    st.session_state.page = page_name


navigation_items = [
    ("📊", "Overall"),
    ("🚘", "Vehicle Type"),
    ("₹", "Revenue"),
    ("🚕", "Cancellation"),
    ("⭐", "Ratings"),
]

# =========================================================
# 5. SIDEBAR: LOGO AND NAVIGATION
# =========================================================
with st.sidebar:
    if LOGO_PATH.is_file():
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            background = Image.new("RGBA", logo.size, (255, 255, 255, 255))
            background.alpha_composite(logo)
            st.image(background.convert("RGB"), use_container_width=True)
        except Exception:
            st.markdown(
                '<div class="logo-fallback">OLA</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="logo-fallback">OLA</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sidebar-section-label">RIDE ANALYTICS</div>',
        unsafe_allow_html=True,
    )

    for icon, label in navigation_items:
        st.button(
            f"{icon}   {label}",
            key=f"nav_{label}",
            type=(
                "primary"
                if st.session_state.page == label
                else "secondary"
            ),
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )

# =========================================================
# 6. LOAD DATASET
# =========================================================
@st.cache_data(show_spinner=False)
def load_csv(file_path):
    data = pd.read_csv(file_path)
    data.columns = [str(column).strip() for column in data.columns]
    return data


csv_path = next((path for path in DATA_PATHS if path.is_file()), None)

if csv_path is None:
    st.error(
        "Bookings_Cleaned.csv was not found. "
        "Place it in the same folder as app.py or update DATA_PATHS."
    )
    st.stop()

try:
    df = load_csv(str(csv_path))
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

# =========================================================
# 7. DATA PREPARATION
# =========================================================
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

numeric_columns = [
    "Booking_Value",
    "Ride_Distance",
    "Customer_Rating",
    "Driver_Ratings",
    "V_TAT",
    "C_TAT",
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

if "Booking_ID" in df.columns:
    df = df.drop_duplicates(subset=["Booking_ID"]).copy()

if "Booking_Status" in df.columns:
    df["Booking_Status"] = (
        df["Booking_Status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace("cancelled", "canceled", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )

# =========================================================
# 8. HELPER FUNCTIONS
# =========================================================
def successful_rows(data):
    if "Booking_Status" not in data.columns:
        return data.iloc[0:0]

    return data[data["Booking_Status"].eq("success")]


def status_count(data, phrase):
    if "Booking_Status" not in data.columns:
        return 0

    phrase = phrase.lower().replace("cancelled", "canceled")

    return int(
        data["Booking_Status"]
        .astype("string")
        .str.contains(phrase, case=False, na=False, regex=False)
        .sum()
    )


def booking_count(data):
    if "Booking_ID" in data.columns:
        return int(data["Booking_ID"].nunique())
    return len(data)


def money(value):
    if pd.isna(value):
        return "N/A"
    return f"₹{value:,.2f}"


def format_value(value):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        if isinstance(value, float) and not value.is_integer():
            return f"{value:,.2f}"
        return f"{value:,.0f}"

    return str(value)


def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{escape(str(title))}</div>
            <div class="kpi-value">{escape(format_value(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpis(metrics, columns_count=3):
    columns = st.columns(columns_count)

    for index, (label, value) in enumerate(metrics):
        with columns[index % columns_count]:
            kpi_card(label, value)

    st.markdown(
        '<div style="height:24px;width:100%;"></div>',
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        autosize=True,
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        margin=dict(l=45, r=25, t=65, b=45),
        font=dict(
            family="Arial, sans-serif",
            size=13,
            color=BLACK,
        ),
        title=dict(
            font=dict(size=20, color=BLACK),
            x=0.02,
            xanchor="left",
        ),
        xaxis=dict(
            title_font=dict(size=14, color=BLACK),
            tickfont=dict(size=12, color=BLACK),
            gridcolor="#E3E7ED",
        ),
        yaxis=dict(
            title_font=dict(size=14, color=BLACK),
            tickfont=dict(size=12, color=BLACK),
            gridcolor="#E3E7ED",
        ),
        legend=dict(font=dict(color=BLACK)),
    )
    return fig


def show_chart(fig, height=380):
    st.plotly_chart(
        chart_layout(fig, height),
        use_container_width=True,
        config={"responsive": True, "displaylogo": False},
    )


def styled_table(data):
    """White cells, black text, green grid lines and green-tinted headers."""
    return (
        data.style
        .set_properties(
            **{
                "background-color": "#FFFFFF",
                "color": "#000000",
                "border": "1px solid #22C55E",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "table",
                    "props": [
                        ("background-color", "#FFFFFF"),
                        ("border-collapse", "collapse"),
                        ("border-spacing", "0"),
                        ("border", "2px solid #22C55E"),
                        ("width", "100%"),
                    ],
                },
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#F0FDF4"),
                        ("color", "#166534"),
                        ("font-weight", "bold"),
                        ("border", "1px solid #22C55E"),
                        ("padding", "10px"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", "#FFFFFF"),
                        ("color", "#000000"),
                        ("border", "1px solid #22C55E"),
                        ("padding", "9px"),
                    ],
                },
            ]
        )
    )


def show_table(data):
    st.dataframe(
        styled_table(data),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 9. DATE RANGE FILTER ONLY
# =========================================================
filtered = df.copy()

with st.sidebar:
    st.markdown("### Filters")

    if "Date" in filtered.columns and filtered["Date"].notna().any():
        min_date = filtered["Date"].min().date()
        max_date = filtered["Date"].max().date()

        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_filter",
        )

        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range

            filtered = filtered[
                filtered["Date"].notna()
                & (filtered["Date"].dt.date >= start_date)
                & (filtered["Date"].dt.date <= end_date)
            ]
    else:
        st.warning("The dataset has no valid Date values.")

# =========================================================
# 10. DASHBOARD HEADER
# =========================================================
page = st.session_state.page

st.markdown(
    f"""
    <div class="dashboard-title">
        OLA Ride Data Analysis — {escape(page)}
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No records match the selected date range.")
    st.stop()

successful = successful_rows(filtered)

# =========================================================
# 11. OVERALL PAGE
# =========================================================
if page == "Overall":
    metrics = [
        ("Total Bookings", booking_count(filtered)),
        ("Successful Bookings", status_count(filtered, "success")),
        ("Canceled by Customer", status_count(filtered, "canceled by customer")),
        ("Canceled by Driver", status_count(filtered, "canceled by driver")),
        ("Driver Not Found", status_count(filtered, "driver not found")),
    ]

    show_kpis(metrics, columns_count=5)

    left, right = st.columns(2)

    with left:
        if "Vehicle_Type" in filtered.columns:
            counts = (
                filtered.groupby("Vehicle_Type", dropna=False)
                .size()
                .reset_index(name="Total Bookings")
            )

            fig = px.bar(
                counts,
                x="Vehicle_Type",
                y="Total Bookings",
                title="Bookings by Vehicle Type",
                color_discrete_sequence=[GREEN],
            )
            show_chart(fig)

    with right:
        if "Booking_Status" in filtered.columns:
            counts = (
                filtered["Booking_Status"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Booking Status")
                .reset_index(name="Bookings")
            )

            fig = px.pie(
                counts,
                names="Booking Status",
                values="Bookings",
                hole=0.5,
                title="Booking Status Distribution",
                color_discrete_sequence=[
                    GREEN, BLUE, "#F97316", "#EF343D", "#9333EA"
                ],
            )
            fig.update_traces(
                textposition="outside",
                textinfo="value+percent",
            )
            show_chart(fig)

    if "Date" in filtered.columns and not successful.empty:
        daily = (
            successful.groupby("Date")
            .size()
            .reset_index(name="Successful Bookings")
        )

        fig = px.line(
            daily,
            x="Date",
            y="Successful Bookings",
            title="Daily Successful Booking Trend",
        )
        fig.update_traces(line=dict(color=GREEN, width=3))
        show_chart(fig, 420)

# =========================================================
# 12. VEHICLE TYPE PAGE
# =========================================================
elif page == "Vehicle Type":
    if "Vehicle_Type" not in filtered.columns:
        st.info("Vehicle_Type column is missing.")
    else:
        vehicle_count = filtered["Vehicle_Type"].nunique()

        total_value = (
            filtered["Booking_Value"].sum()
            if "Booking_Value" in filtered.columns else 0
        )

        average_distance = (
            successful["Ride_Distance"].mean()
            if "Ride_Distance" in successful.columns and not successful.empty
            else 0
        )

        average_customer_rating = (
            successful["Customer_Rating"].mean()
            if "Customer_Rating" in successful.columns and not successful.empty
            else 0
        )

        show_kpis(
            [
                ("Vehicle Types", vehicle_count),
                ("Total Booking Value", money(total_value)),
                ("Successful Bookings", len(successful)),
                ("Average Ride Distance", average_distance),
                ("Average Customer Rating", average_customer_rating),
            ],
            columns_count=5,
        )

        summary = (
            filtered.groupby("Vehicle_Type", dropna=False)
            .size()
            .reset_index(name="Total Bookings")
        )

        measures = [
            ("Booking_Value", "Total Booking Value", "sum", filtered),
            ("Ride_Distance", "Total Ride Distance", "sum", filtered),
            ("Ride_Distance", "Average Ride Distance", "mean", successful),
            ("Customer_Rating", "Average Customer Rating", "mean", successful),
            ("Driver_Ratings", "Average Driver Rating", "mean", successful),
        ]

        for column, label, operation, source in measures:
            if column in source.columns and not source.empty:
                result = (
                    source.groupby("Vehicle_Type")[column]
                    .agg(operation)
                    .rename(label)
                )
                summary = summary.merge(
                    result,
                    on="Vehicle_Type",
                    how="left",
                )

        st.subheader("Vehicle Type Summary")
        show_table(summary.round(2))

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                summary,
                x="Vehicle_Type",
                y="Total Bookings",
                title="Total Bookings by Vehicle Type",
                color_discrete_sequence=[GREEN],
            )
            show_chart(fig)

        with right:
            if "Average Ride Distance" in summary.columns:
                fig = px.bar(
                    summary,
                    x="Vehicle_Type",
                    y="Average Ride Distance",
                    title="Average Ride Distance by Vehicle",
                    color_discrete_sequence=[GREEN],
                )
                show_chart(fig)

# =========================================================
# 13. REVENUE PAGE
# =========================================================
elif page == "Revenue":
    if "Booking_Value" not in filtered.columns:
        st.info("Booking_Value column is missing.")
    else:
        total_value = filtered["Booking_Value"].sum()

        successful_value = (
            successful["Booking_Value"].sum()
            if not successful.empty else 0
        )

        average_successful_value = (
            successful["Booking_Value"].mean()
            if not successful.empty else 0
        )

        show_kpis(
            [
                ("Total Booking Value", money(total_value)),
                ("Successful Booking Value", money(successful_value)),
                ("Average Successful Booking Value", money(average_successful_value)),
            ],
            columns_count=3,
        )

        if "Date" in filtered.columns and filtered["Date"].notna().any():
            daily = (
                filtered.groupby("Date")["Booking_Value"]
                .sum()
                .reset_index()
            )

            fig = px.line(
                daily,
                x="Date",
                y="Booking_Value",
                title="Booking Value by Day",
            )
            fig.update_traces(line=dict(color=GREEN, width=3))
            show_chart(fig, 430)

        left, right = st.columns(2)

        with left:
            if "Vehicle_Type" in successful.columns and not successful.empty:
                by_vehicle = (
                    successful.groupby("Vehicle_Type")["Booking_Value"]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    by_vehicle,
                    x="Vehicle_Type",
                    y="Booking_Value",
                    title="Successful Booking Value by Vehicle",
                    color_discrete_sequence=[GREEN],
                )
                show_chart(fig)

        with right:
            if "Payment_Method" in filtered.columns:
                by_payment = (
                    filtered.groupby("Payment_Method", dropna=False)["Booking_Value"]
                    .sum()
                    .reset_index()
                )

                by_payment["Payment_Method"] = (
                    by_payment["Payment_Method"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                by_payment = by_payment[
                    by_payment["Payment_Method"].ne("")
                    & by_payment["Payment_Method"].str.lower().ne("unknown")
                ]

                if not by_payment.empty:
                    fig = px.pie(
                        by_payment,
                        names="Payment_Method",
                        values="Booking_Value",
                        hole=0.5,
                        title="Booking Value by Payment Method",
                        color_discrete_sequence=[
                            GREEN, "#F97316", "#9333EA", BLUE
                        ],
                    )
                    fig.update_traces(
                        textposition="outside",
                        textinfo="percent",
                    )
                    show_chart(fig)
                else:
                    st.info("No recognized payment methods are available.")

# =========================================================
# 14. CANCELLATION PAGE
# =========================================================
elif page == "Cancellation":
    if "Booking_Status" not in filtered.columns:
        st.info("Booking_Status column is missing.")
    else:
        customer_cancel = filtered[
            filtered["Booking_Status"].astype(str).str.contains(
                "canceled by customer",
                case=False,
                na=False,
            )
        ]

        driver_cancel = filtered[
            filtered["Booking_Status"].astype(str).str.contains(
                "canceled by driver",
                case=False,
                na=False,
            )
        ]

        driver_not_found = status_count(filtered, "driver not found")
        total_cancellations = len(customer_cancel) + len(driver_cancel)

        cancellation_rate = (
            total_cancellations / len(filtered) * 100
            if len(filtered) else 0
        )

        show_kpis(
            [
                ("Canceled by Customer", len(customer_cancel)),
                ("Canceled by Driver", len(driver_cancel)),
                ("Driver Not Found", driver_not_found),
                ("Total Cancellations", total_cancellations),
                ("Cancellation Rate (%)", cancellation_rate),
            ],
            columns_count=5,
        )

        left, right = st.columns(2)

        with left:
            counts = (
                filtered["Booking_Status"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Booking Status")
                .reset_index(name="Bookings")
            )

            fig = px.pie(
                counts,
                names="Booking Status",
                values="Bookings",
                hole=0.5,
                title="Booking Status Distribution",
            )
            show_chart(fig)

        with right:
            if (
                "Date" in filtered.columns
                and (not customer_cancel.empty or not driver_cancel.empty)
            ):
                customer_daily = (
                    customer_cancel.groupby("Date")
                    .size()
                    .rename("Canceled by Customer")
                )

                driver_daily = (
                    driver_cancel.groupby("Date")
                    .size()
                    .rename("Canceled by Driver")
                )

                daily = (
                    pd.concat([customer_daily, driver_daily], axis=1)
                    .fillna(0)
                    .reset_index()
                )

                daily_long = daily.melt(
                    id_vars="Date",
                    var_name="Cancellation Type",
                    value_name="Bookings",
                )

                fig = px.line(
                    daily_long,
                    x="Date",
                    y="Bookings",
                    color="Cancellation Type",
                    title="Daily Cancellation Trend",
                    color_discrete_sequence=[GREEN, DARK_GREEN],
                )
                show_chart(fig)

        left, right = st.columns(2)

        reason_columns = [
            (
                left,
                "Canceled_Rides_by_Customer",
                customer_cancel,
                "Customer Cancellation Reasons",
            ),
            (
                right,
                "Canceled_Rides_by_Driver",
                driver_cancel,
                "Driver Cancellation Reasons",
            ),
        ]

        for col, column, source, title in reason_columns:
            with col:
                if column in source.columns:
                    reasons = (
                        source[column]
                        .dropna()
                        .astype(str)
                        .value_counts()
                        .reset_index()
                    )

                    reasons.columns = ["Cancellation Reason", "Bookings"]

                    if not reasons.empty:
                        fig = px.bar(
                            reasons,
                            x="Bookings",
                            y="Cancellation Reason",
                            orientation="h",
                            title=title,
                            color_discrete_sequence=[GREEN],
                        )
                        show_chart(fig, 400)
                    else:
                        st.info(f"No data available for {title.lower()}.")

# =========================================================
# 15. RATINGS PAGE
# =========================================================
elif page == "Ratings":
    if "Vehicle_Type" not in filtered.columns:
        st.info("Vehicle_Type column is missing.")
    else:
        average_customer_rating = (
            successful["Customer_Rating"].mean()
            if "Customer_Rating" in successful.columns and not successful.empty
            else 0
        )

        average_driver_rating = (
            successful["Driver_Ratings"].mean()
            if "Driver_Ratings" in successful.columns and not successful.empty
            else 0
        )

        customer_rating_count = (
            successful["Customer_Rating"].notna().sum()
            if "Customer_Rating" in successful.columns else 0
        )

        driver_rating_count = (
            successful["Driver_Ratings"].notna().sum()
            if "Driver_Ratings" in successful.columns else 0
        )

        show_kpis(
            [
                ("Average Customer Rating", average_customer_rating),
                ("Average Driver Rating", average_driver_rating),
                ("Successful Bookings", len(successful)),
                ("Customer Ratings Recorded", customer_rating_count),
                ("Driver Ratings Recorded", driver_rating_count),
            ],
            columns_count=5,
        )

        rating_columns = [
            column
            for column in ["Customer_Rating", "Driver_Ratings"]
            if column in successful.columns
        ]

        if successful.empty or not rating_columns:
            st.info("No successful rides or rating columns are available.")
        else:
            ratings = (
                successful.groupby("Vehicle_Type")[rating_columns]
                .mean()
                .reset_index()
                .rename(
                    columns={
                        "Customer_Rating": "Average Customer Rating",
                        "Driver_Ratings": "Average Driver Rating",
                    }
                )
                .round(2)
            )

            st.subheader("Average Ratings by Vehicle Type")
            show_table(ratings)

            ratings_long = ratings.melt(
                id_vars="Vehicle_Type",
                var_name="Rating Type",
                value_name="Average Rating",
            )

            fig = px.bar(
                ratings_long,
                x="Vehicle_Type",
                y="Average Rating",
                color="Rating Type",
                barmode="group",
                title="Customer and Driver Ratings",
                color_discrete_sequence=[GREEN, DARK_GREEN],
            )
            fig.update_yaxes(range=[0, 5])
            show_chart(fig, 420)

# =========================================================
# 16. FOOTER
# =========================================================
st.divider()
