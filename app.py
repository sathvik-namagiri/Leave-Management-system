import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Leave Management System", layout="wide")

st.title("🚀 Leave Management Dashboard")

menu = st.sidebar.selectbox(
    "Menu",
    ["📊 Dashboard", "👤 Register Employee", "📝 Apply Leave", "📋 View Leaves", "⚙️ Admin"]
)

# ---------------- DASHBOARD ----------------
if menu == "📊 Dashboard":
    st.header("📊 System Overview")

    try:
        res = requests.get(f"{API}/employees/count")
        total = res.json()["total_employees"]

        col1, col2 = st.columns(2)

        col1.metric("👥 Total Employees", total)

        leaves = requests.get(f"{API}/leaves").json()
        col2.metric("📄 Total Leaves", len(leaves))

    except:
        st.error("⚠️ Backend not running")


# ---------------- REGISTER EMPLOYEE ----------------
elif menu == "👤 Register Employee":
    st.header("👤 Employee Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(f"{API}/employees/register", json={
            "name": name,
            "email": email,
            "password": password
        })

        if res.status_code == 201:
            st.success("✅ Employee Registered Successfully")
        else:
            st.error(res.json().get("detail", "Error occurred"))


# ---------------- APPLY LEAVE ----------------
elif menu == "📝 Apply Leave":
    st.header("📝 Apply for Leave")

    try:
        employees = requests.get(f"{API}/employees").json()
        emp_dict = {f"{e['name']} (ID: {e['id']})": e["id"] for e in employees}

        selected = st.selectbox("Select Employee", list(emp_dict.keys()))
        emp_id = emp_dict[selected]

    except:
        st.error("⚠️ Could not fetch employees")
        emp_id = None

    # 🔥 Updated Leave Type Dropdown
    leave_type = st.selectbox(
        "Leave Type",
        ["Casual Leave", "Sick Leave", "Other"]
    )

    # Optional custom input
    if leave_type == "Other":
        leave_type = st.text_input("Enter Leave Type")

    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    reason = st.text_area("Reason")

    if st.button("Submit Leave"):
        if not emp_id:
            st.error("Employee not selected")
        elif end < start:
            st.error("End date cannot be before start date")
        else:
            res = requests.post(f"{API}/apply", json={
                "employee_id": emp_id,
                "leave_type": leave_type,
                "start_date": str(start),
                "end_date": str(end),
                "reason": reason
            })

            if res.status_code == 201:
                st.success("✅ Leave Applied Successfully")
            else:
                st.error(res.json().get("detail", "Error occurred"))


# ---------------- VIEW LEAVES ----------------
elif menu == "📋 View Leaves":
    st.header("📋 All Leave Requests")

    try:
        leaves = requests.get(f"{API}/leaves").json()

        if leaves:
            st.dataframe(leaves)
        else:
            st.info("No leave records found")

    except:
        st.error("⚠️ Backend not reachable")


# ---------------- ADMIN ----------------
elif menu == "⚙️ Admin":
    st.header("⚙️ Approve / Reject Leaves")

    leave_id = st.number_input("Leave ID", step=1)

    col1, col2 = st.columns(2)

    if col1.button("✅ Approve"):
        res = requests.put(f"{API}/approve/{leave_id}")
        st.success(res.json())

    if col2.button("❌ Reject"):
        res = requests.put(f"{API}/reject/{leave_id}")
        st.error(res.json())