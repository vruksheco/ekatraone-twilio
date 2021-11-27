from twilio.rest import Client
import connect
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

day = connect.day_list
std_list = []

connect.get_delivery()

for list in connect.students_list:
    students = {}
    for tuple in list:
        students[tuple[0]] = tuple[1]
    std_list.append(students)

client = Client(os.environ.get('account_sid'),os.environ.get('auth_token'))

def sms_reply(number, message):
    client.messages.create(
        body=message,
        messaging_service_sid=os.environ.get('messaging_service_sid'),
        to=number
    )
    return 'Done!'

def whatsapp_reply(number, message):
    client.messages.create(
        body=message,
        from_=os.environ.get('from_whatsapp_number'),
        to='whatsapp:'+number
    )
    return 'Done!'
	
def send_course_data_to_student_with_number_and_channel(number, channel, count):
    msg = '*Course - {}*\n*Day{}*\n{}'.format(connect.course_name_list[count], day[count], connect.content_list[count][0][0])
    if channel=='Sms':
        sms_reply(number, msg)
    else:
        whatsapp_reply(number, msg)

c=0
for std_dict in std_list:
    for std_num in std_dict:
        std_channel = std_dict[std_num]
        send_course_data_to_student_with_number_and_channel(number=std_num, channel=std_channel, count=c)
    c+=1
