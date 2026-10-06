# Student Expense Tracker

## 📌 Project Description

The **Student Expense Tracker** is a simple web application designed to help students record, manage, and monitor their daily expenses.

It allows students to add expenses, view their spending records, and understand where their money is being spent.

## 🎯 Objectives

* Track daily student expenses
* Store expense details safely
* Categorize expenses
* Calculate total spending
* Help students manage their budget

## 🛠️ Technologies Used

* **Python 3.12** – Main programming language
* **Streamlit** – Web application interface
* **SQLite** – Database for storing expenses

## ✨ Features

* ➕ Add new expenses
* 📋 View expense history
* 🗑️ Delete expenses
* 💰 Calculate total expenses
* 📊 View expenses by category
* 💾 Store data using SQLite

## 📂 Project Structure

```text
Student_Expense_Tracker/
│
├── app.py
├── database.py
├── expenses.db
└── README.md
```

## ⚙️ Installation

### 1. Install Python

Make sure Python 3.12 is installed.

Check the version:

```bash
python --version
```

### 2. Install Streamlit

Open the VS Code terminal and run:

```bash
pip install streamlit
```

### 3. Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your web browser.

## 🗄️ Database

The project uses **SQLite** to store expense information.

SQLite is already included with Python through the `sqlite3` module, so no separate SQLite installation is required.

## 📋 Expense Details

Each expense can contain:

* Expense name
* Amount
* Category
* Date

## 🚀 Future Improvements

* Student login and registration
* Monthly budget setting
* Expense charts and graphs
* Monthly reports
* Export expenses to Excel/CSV
* Expense alerts

## 👩‍💻 Author

**Pranavi**

### Student Expense Tracker

A simple project developed to learn **Python, Streamlit, and SQLite**.
