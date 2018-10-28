import json
from datetime import datetime, timedelta
from twilio.rest import Client
import requests
import pandas as pd


def get_config_setting():
    with open('asset/config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        BASE_URL = config['BASE_URL']
        twilio_account_sid = config['twilio_account_sid']
        twilio_auth_token = config['twilio_auth_token']
        twilio_phone_to = config['twilio_phone_to']
        twilio_phone_from = config['twilio_phone_from']
    return access_token, BASE_URL,twilio_account_sid,twilio_auth_token,twilio_phone_to,twilio_phone_from


# BASE_URL = 'https://canvas.ubc.ca'




token, BASE_URL,twilio_account_sid,twilio_auth_token,twilio_phone_to,twilio_phone_from = get_config_setting()
auth_header = {'Authorization': 'Bearer ' + token} # setup the authorization header to be used later


def send_sms( content ,phone_to=twilio_phone_to, phone_from=twilio_phone_from):
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        to= phone_to,
        from_=phone_from,
        body= content)

    print(message.sid)
    return


def hours_minutes(duration):
    totsec = duration.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    sec = (totsec % 3600) % 60  # just for reference
    print("You still have %d hours , %d mins" % (h, m))


def time_left_from_due_time(due_time):

    due_time = datetime.strptime(due_time,"%Y-%m-%dT%H:%M:%SZ")
    print("due_at :",due_time)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    print("now    :",now_str)
    now = datetime.now()
    time_delta = due_time-now

    hours_minutes(time_delta)
    return time_delta , due_time

def send_reminder_to_user(due_time,email, name,reminder_hours=48):

    print("____________From send_reminder_to_user start___________________")

    now = datetime.now()
    reminder_time = due_time- timedelta(hours=reminder_hours)
    print("now :" , now)
    print("reminder time :", reminder_time)
    print("send_email_or_no ",reminder_time < now)

    send_email_or_no = (reminder_time < now)

    if send_email_or_no:
        print("email",email)
        print("Assigment name :",name)
    print("____________From send_reminder_to_user end___________________")

    return

def get_assignment(url= BASE_URL):

    req_url = url + '/api/v1/courses/26149/assignments'
    r = requests.get(req_url, headers=auth_header)

    r.raise_for_status()
    email = get_user_email()
    data = r.json()
    count=0
    for i in data:
        count=count+1

        #if i["due_at"]is not None and i["has_submitted_submissions"] is False:
        if i["due_at"] is not None :
            print("Count :" ,count)
            time_delta, due_time  = time_left_from_due_time(i["due_at"])
            print("due time :", due_time)

            name = i["name"]
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
            #print("user: ", data["primary_email"])
    return email

# get_assignment()
#
# get_user_email()

send_sms("Hello from here!!")
