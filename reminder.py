import json
from datetime import datetime, timedelta
from twilio.rest import Client
import requests
import pandas as pd



def get_config_setting():
    with open('asset/config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        base_url = config['BASE_URL']
        twilio_account_sid = config['twilio_account_sid']
        twilio_auth_token = config['twilio_auth_token']
        twilio_phone_to = config['twilio_phone_to']
        twilio_phone_from = config['twilio_phone_from']
    return access_token, base_url,twilio_account_sid,twilio_auth_token,twilio_phone_to,twilio_phone_from


token, BASE_URL,twilio_account_sid, twilio_auth_token, twilio_phone_to, twilio_phone_from = get_config_setting()
auth_header = {'Authorization': 'Bearer ' + token}


def send_sms( content ,phone_to=twilio_phone_to, phone_from=twilio_phone_from):
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        to= phone_to,
        from_=phone_from,
        body= content)

    print(message.sid)
    return


def send_whatsapp( content ,phone_to=twilio_phone_to, phone_from=twilio_phone_from):
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        to= "whatsapp:+17787126686",
        from_="whatsapp:+17786440746",
        body= content)

    print(message.sid)
    return


def hours_minutes(duration):
    totsec = duration.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    sec = (totsec % 3600) % 60  # just for reference
    print("You still have %d hours , %d mins" % (h, m))


def time_left_from_due_time(due_time, debug=False):

    due_time = datetime.strptime(due_time,"%Y-%m-%dT%H:%M:%SZ")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    if debug is True:
        print("due_at :", due_time)
        print("now    :",now_str)
    now = datetime.now()
    time_delta = due_time-now
    hours_minutes(time_delta)
    return time_delta , due_time


def send_reminder_to_user(due_time, email, name, reminder_hours=48, debug=False):

    now = datetime.now()
    reminder_time = due_time- timedelta(hours=reminder_hours)
    if debug is True:
        print("____________From send_reminder_to_user start___________________")
        print("now :", now)
        print("reminder time :", reminder_time)
        print("send_email_or_no ", reminder_time < now)

    send_email_or_no = (reminder_time < now)

    if send_email_or_no:
        print("email", email)
        print("Assignment name :", name)

    if debug is True:
        print("____________From send_reminder_to_user end___________________")

    return


def get_assignment(url= BASE_URL, debug= False):

    req_url = url + '/api/v1/courses/26149/assignments'
    r = requests.get(req_url, headers=auth_header)

    r.raise_for_status()
    email = get_user_email()
    data = r.json()
    count=0
    for i in data:
        if debug is True:
            count=count+1
#        if i["due_at"]is not None and i["has_submitted_submissions"] is False:
        if i["due_at"] is not None:
            time_delta, due_time = time_left_from_due_time(i["due_at"])
            name = i["name"]
            if debug is True:
                print("Count :", count)
                print("due time :", due_time)
                print("Assignment name: ", name)
            send_reminder_to_user(due_time, email, name)
    return


def get_user_email(url= BASE_URL):
    req_url = url + '/api/v1/users/self/profile'
    r = requests.get(req_url, headers=auth_header)
    r.raise_for_status()

    data = r.json()
    if data["primary_email"] is not None:
            email = data["primary_email"]
#            print("user: ", data["primary_email"])
    return email


#get_assignment()

# get_user_email()

#send_sms("Hello from here!!")





# app = Flask("__name___")
#
# @app.route('/')
# def index():
#     send_sms("Hello from here!!")
#     return "Hello World!"
#
# app.run(debug=True,port=8000,host='0.0.0.0')
#
