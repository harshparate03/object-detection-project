from twilio.rest import Client
# print("Twilio import successful")
from django.conf import settings
from django.shortcuts import render,redirect
import re
from django.contrib.auth.models import User

# def send_sms(phone_number, message):
#     # Create a Twilio client
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#     # Send the message
#     message = client.messages.create(
#         body=message,  # The SMS content
#         from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
#         to=phone_number  # The recipient's phone number
#     )
#     return message.sid

from twilio.rest import Client
import random

def send_sms(phone_number, message):
    # Twilio account SID and authentication token
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    
    # Your Twilio phone number (this must be a verified number or purchased Twilio number)
    from_phone = 'your_twilio_verified_or_purchased_phone_number'
    
    # If the phone number is not in international format, prepend '+91'
    if not phone_number.startswith('+91'):
        phone_number = '+91' + phone_number.lstrip('0')  # Ensure correct format by adding +91 and removing leading 0
    
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=message,
        from_=from_phone,
        to=phone_number
    )
    
    return message.sid

# # Example OTP generation with phone number format adjustment
# def forgot(request):
#     error_message = None  # Variable to store error messages
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
        
#         # Validate phone number using a regular expression (adjust regex for your requirements)
#         phone_pattern = r'^\+?[0-9]{10,15}$'
#         if not re.match(phone_pattern, phone_number):
#             error_message = "Invalid phone number format. Please enter a valid number."
#             return render(request, 'forgot.html', {'error': error_message})
        
#         try:
#             # Ensure the phone number field is correctly named in your User model
#             user = User.objects.get(phone=phone_number)
            
#             # Store user ID in the session for later use
#             request.session['user_id'] = user.id
            
#             # Generate a random 6-digit OTP
#             otp_code = f"{random.randint(100000, 999999)}"
            
#             # Send the OTP via SMS with country code
#             send_sms(phone_number, f"Your OTP is: {otp_code}")
            
#             # Optionally store the OTP in the session (you could use a database instead)
#             request.session['otp_code'] = otp_code
            
#             return redirect('verify_otp')
#         except User.DoesNotExist:
#             error_message = "User with this phone number does not exist."
    
#     # Render the form with error messages if validation fails
#     return render(request, 'forgot.html', {'error': error_message})

from twilio.rest import Client
import random

def send_sms(phone_number, message):
    # Twilio account SID and authentication token
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    
    # Your Twilio phone number (this must be a verified number or purchased Twilio number)
    from_phone = settings.TWILIO_PHONE_NUMBER
    
    # If the phone number is not in international format, prepend '+91'
    if not phone_number.startswith('+91'):
        phone_number = '+91' + phone_number.lstrip('0')  # Ensure correct format by adding +91 and removing leading 0
    
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=message,
        from_=from_phone,
        to=phone_number
    )
    
    return message.sid

# Example OTP generation with phone number format adjustment
def forgot(request):
    error_message = None  # Variable to store error messages
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Validate phone number using a regular expression (adjust regex for your requirements)
        phone_pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_pattern, phone_number):
            error_message = "Invalid phone number format. Please enter a valid number."
            return render(request, 'forgot.html', {'error': error_message})
        
        try:
            # Ensure the phone number field is correctly named in your User model
            user = User.objects.get(phone=phone_number)
            
            # Store user ID in the session for later use
            request.session['user_id'] = user.id
            
            # Generate a random 6-digit OTP
            otp_code = f"{random.randint(100000, 999999)}"
            
            # Send the OTP via SMS with country code
            send_sms(phone_number, f"Your OTP is: {otp_code}")
            
            # Optionally store the OTP in the session (you could use a database instead)
            request.session['otp_code'] = otp_code
            
            return redirect('verify_otp')
        except User.DoesNotExist:
            error_message = "User with this phone number does not exist."
    
    # Render the form with error messages if validation fails
    return render(request, 'forgot.html', {'error': error_message})


# import requests
# from django.conf import settings

# def send_sms(phone_number, message):
#     # Twilio API URL
#     url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(settings.TWILIO_ACCOUNT_SID)
    
#     # Basic authentication (Twilio SID and Auth Token)
#     auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#     # Data payload for sending SMS
#     data = {
#         'To': phone_number,  # Recipient's phone number
#         'From': settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
#         'Body': message  # SMS content
#     }

#     # Send SMS via POST request
#     response = requests.post(url, data=data, auth=auth)

#     if response.status_code == 201:
#         return response.json()['sid']
#     else:
#         return f"Error: {response.status_code} - {response.text}"
