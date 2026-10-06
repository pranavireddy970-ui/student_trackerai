import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT,
    description TEXT,
    category TEXT,
    payment_method TEXT,
    amount REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY,
    monthly_budget REAL
)
""")

conn.commit()

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("💰 Student Expense Tracker")
st.write("Manage your daily expenses and track your student budget.")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📊 Analytics",
        "🎯 Budget",
        "📋 Expense History"
    ]
)

# =========================
# DASHBOARD
# =========================

if menu == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    data = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    if data.empty:
        total = 0
        today_total = 0
        month_total = 0
    else:
        total = data["amount"].sum()

        today_total = data[
            data["expense_date"] == str(date.today())
        ]["amount"].sum()

        current_month = str(date.today())[:7]

        month_total = data[
            data["expense_date"].str.startswith(current_month)
        ]["amount"].sum()

    # Get budget
    budget_data = pd.read_sql_query(
        "SELECT * FROM budget WHERE id = 1",
        conn
    )

    if budget_data.empty:
        monthly_budget = 0
    else:
        monthly_budget = budget_data.iloc[0]["monthly_budget"]

    remaining = monthly_budget - month_total

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Expenses",
        f"₹{total:.2f}"
    )

    col2.metric(
        "📅 Today's Expense",
        f"₹{today_total:.2f}"
    )

    col3.metric(
        "📆 This Month",
        f"₹{month_total:.2f}"
    )

    col4.metric(
        "🎯 Remaining Budget",
        f"₹{remaining:.2f}"
    )

    st.divider()

    st.subheader("📌 Recent Expenses")

    if not data.empty:

        recent = data.sort_values(
            "expense_date",
            ascending=False
        ).head(5)

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No expenses added yet.")

# =========================
# ADD EXPENSE
# =========================

elif menu == "➕ Add Expense":

    st.header("➕ Add New Expense")

    expense_date = st.date_input(
        "Date",
        date.today()
    )

    description = st.text_input(
        "Description",
        placeholder="Example: Lunch"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Education",
            "Shopping",
            "Entertainment",
            "Bills",
            "Other"
        ]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Cash",
            "UPI",
            "Debit Card",
            "Credit Card"
        ]
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    if st.button("💾 Add Expense", type="primary"):

        if description.strip() == "":
            st.warning("Please enter a description.")

        elif amount <= 0:
            st.warning("Please enter a valid amount.")

        else:

            cursor.execute("""
                INSERT INTO expenses
                (expense_date, description, category, payment_method, amount)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(expense_date),
                description,
                category,
                payment_method,
                amount
            ))

            conn.commit()

            st.success("Expense added successfully! ✅")

# =========================
# ANALYTICS
# =========================

elif menu == "📊 Analytics":

    st.header("📊 Expense Analytics")

    data = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    if data.empty:

        st.info("Add some expenses to see analytics.")

    else:

        st.subheader("📌 Spending by Category")

        category_data = data.groupby(
            "category"
        )["amount"].sum()

        fig, ax = plt.subplots()

        category_data.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_ylabel("")

        st.pyplot(fig)

        st.subheader("📈 Expenses by Category")

        fig2, ax2 = plt.subplots()

        category_data.plot(
            kind="bar",
            ax=ax2
        )

        ax2.set_xlabel("Category")
        ax2.set_ylabel("Amount (₹)")

        st.pyplot(fig2)

# =========================
# BUDGET
# =========================

elif menu == "🎯 Budget":

    st.header("🎯 Monthly Budget")

    budget_data = pd.read_sql_query(
        "SELECT * FROM budget WHERE id = 1",
        conn
    )

    current_budget = 0

    if not budget_data.empty:
        current_budget = budget_data.iloc[0]["monthly_budget"]

    budget_amount = st.number_input(
        "Set Monthly Budget (₹)",
        min_value=0.0,
        value=float(current_budget),
        step=500.0
    )

    if st.button("💾 Save Budget"):

        cursor.execute("""
            INSERT OR REPLACE INTO budget
            (id, monthly_budget)
            VALUES (1, ?)
        """, (budget_amount,))

        conn.commit()

        st.success("Monthly budget saved! 🎯")

    data = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    current_month = str(date.today())[:7]

    if data.empty:
        month_expense = 0
    else:
        month_expense = data[
            data["expense_date"].str.startswith(current_month)
        ]["amount"].sum()

    remaining = budget_amount - month_expense

    st.metric(
        "Monthly Budget",
        f"₹{budget_amount:.2f}"
    )

    st.metric(
        "Spent This Month",
        f"₹{month_expense:.2f}"
    )

    st.metric(
        "Remaining",
        f"₹{remaining:.2f}"
    )

    if budget_amount > 0:

        progress = min(
            month_expense / budget_amount,
            1.0
        )

        st.progress(progress)

        if month_expense > budget_amount:
            st.error("⚠️ You have exceeded your monthly budget!")

        elif month_expense >= budget_amount * 0.8:
            st.warning("⚠️ You have used more than 80% of your budget.")

        else:
            st.success("✅ You are within your budget.")

# =========================
# EXPENSE HISTORY
# =========================

elif menu == "📋 Expense History":

    st.header("📋 Expense History")

    data = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY expense_date DESC",
        conn
    )

    if data.empty:

        st.info("No expenses available.")

    else:

        search = st.text_input(
            "🔍 Search Expense"
        )

        if search:

            data = data[
                data["description"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗑️ Delete Expense")

        expense_id = st.number_input(
            "Enter Expense ID",
            min_value=1,
            step=1
        )

        if st.button("Delete"):

            cursor.execute(
                "DELETE FROM expenses WHERE id = ?",
                (expense_id,)
            )

            conn.commit()

            st.success("Expense deleted successfully.")

            st.rerun()

# =========================
# FOOTER
# =========================

st.sidebar.divider()

st.sidebar.caption(
    "Student Expense Tracker"
)

st.sidebar.caption(
    "Python • Streamlit • SQLite"
)