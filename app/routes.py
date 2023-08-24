from flask import session, request, flash, redirect, url_for, render_template, jsonify
from app import app
from db.utils import save_otp_to_database, verify_otp_code
from .utils import generate_otp_code, make_otp_request, send_otp_code

# API Endpoints
@app.route('/api/otp/create', methods=['POST'])
def api_create_otp():
    # Parse request data and generate OTP
    phone_number = request.json.get('phone_number')
    expiration = request.json.get('expiration')
    channel = request.json.get('channel')
    otp_code = generate_otp_code()
    print("=========================")
    print(otp_code)
    print("=========================")
    save_otp_to_database(phone_number, otp_code, expiration)
    send_otp_code(phone_number, otp_code, channel)
    return jsonify({"success":True, "message": "OTP created and sent successfully"})

@app.route('/api/otp/validate', methods=['POST'])
def api_validate_otp():
    otp_code = request.json.get('otp_code')
    phone_number = request.json.get('phone_number')
    status, message = verify_otp_code(otp_code, phone_number)
    return jsonify({"success": status, "message": message})

# Demo

@app.route('/demo')
def demo():
    return render_template('index.html')


# Web App
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        return render_template('generate.html')
    
    phone_number = request.form['phone_number']
    channel = request.form['channel']
    error = None
    if not phone_number:
        error = 'Phone Number is required'
    if channel != 'voice' and channel != 'sms':
        error = 'Invalid channel'
    if error is None:
        formatted_phone_number = phone_number[1:]
        session['phone_number'] = formatted_phone_number
        otp_code = make_otp_request(formatted_phone_number)
        if otp_code:
            # send_otp_code(phone_number, otp_code, channel)
            flash('Otp has been generated successfully', 'success')
            return redirect(url_for('validate',))
        error = 'Something went wrong, could not generate OTP'
    flash(error, 'danger')
    return redirect(url_for('generate'))

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'GET':
        return render_template('validate.html')
    otp_code = request.form['otp_code']
    phone_number = request.form['phone_number']
    error = None
    if not otp_code:
        error = 'Otp code is required'
    if not phone_number:
       error = 'Please request for a new OTP'

    if error is None:
        session.pop('phone_number', None)
        status, message = verify_otp_code(otp_code, phone_number)
        if status == True:
           flash(message, 'success')
           return redirect(url_for('validate'))
        if status == False:
           flash(message, 'danger')
           return redirect(url_for('validate'))
        error = 'Something went wrong, could not validate OTP'
    flash(error, 'info')
    return redirect(url_for('generate'))
