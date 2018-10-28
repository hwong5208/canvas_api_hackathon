from flask import Flask
from flask import request
import reminder as reminder

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
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'


@app.route('/send_sms', methods=['GET'])
def call_reminder_send_sms():
    reminder.send_sms(" Class reminder")
    return 'send_sms_to phone'

if __name__ =='__main__':
    app.run(debug=DEBUG,host=HOST,port=PORT)


