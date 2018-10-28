from flask import Flask
from flask import request
import reminder as reminder
import json

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask('__name___')



@app.route('/')
def hello_world():
    reminder.send_sms("Hello from here =P")
    return "Hello World!"


@app.route('/post_json', methods=['POST'])
def post_json_handler():

    data = request.get_json(force=True)
    print("data:", data)
    return 'JSON posted'


@app.route('/send_sms', methods=['GET'])
def call_reminder_send_sms():
    reminder.send_sms("Reminder: your assignment1 is due in 30 mins, please submit it ASAP")
    #reminder.send_whatsapp("Reminder: your assignment1 is due in 30 mins, please submit it ASAP")
    return 'send_sms_to phone'

if __name__ =='__main__':
    app.run(debug=DEBUG,host=HOST,port=PORT)


