# coding=utf-8
from sleep_whu.celery import app
from Sleep import Sleep
from .models import SleepUser
import datetime

@app.task
def checkWhetherSleep():
    SleepUsers = SleepUser.objects.all()
    now = datetime.datetime.now()
    now = datetime.datetime.strptime(now.strftime('%H:%M:%S'), '%H:%M:%S')
    result = []
    for user in SleepUsers:
        start_time = user.startTime
        end_time = user.endTime
        start_time = datetime.datetime.strptime(str(start_time), '%H:%M:%S')
        end_time = datetime.datetime.strptime(str(end_time), '%H:%M:%S')
        # 是否处于睡觉时段
        isSleepTime = (now>=start_time) and (now<=end_time)
        isSleeping = user.status
        if isSleepTime:
            result.append(sleep(user.id,user.password))
        else:
            if isSleeping:
                result.append(resume(user.id, user.password))
            else:
                pass
    print result

def sleep(id,password):
    sleep = Sleep(id, password)
    # choice between "resume" and "stop"
    status = sleep.keep("stop")
    return {id,'SLEEPING',status}

def resume(id,password):
    sleep = Sleep(id, password)
    # choice between "resume" and "stop"
    status = sleep.keep("resume")
    return {id,'USING',status}
