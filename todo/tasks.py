from celery.schedules import crontab
from .celery import app

from django.utils import timezone
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from .models import ToDoItem
from django.contrib.auth.models import User

@app.task
def check_for_notifications():
    notify_interval_begin = datetime.now() + relativedelta(hours=+1)
    notify_interval_end = datetime.now() + relativedelta(hours=+1, minutes=+5)
    todo_list = ToDoItem.objects.filter(notify=true).filter(duedate__gte=notify_interval_begin).filter(duedate__lte=notify_interval_end)
    for todo in todo_list:
        notify_time = todo.duedate + relativedelta(hours=-1)
        queue_email.apply_async((todo_notify.id), eta=notify_time)

@app.task
def queue_email(todo_item_id):
    todo_notify = ToDoItem.objects.get(id=todo_item_id)
    user_to_notify = User.objects.get(id=todo_notify.user)
    due_date_local = todo_notify.duedate.astimezone(pytz.timezone("America/New_York"))
    send_mail(
        todo_notify.title + ' due soon!',
        'Your todo item is due soon!' + 
        '\n Title: ' + todo_notify.title + 
        '\n Description: \t' + todo_notify.description +
        '\n Due: \t' + due_date_local.strftime("%m/%d/%Y, %I:%M:%S %p"),
        'personaldashboard.bogosorters@gmail.com',
        [user_to_notify.email],
   )