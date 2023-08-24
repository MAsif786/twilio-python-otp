
import sqlite3
from consts import DATABASE_NAME, OTP_EXPIRATION
import datetime


def verify_otp_code(otp_code, phone_number):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT otp_code, expiration_time FROM otps WHERE phone_number = ?', (phone_number,))
    stored_data = cursor.fetchone()
    if stored_data:
        stored_otp = stored_data[0]
        expiration_time_str = stored_data[1]

        # Convert the expiration time string from the database to a datetime object
        expiration_time = datetime.datetime.strptime(expiration_time_str, '%Y-%m-%d %H:%M:%S.%f')

        if datetime.datetime.now() <= expiration_time and otp_code == stored_otp:
            message = 'OTP validated successfully'
            status = True
        elif datetime.datetime.now() > expiration_time:
            message = 'OTP has expired'
            status = False
        else:
            message = 'Invalid OTP'
            status = False
    else:
        message = 'Invalid OTP'
        status = False

    conn.close()
    return status, message


def delete_phone_records(phone_number):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM otps WHERE phone_number = ?', (phone_number,))
    conn.commit()  # Commit the deletion



def save_otp_to_database(phone_number, otp_code, expiration_seconds=OTP_EXPIRATION):
    delete_phone_records(phone_number)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Set OTP expiration time OTP_EXPIRATION in minutes
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=60*expiration_seconds)
    
    cursor.execute('INSERT INTO otps (phone_number, otp_code, expiration_time) VALUES (?, ?, ?)', (phone_number, otp_code, expiration_time))
    conn.commit()
    conn.close()
