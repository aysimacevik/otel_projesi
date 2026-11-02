import streamlit as st
import sqlite3
import pandas as pd

# Sayfa ayarı
st.set_page_config(page_title="Otel Rezervasyon Sistemi", page_icon="🏨", layout="wide")

st.title("🏨 Otel Rezervasyon Yönetim Paneli")
st.write("Proje için hazırladığımız akıllı otel arayüzüne hoş geldin kanka!")

# Veritabanı bağlantısı
def get_connection():
    return sqlite3.connect('hotel.db')

# Sol menü (Sidebar) navigasyonu - Raporlar eklendi!
menu = st.sidebar.selectbox(
    "Menü Seç", 
    ["Oda Listesi & Müsaitlik", "Rezervasyon Yap", "Müşteri Listesi", "Gelişmiş Raporlar & Sorgular"]
)

conn = get_connection()

if menu == "Oda Listesi & Müsaitlik":
    st.subheader("🛏️ Mevcut Otel Odaları")
    df_rooms = pd.read_sql("SELECT * FROM Rooms", conn)
    st.dataframe(df_rooms, use_container_width=True)

elif menu == "Rezervasyon Yap":
    st.subheader("📝 Yeni Rezervasyon Oluştur")
    
    customers_df = pd.read_sql("SELECT customer_id, first_name || ' ' || last_name as full_name FROM Customers", conn)
    rooms_df = pd.read_sql("SELECT room_id, room_number || ' - ' || room_type || ' (' || price || ' TL)' as room_info FROM Rooms WHERE status='Available'", conn)
    
    if not customers_df.empty and not rooms_df.empty:
        selected_customer = st.selectbox("Müşteri Seç", customers_df['full_name'])
        selected_room = st.selectbox("Müsait Oda Seç", rooms_df['room_info'])
        
        check_in = st.date_input("Giriş Tarihi")
        check_out = st.date_input("Çıkış Tarihi")
        
        if st.button("Rezervasyonu Onayla"):
            cust_id = customers_df[customers_df['full_name'] == selected_customer]['customer_id'].values[0]
            room_id = rooms_df[rooms_df['room_info'] == selected_room]['room_id'].values[0]
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Reservations (customer_id, room_id, check_in_date, check_out_date, total_price)
                VALUES (?, ?, ?, ?, ?)
            """, (int(cust_id), int(room_id), str(check_in), str(check_out), 1500.0))
            
            cursor.execute("UPDATE Rooms SET status='Booked' WHERE room_id = ?", (int(room_id),))
            conn.commit()
            st.success("Rezervasyon başarıyla oluşturuldu kanka! Oda durumu güncellendi.")
    else:
        st.warning("Sistemde kayıtlı müşteri veya müsait oda kalmadı!")

elif menu == "Müşteri Listesi":
    st.subheader("👥 Kayıtlı Müşteriler")
    df_customers = pd.read_sql("SELECT * FROM Customers", conn)
    st.dataframe(df_customers, use_container_width=True)

elif menu == "Gelişmiş Raporlar & Sorgular":
    st.subheader("📊 Hocanın İstediği SQL Sorguları ve Raporlar")
    st.write("Bu bölümde veritabanındaki ilişkisel sorguların çıktılarını görebilirsin.")
    
    # Sorgu 1: Aktif Rezervasyonlar ve Müşteri-Oda Detayları (JOIN Örneği)
    st.markdown("### 1. Detaylı Rezervasyon Listesi (JOIN Sorgusu)")
    query_join = """
        SELECT r.reservation_id, c.first_name || ' ' || c.last_name AS Musteri, 
               ro.room_number, ro.room_type, r.check_in_date, r.check_out_date, r.total_price
        FROM Reservations r
        JOIN Customers c ON r.customer_id = c.customer_id
        JOIN Rooms ro ON r.room_id = ro.room_id
    """
    df_join = pd.read_sql(query_join, conn)
    if not df_join.empty:
        st.dataframe(df_join, use_container_width=True)
    else:
        st.info("Henüz yapılan bir rezervasyon yok. Önce 'Rezervasyon Yap' sekmesinden bir kayıt oluşturabilirsin.")

    # Sorgu 2: Otel Bazlı Oda Tipleri ve Fiyat Dağılımı
    st.markdown("### 2. Oda Fiyat ve Durum Analizi")
    query_rooms = """
        SELECT room_type, COUNT(*) AS Oda_Sayisi, AVG(price) AS Ortalama_Fiyat 
        FROM Rooms 
        GROUP BY room_type
    """
    df_rooms_analysis = pd.read_sql(query_rooms, conn)
    st.dataframe(df_rooms_analysis, use_container_width=True)

conn.close()