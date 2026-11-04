import streamlit as st
import sqlite3
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Hotel Reservation System", page_icon="🏨", layout="wide")

st.title("🏨 Hotel Reservation Management Panel")
st.write("Welcome to the smart hotel management system for our project, kanka!")

# Database connection function
def get_connection():
    return sqlite3.connect('hotel.db')

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Select Menu", 
    ["Room List & Availability", "Make Reservation", "Customer List", "Advanced Reports & Queries"]
)

conn = get_connection()

if menu == "Room List & Availability":
    st.subheader("🛏️ Available Hotel Rooms")
    df_rooms = pd.read_sql("SELECT * FROM Rooms", conn)
    st.dataframe(df_rooms, use_container_width=True)

elif menu == "Make Reservation":
    st.subheader("📝 Create New Reservation")
    
    customers_df = pd.read_sql("SELECT customer_id, first_name || ' ' || last_name as full_name FROM Customers", conn)
    rooms_df = pd.read_sql("SELECT room_id, room_number || ' - ' || room_type || ' ($' || price || ')' as room_info FROM Rooms WHERE status='Available'", conn)
    
    if not customers_df.empty and not rooms_df.empty:
        selected_customer = st.selectbox("Select Customer", customers_df['full_name'])
        selected_room = st.selectbox("Select Available Room", rooms_df['room_info'])
        
        check_in = st.date_input("Check-in Date")
        check_out = st.date_input("Check-out Date")
        
        if st.button("Confirm Reservation"):
            cust_id = customers_df[customers_df['full_name'] == selected_customer]['customer_id'].values[0]
            room_id = rooms_df[rooms_df['room_info'] == selected_room]['room_id'].values[0]
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Reservations (customer_id, room_id, check_in_date, check_out_date, total_price)
                VALUES (?, ?, ?, ?, ?)
            """, (int(cust_id), int(room_id), str(check_in), str(check_out), 1500.0))
            
            cursor.execute("UPDATE Rooms SET status='Booked' WHERE room_id = ?", (int(room_id),))
            conn.commit()
            st.success("Reservation successfully created! Room status updated.")
    else:
        st.warning("No registered customers or available rooms left in the system!")

elif menu == "Customer List":
    st.subheader("👥 Registered Customers")
    df_customers = pd.read_sql("SELECT * FROM Customers", conn)
    st.dataframe(df_customers, use_container_width=True)

elif menu == "Advanced Reports & Queries":
    st.subheader("📊 SQL Queries & Reports")
    st.write("You can view the relational query outputs from the database in this section.")
    
    # Query 1: Detailed Reservations (JOIN Example)
    st.markdown("### 1. Detailed Reservation List (JOIN Query)")
    query_join = """
        SELECT r.reservation_id, c.first_name || ' ' || c.last_name AS Customer, 
               ro.room_number, ro.room_type, r.check_in_date, r.check_out_date, r.total_price
        FROM Reservations r
        JOIN Customers c ON r.customer_id = c.customer_id
        JOIN Rooms ro ON r.room_id = ro.room_id
    """
    df_join = pd.read_sql(query_join, conn)
    if not df_join.empty:
        st.dataframe(df_join, use_container_width=True)
    else:
        st.info("No reservations made yet. Create a record from the 'Make Reservation' tab first.")

    # Query 2: Room Price and Status Analysis (GROUP BY Example)
    st.markdown("### 2. Room Price and Status Analysis (GROUP BY)")
    query_rooms = """
        SELECT room_type, COUNT(*) AS Room_Count, AVG(price) AS Average_Price 
        FROM Rooms 
        GROUP BY room_type
    """
    df_rooms_analysis = pd.read_sql(query_rooms, conn)
    st.dataframe(df_rooms_analysis, use_container_width=True)

conn.close()