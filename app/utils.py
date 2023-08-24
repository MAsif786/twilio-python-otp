import random
from db.utils import save_otp_to_database
from twilio.rest import Client
from consts import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER


def generate_otp_code():
    return str(random.randint(100000, 999999))

def split_code(code):
    return " ".join(code)


def send_otp_code(phone_number, otp_code, channel):
    if channel == 'voice':
        return send_otp_via_voice_call(phone_number, otp_code)
    if channel == 'sms':
        return send_otp_via_sms(phone_number, otp_code)


def send_otp_via_voice_call(number, code):
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    outline_code = split_code(code)
    call = twilio_client.calls.create(
        twiml=f"<Response><Say voice='alice'>Your OTP is {outline_code}</Say><Pause length='1'/><Say>Your one time password is {outline_code}</Say><Pause length='1'/><Say>Goodbye</Say></Response>",
        to=f"{number}",
        from_=TWILIO_NUMBER
    )


def send_otp_via_sms(number, code):

    print("outline_code: ", code)
    print("number: ", number)
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    messages = twilio_client.messages.create(to=f"{number}", from_=TWILIO_NUMBER, body=f"Your OTP is {code}")


def make_otp_request(phone_number):
    otp_code = generate_otp_code()
    save_otp_to_database(phone_number, otp_code)
    return otp_code


def verify_caller_id():
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    validation_request = client.validation_requests \
        .create(
            friendly_name='Third Party VOIP Number',
            status_callback='https://somefunction.twil.io/caller-id-validation-callback',
            phone_number='+923036982800'
        )
    
    print(validation_request)
