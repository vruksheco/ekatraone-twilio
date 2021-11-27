import psycopg2
import pytz
from datetime import datetime
from sqlalchemy.sql.expression import null
from config import config

day_list = []
content_list = []
course_name_list = []
students_list = []
# questions_and_answers_list = []

def get_delivery():
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        # print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        select_all_from_deliveries = "select * from delivery where status = 'SCHEDULED'"
        select_name_from_courses = "select name from course where id = %s"
        select_content_from_days = "select text from days where course_id = %s and day = %s"
        # select_id_from_days = "select id from days where day = %s and course_id = %s"
        # select_que_ans_from_questions = "select text, correct_answer from questions where day_id = %s and course_id = %s"
        select_number_channel_from_students = "select number, channel from students where group_id = %s and is_subscribed = 'true' and is_deleted = 'false' "
        cursor.execute(select_all_from_deliveries)
        deliveries = cursor.fetchall()
        for row in deliveries:
            day = (datetime.now(pytz.timezone('Asia/Calcutta')).date() - row[7].date()).days + 1
            # print(str(datetime.now(pytz.timezone('Asia/Calcutta')).date()))
            # print(str(row[7].date()))
            global day_list
            day_list.append(day)
            print('id:' + str(row[0]))
            group_id = row[1]
            course_id = row[2]
            print(course_id)
            cursor.execute(select_name_from_courses, (course_id,))
            course_name = cursor.fetchall()
            global course_name_list
            course_name_list.append(course_name[0][0])
            cursor.execute(select_content_from_days, (course_id, day,))
            content = cursor.fetchall()
            # print(content[0][0])
            if not content:
                continue
            global content_list
            content_list.append(content)
            # print('day:' + str(day))  
            # cursor.execute(select_id_from_days, (day, course_id,))
            # day_id = cursor.fetchall()
            # if not day_id:
            #     continue
            # print('day_id:' + str(day_id))
            # cursor.execute(select_que_ans_from_questions, (day_id[0], course_id,))
            # qna = cursor.fetchall()
            # print('qna:' + str(qna))
            # global questions_and_answers_list
            # questions_and_answers_list.append(qna)
            
            cursor.execute(select_number_channel_from_students, (group_id,))
            global students
            students = cursor.fetchall()
            students_list.append(students)
            # print('students:' + str(students))

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection   
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")

# get_delivery()
# print(content_list[0][0][0])
# if __name__ == '__main__':
    # get_delivery()
#     print(questions_and_answers)
