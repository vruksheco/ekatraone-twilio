from twilio.rest import Client
import connect
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

day = connect.day_list
# qna_list = []
std_list = []

connect.get_delivery()

print('BACK TO APP')

# for list in connect.questions_and_answers_list:
#     que_ans = {}
#     for tuple in list:
#         que_ans[tuple[0]] = tuple[1]
#     qna_list.append(que_ans)

for list in connect.students_list:
    students = {}
    for tuple in list:
        students[tuple[0]] = tuple[1]
    std_list.append(students)

# print(qna_list)
# print(std_list)
client = Client(os.environ.get('account_sid'),os.environ.get('auth_token'))

# app = Flask(__name__)

# @app.route("/")
# def hello():
# 	return 'Hello World!'

# @app.route("/sms/<string:number>/<string:message>", methods=['GET','POST'])
def sms_reply(number, message):
    client.messages.create(
        body=message,
        messaging_service_sid=os.environ.get('messaging_service_sid'),
        to=number
    )
    return 'Done!'

# @app.route("/whatsapp/<string:number>/<string:message>", methods=['GET','POST'])
def whatsapp_reply(number, message):
    client.messages.create(
        body=message,
        from_=os.environ.get('from_whatsapp_number'),
        to='whatsapp:'+number
    )
    return 'Done!'
	
def send_course_data_to_student_with_number_and_channel(number, channel, count):
    # i = 1
    # print(count)
    msg = '*Course - {}*\n*Day{}*\n{}'.format(connect.course_name_list[count], day[count], connect.content_list[count][0][0])
    # qna_dict = qna_list[count]
    # for que in qna_dict:
    #     ans = qna_dict[que]
    #     msg += 'Q{}: {} \nAns: {}\n'.format(i, que, ans)
    #     i+=1
    print(msg)
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

# if __name__ == "__main__":
# 	app.run(debug=True)
