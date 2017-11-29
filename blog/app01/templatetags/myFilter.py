from django.template import Library
import datetime
register = Library()

@register.filter
def yunling(t):
     current_time=datetime.datetime.now()
     create_time=datetime.datetime(year=t.year,month=t.month,day=t.day,hour=t.hour,minute=t.minute,second=t.second)

     time=current_time-create_time
     print(time.days)

     return  time.days