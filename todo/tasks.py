from celery import shared_task
from celery.schedules import crontab

from django.utils import timezone
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from .models import ToDoItem
from django.contrib.auth.models import User

@shared_task
def check_for_notifications(user_id):
    notify_interval_begin = datetime.now() + relativedelta(hours=+1)
    notify_interval_end = datetime.now() + relativedelta(hours=+1, minutes=+5)
    todo_list = ToDoItem.objects.filter(user=user_id).filter(notify=true).filter(duedate__gte=notify_interval_begin).filter(duedate__lte=notify_interval_end)
    for todo in todo_list:
        notify_time = todo.duedate + relativedelta(hours=-1)
        queue_email.apply_async((todo_notify.id, user_id), eta=notify_time)

@shared_task
def queue_email(todo_item_id, user_id):
    todo_notify = ToDoItem.objects.get(id=todo_item_id)
    user = User.objects.get(id=user_id)
    due_date_local = todo_notify.duedate.astimezone(pytz.timezone("America/New_York"))
    send_mail(
        todo_notify.title + ' due soon!',
        'Your todo item is due soon!' + 
        '\n Title: ' + todo_notify.title + 
        '\n Description: \t' + todo_notify.description +
        '\n Due: \t' + due_date_local.strftime("%m/%d/%Y, %I:%M:%S %p"),
        'personaldashboard.bogosorters@gmail.com',
        [user.email],
   )