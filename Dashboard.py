import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="Email Content Monitoring Dashboard",
    layout="wide"
)

# ==========================================
# Page title
# ==========================================

st.markdown(
    """
    <h1 style="color: #D71920;">
        Email Content Monitoring Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# ==========================================
# Read Excel file
# ==========================================

df = pd.read_excel("mock_database_with_gemini_results.xlsx")

# Create permanent record number
df.insert(0, "No.", range(1, len(df) + 1))

# Clean department names
df["department"] = df["department"].str.strip().str.title()

# ==========================================
# Create AI_reason column if missing
# ==========================================

if "AI_reason" not in df.columns:
    df["AI_reason"] = ""

# ==========================================
# Filters
# ==========================================

st.sidebar.header("Filters")

# ------------------------------------------
# Email ID filter
# ------------------------------------------

email_id_values = (
    df["email_id"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

email_id_options = ["All"] + sorted(email_id_values)

selected_email_id = st.sidebar.selectbox(
    "Email ID",
    email_id_options,
    key="email_id_filter"
)

# ------------------------------------------
# Department filter
# ------------------------------------------

department_options = ["All Departments"] + sorted(
    df["department"].dropna().unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    department_options,
    key="department_filter"
)

# ------------------------------------------
# Result filter
# ------------------------------------------

result_options = ["All", "Green", "Amber", "Red"]

selected_result = st.sidebar.selectbox(
    "Result",
    result_options,
    key="result_filter"
)

# ------------------------------------------
# Midnight filter
# ------------------------------------------

midnight_options = ["All", "Yes", "No"]

selected_midnight = st.sidebar.selectbox(
    "Midnight Email",
    midnight_options,
    key="midnight_filter"
)

# ------------------------------------------
# Policy Triggered filter
# ------------------------------------------

policy_values = (
    df["policy_triggered"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

policy_options = ["All"] + sorted(policy_values)

selected_policy = st.sidebar.selectbox(
    "Policy Triggered",
    policy_options,
    key="policy_filter"
)

# ------------------------------------------
# Rules Triggered filter
# ------------------------------------------

rules_values = (
    df["rules_triggered"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

rules_options = ["All"] + sorted(rules_values)

selected_rules = st.sidebar.selectbox(
    "Rules Triggered",
    rules_options,
    key="rules_filter"
)

# ------------------------------------------
# Severity filter
# ------------------------------------------

severity_values = (
    df["severity"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

severity_options = ["All"] + sorted(severity_values)

selected_severity = st.sidebar.selectbox(
    "Severity",
    severity_options,
    key="severity_filter"
)


# ==========================================
# Apply Filters
# ==========================================

filtered_df = df.copy()

# ------------------------------------------
# Email ID
# ------------------------------------------

if selected_email_id != "All":
    filtered_df = filtered_df[
        filtered_df["email_id"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_email_id
    ]

# ------------------------------------------
# Department
# ------------------------------------------

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["department"] == selected_department
    ]

# ------------------------------------------
# Result
# ------------------------------------------

if selected_result != "All":
    filtered_df = filtered_df[
        filtered_df["expected_result"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_result
    ]

# ------------------------------------------
# Midnight
# ------------------------------------------

if selected_midnight != "All":
    filtered_df = filtered_df[
        filtered_df["midnight"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.title()
        == selected_midnight
    ]

# ------------------------------------------
# Policy Triggered
# ------------------------------------------

if selected_policy != "All":
    filtered_df = filtered_df[
        filtered_df["policy_triggered"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_policy
    ]

# ------------------------------------------
# Rules Triggered
# ------------------------------------------

if selected_rules != "All":
    filtered_df = filtered_df[
        filtered_df["rules_triggered"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_rules
    ]

# ------------------------------------------
# Severity
# ------------------------------------------

if selected_severity != "All":
    filtered_df = filtered_df[
        filtered_df["severity"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_severity
    ]


# ==========================================
# Email Monitoring Results
# ==========================================

st.subheader("Email Monitoring Results")

# ==========================================
# Calculate counts
# ==========================================

total_emails = len(filtered_df)

green_count = (
    filtered_df["expected_result"] == "Green"
).sum()

amber_count = (
    filtered_df["expected_result"] == "Amber"
).sum()

red_count = (
    filtered_df["expected_result"] == "Red"
).sum()

# ==========================================
# Display four monitoring cards
# ==========================================

# Add CSS for the monitoring cards
st.markdown("""
<style>

.monitor-card {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-sizing: border-box;
    width: 100%;
    min-height: 170px;
}

.monitor-title {
    font-size: 22px;
    font-weight: 600;
    margin: 0;
    text-align: center;
}

.monitor-number {
    font-size: 42px;
    font-weight: 700;
    margin: 10px 0;
    text-align: center;
}

.monitor-label {
    font-size: 16px;
    margin: 0;
    text-align: center;
}

.total-card {
    background-color: #E3F2FD;
    border-left: 8px solid #1565C0;
}

.total-card .monitor-title,
.total-card .monitor-number {
    color: #1565C0;
}

.total-card .monitor-label {
    color: #333333;
}

.green-card {
    background-color: #E8F5E9;
    border-left: 8px solid #2E7D32;
}

.green-card .monitor-title,
.green-card .monitor-number {
    color: #2E7D32;
}

.green-card .monitor-label {
    color: #333333;
}

.amber-card {
    background-color: #FFF8E1;
    border-left: 8px solid #F9A825;
}

.amber-card .monitor-title,
.amber-card .monitor-number {
    color: #F9A825;
}

.amber-card .monitor-label {
    color: #333333;
}

.red-card {
    background-color: #FFEBEE;
    border-left: 8px solid #C62828;
}

.red-card .monitor-title,
.red-card .monitor-number {
    color: #C62828;
}

.red-card .monitor-label {
    color: #333333;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# Create four columns
# ==========================================

col1, spacer1, col2, spacer2, col3, spacer3, col4 = st.columns(
    [1, 0.08, 1, 0.08, 1, 0.08, 1]
)


# ==========================================
# Total Emails
# ==========================================

with col1:
    st.markdown(
        f"""
        <div class="monitor-card total-card">
            <div class="monitor-title">Total Emails</div>
            <div class="monitor-number">{total_emails}</div>
            <div class="monitor-label">Emails</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# Green
# ==========================================

with col2:
    st.markdown(
        f"""
        <div class="monitor-card green-card">
            <div class="monitor-title">Green</div>
            <div class="monitor-number">{green_count}</div>
            <div class="monitor-label">Emails</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# Amber
# ==========================================

with col3:
    st.markdown(
        f"""
        <div class="monitor-card amber-card">
            <div class="monitor-title">Amber</div>
            <div class="monitor-number">{amber_count}</div>
            <div class="monitor-label">Emails</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# Red
# ==========================================

with col4:
    st.markdown(
        f"""
        <div class="monitor-card red-card">
            <div class="monitor-title">Red</div>
            <div class="monitor-number">{red_count}</div>
            <div class="monitor-label">Emails</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# Space between monitoring cards and filters
# ==========================================

st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

# ==========================================
# Table Filters
# ==========================================

filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

with filter_col1:
    pii_filter = st.selectbox(
        "PII Verdict",
        ["All", "Yes", "No"]
    )

with filter_col2:
    transaction_filter = st.selectbox(
        "Transaction Verdict",
        ["All", "Yes", "No"]
    )

with filter_col3:
    credential_filter = st.selectbox(
        "Credential Verdict",
        ["All", "Yes", "No"]
    )

with filter_col4:
    health_filter = st.selectbox(
        "Health Data Verdict",
        ["All", "Yes", "No"]
    )

with filter_col5:
    result_filter = st.selectbox(
        "Result",
        ["All", "Green", "Amber", "Red"]
    )

# ==========================================
# Space between filters and table
# ==========================================

st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

# ==========================================
# Apply Table Filters
# ==========================================

table_df = filtered_df.copy()

if pii_filter != "All":
    if pii_filter == "Yes":
        table_df = table_df[
            table_df["PII_flag"].fillna("").str.strip() == "Yes"
        ]
    else:
        table_df = table_df[
            table_df["PII_flag"].fillna("").str.strip() != "Yes"
        ]

if transaction_filter != "All":
    if transaction_filter == "Yes":
        table_df = table_df[
            table_df["transaction_flag"].fillna("").str.strip() == "Yes"
        ]
    else:
        table_df = table_df[
            table_df["transaction_flag"].fillna("").str.strip() != "Yes"
        ]

if credential_filter != "All":
    if credential_filter == "Yes":
        table_df = table_df[
            table_df["credential_flag"].fillna("").str.strip() == "Yes"
        ]
    else:
        table_df = table_df[
            table_df["credential_flag"].fillna("").str.strip() != "Yes"
        ]

if health_filter != "All":
    if health_filter == "Yes":
        table_df = table_df[
            table_df["health_flag"].fillna("").str.strip() == "Yes"
        ]
    else:
        table_df = table_df[
            table_df["health_flag"].fillna("").str.strip() != "Yes"
        ]

if result_filter != "All":
    table_df = table_df[
        table_df["expected_result"] == result_filter
    ]

# ==========================================
# Create display table
# ==========================================

display_df = table_df[
    [
        "No.",
        "email_id",
        "subject",
        "recipient_email",
        "PII_flag",
        "transaction_flag",
        "credential_flag",
        "health_flag",
        "intended_recipient",
        "expected_result",
        "AI_reason"
    ]
].copy()


# ==========================================
# Rename columns for dashboard display
# ==========================================

display_df = display_df.rename(
    columns={
        "email_id": "Email ID",
        "subject": "Subject",
        "recipient_email": "Recipient",
        "PII_flag": "PII Verdict",
        "transaction_flag": "Transaction Verdict",
        "credential_flag": "Authentication Credential Verdict",
        "health_flag": "Health Data Verdict",
        "intended_recipient": "Intended Recipient",
        "expected_result": "Result",
        "AI_reason": "AI Reason"
    }
)

# ==========================================
# Colour-code Result column
# ==========================================

def colour_result(value):

    if value == "Green":
        return "background-color: #2E7D32; color: white; font-weight: bold"

    elif value == "Amber":
        return "background-color: #F9A825; color: black; font-weight: bold"

    elif value == "Red":
        return "background-color: #C62828; color: white; font-weight: bold"

    return ""

# ==========================================
# Style display table
# ==========================================

styled_df = (
    display_df.style
    .hide(axis="index")

    # ======================================
    # Colour Result column
    # ======================================
    .map(
        colour_result,
        subset=["Result"]
    )

    # ======================================
    # General body properties
    # ======================================
    .set_properties(
        **{
            "font-size": "17px",
            "font-family": "Arial, sans-serif",
            "white-space": "normal",
            "word-wrap": "break-word",
            "overflow-wrap": "break-word",
            "word-break": "normal",
            "vertical-align": "top",
            "padding": "14px 12px",
            "line-height": "1.5"
        }
    )

    # ======================================
    # Email ID - CENTER ALIGN
    # ======================================
    .set_properties(
        subset=["Email ID"],
        **{
            "text-align": "center",
            "vertical-align": "middle"
        }
    )

    # ======================================
    # Table styles
    # ======================================
    .set_table_styles(
        [

            # ======================================
            # Entire table
            # ======================================
            {
                "selector": "table",
                "props": [
                    ("width", "100%"),
                    ("table-layout", "fixed"),
                    ("border-collapse", "collapse"),
                    ("font-size", "17px")
                ]
            },

            # ======================================
            # Header
            # ======================================
            {
                "selector": "thead th",
                "props": [
                    ("background-color", "#D71920"),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("font-size", "17px"),
                    ("text-align", "center"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word"),
                    ("overflow-wrap", "break-word"),
                    ("padding", "15px 10px"),
                    ("line-height", "1.4"),
                    ("border", "1px solid #B5121B")
                ]
            },

            # ======================================
            # Body cells
            # ======================================
            {
                "selector": "tbody td",
                "props": [
                    ("font-size", "17px"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word"),
                    ("overflow-wrap", "break-word"),
                    ("word-break", "normal"),
                    ("vertical-align", "middle"),
                    ("padding", "14px 12px"),
                    ("line-height", "1.5"),
                    ("border", "1px solid #dddddd")
                ]
            },

            # ======================================
            # No.
            # ======================================
            {
                "selector": "th:nth-child(1), td:nth-child(1)",
                "props": [
                    ("width", "4%"),
                    ("min-width", "40px"),
                    ("max-width", "55px"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("padding", "8px 4px")
                ]
            },

            # ======================================
            # Email ID
            # ======================================
            {
                "selector": "th:nth-child(2), td:nth-child(2)",
                "props": [
                    ("width", "6%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("padding", "8px 4px")
                ]
            },

            # ======================================
            # Subject
            # ======================================
            {
                "selector": "th:nth-child(3), td:nth-child(3)",
                "props": [
                    ("width", "14%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word")
                ]
            },

            # ======================================
            # Recipient
            # ======================================
            {
                "selector": "th:nth-child(4), td:nth-child(4)",
                "props": [
                    ("width", "13%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word")
                ]
            },

            # ======================================
            # PII
            # ======================================
            {
                "selector": "th:nth-child(5), td:nth-child(5)",
                "props": [
                    ("width", "7%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle")
                ]
            },

            # ======================================
            # Transaction
            # ======================================
            {
                "selector": "th:nth-child(6), td:nth-child(6)",
                "props": [
                    ("width", "9%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle")
                ]
            },

            # ======================================
            # Credential
            # ======================================
            {
                "selector": "th:nth-child(7), td:nth-child(7)",
                "props": [
                    ("width", "12%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word")
                ]
            },

            # ======================================
            # Health
            # ======================================
            {
                "selector": "th:nth-child(8), td:nth-child(8)",
                "props": [
                    ("width", "9%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle")
                ]
            },

            # ======================================
            # Intended Recipient
            # ======================================
            {
                "selector": "th:nth-child(9), td:nth-child(9)",
                "props": [
                    ("width", "10%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word")
                ]
            },

            # ======================================
            # Result
            # ======================================
            {
                "selector": "th:nth-child(10), td:nth-child(10)",
                "props": [
                    ("width", "7%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle")
                ]
            },

            # ======================================
            # AI Reason
            # ======================================
            {
                "selector": "th:nth-child(11), td:nth-child(11)",
                "props": [
                    ("width", "9%"),
                    ("text-align", "center"),
                    ("vertical-align", "middle"),
                    ("white-space", "normal"),
                    ("word-wrap", "break-word"),
                    ("overflow-wrap", "break-word")
                ]
            }
        ]
    )
)

# ==========================================
# Convert styled dataframe to HTML
# ==========================================

table_html = styled_df.to_html(
    index=False,
    escape=False
)

# ==========================================
# Display table
# ==========================================

st.markdown(
    table_html,
    unsafe_allow_html=True
)