import psycopg2
import pytz
from datetime import datetime
from sqlalchemy.sql.expression import null
from config import config

day_list = []
content_list = []
course_name_list = []
students_list = []

def get_delivery():
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        select_all_from_deliveries = "select * from delivery where status = 'SCHEDULED'"
        select_name_from_courses = "select name from course where id = %s"
        select_content_from_days = "select text from days where course_id = %s and day = %s"
        select_number_channel_from_students = "select number, channel from students where group_id = %s and is_subscribed = 'true' and is_deleted = 'false' "
        cursor.execute(select_all_from_deliveries)
        deliveries = cursor.fetchall()
        for row in deliveries:
            day = (datetime.now(pytz.timezone('Asia/Calcutta')).date() - row[7].date()).days + 1
            global day_list
            day_list.append(day)
            group_id = row[1]
            course_id = row[2]
            cursor.execute(select_name_from_courses, (course_id,))
            course_name = cursor.fetchall()
            global course_name_list
            course_name_list.append(course_name[0][0])
            cursor.execute(select_content_from_days, (course_id, day,))
            content = cursor.fetchall()
            if not content:
                continue
            global content_list
            content_list.append(content)
            
            cursor.execute(select_number_channel_from_students, (group_id,))
            global students
            students = cursor.fetchall()
            students_list.append(students)

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection   
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")
