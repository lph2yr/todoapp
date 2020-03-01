from celery import shared_task
from celery.schedules import crontab

from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta

from models import ToDoItem


@shared_task
def schedule_emails():
    todo_schedule = ToDoItem.objects.filter(notify=True)
    #If list of todos for notifications not empty
    if todo_schedule:
        #Parses duedate of todo into crontab
        for todo in todo_schedule:
            #Sets notification time to be 1 hour before todo duedate
            notification_time = todo.duedate - relativedelta(hours=-1)
            crontab(day_of_month=notification_time.day, month_of_year=notification_time.month, year=notification_time.year, hour=notification_time.hour, minute=notification_time.minute)
    #parse datetime from schedule and format for crontab
    #schedule reminder email
    return None