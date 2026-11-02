import sqlite3

def create_database():
    # hotel.db adında bir SQLite veritabanı dosyası oluşturur (yoksa otomatik yaratır)
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # 1. Hotels (Oteller) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hotels (
            hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT
        )
    ''')

    # 2. Rooms (Odalar) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER,
            room_number TEXT NOT NULL,
            room_type TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'Available',
            FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id)
        )
    ''')

    # 3. Customers (Müşteriler) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    ''')

    # 4. Reservations (Rezervasyonlar) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            room_id INTEGER,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            total_price REAL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        )
    ''')

    # 5. Payments (Ödemeler) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            payment_method TEXT,
            FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id)
        )
    ''')

    # Başlangıç için örnek veriler (INSERT komutları)
    cursor.execute("INSERT OR IGNORE INTO Hotels (hotel_id, name, city, address) VALUES (1, 'Grand Palace Hotel', 'Gaziantep', 'Şehitkamil');")
    cursor.execute("INSERT OR IGNORE INTO Rooms (room_id, hotel_id, room_number, room_type, price, status) VALUES (1, 1, '101', 'Single', 1200.0, 'Available');")
    cursor.execute("INSERT OR IGNORE INTO Rooms (room_id, hotel_id, room_number, room_type, price, status) VALUES (2, 1, '102', 'Double', 2000.0, 'Available');")
    cursor.execute("INSERT OR IGNORE INTO Customers (customer_id, first_name, last_name, phone, email) VALUES (1, 'Ahmet', 'Yılmaz', '5551234567', 'ahmet@ornek.com');")

    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()
    print("Veritabanı, tablolar ve örnek veriler başarıyla oluşturuldu dostum!")

if __name__ == '__main__':
    create_database()