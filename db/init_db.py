import sqlite3
from consts import DATABASE_NAME

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS otps
                      (phone_number TEXT, otp_code TEXT, expiration_time DATETIME)''')
    conn.commit()
    conn.close()
