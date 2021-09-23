from datetime import datetime, timedelta
from time import sleep

from . import lcd
from flask import Blueprint, flash, redirect, request, url_for

from .models import Break, Pattern, Time, Setting

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Unable to load GPIO")


scheduled = Blueprint("scheduled", __name__)
inclementBellGPIO = 18
manualBellGPIO = 15


@scheduled.route('/')
def scheduled_invalid():
    return ''


@scheduled.route('/manual/ringbell', methods=['POST'])
def manualBell():
    ringPattern = Pattern.query.get(request.form.get('pattern'))
    bellRelay = False
    bellGPIO = manualBellGPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellGPIO, GPIO.OUT, initial=GPIO.LOW)
    if ringPattern:
        rPattern = ringPattern.pattern.replace(" ", "").split(",")
        i = 0
        for p in rPattern:
            timeDelay = (float(int(p)) / 10)
            if i % 2 == 0:
                bellRelay = True
            else:
                bellRelay = False

            GPIO.output(bellGPIO, bellRelay)
            sleep(timeDelay)
            i += 1
        GPIO.output(bellGPIO, False)
    GPIO.cleanup(bellGPIO)
    flash("Bell has been rung!!!!", 'success')
    return redirect(url_for('main.home'))


@scheduled.route('/manual/inclement', methods=['POST'])
def inclementBell():
    bellGPIO = inclementBellGPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellGPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(bellGPIO, True)
    sleep(1)
    GPIO.output(bellGPIO, False)
    GPIO.cleanup(bellGPIO)
    flash("Inclement Bell has been rung!!!!", 'success')
    return redirect(url_for('main.home'))


@scheduled.route('/scheduled/ringbell', methods=['POST'])
def ringBell():
    datetimeNow = datetime.now()
    dateNow = str(datetimeNow.strftime("%Y-%m-%d"))
    timeNow = datetimeNow.strftime("%H:%M")

    dayNumber = datetimeNow.weekday()
    isSchoolDay = False
    isBreak = False
    isTime = False
    bellRelay = False
    bellGPIO = manualBellGPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellGPIO, GPIO.OUT, initial=GPIO.LOW)

    Override = Setting.query.filter_by(setting='override_bell').first()

    if Override.setting_value == 1:
        GPIO.cleanup(bellGPIO)
        return "OK", 200

    if dayNumber not in [5, 6]:
        isSchoolDay = True

    if isSchoolDay:
        breaks = Break.query.filter(
            Break.startDate <= dateNow, Break.endDate >= dateNow).count()
        if breaks:
            isBreak = True

    if not isBreak:
        ringTimes = Time.query.all()
        for t in ringTimes:
            if t.time.strftime("%H:%M") == timeNow:
                if t.days[dayNumber] == '1':
                    patternId = t.pattern
                    isTime = True
                    break

    if isTime:
        qPattern = Pattern.query.get(patternId)
        if qPattern:
            rPattern = qPattern.pattern.replace(" ", "").split(",")
            i = 0
            for p in rPattern:
                timeDelay = (float(int(p)) / 10)
                if i % 2 == 0:
                    bellRelay = True
                else:
                    bellRelay = False

                GPIO.output(bellGPIO, bellRelay)
                sleep(timeDelay)
                i += 1
            GPIO.output(bellGPIO, False)

    GPIO.cleanup(bellGPIO)

    return "OK", 200


@scheduled.route('/scheduled/nextbell', methods=['POST'])
def nextBell():
    datetimeNow = datetime.now()
    timeNow = datetimeNow.strftime("%H:%M")
    lcdDate = str(datetimeNow.strftime("%d/%m/%y"))
    lcdTime = datetimeNow.strftime("%H:%M")

    isSchoolDay = False
    isBreak = False
    isTime = False

    Override = Setting.query.filter_by(setting='override_bell').first()

    while True:
        dateNow = str(datetimeNow.strftime("%Y-%m-%d"))
        printDate = str(datetimeNow.strftime("%d/%m/%y"))
        dayNumber = datetimeNow.weekday()

        if dayNumber not in [5, 6]:
            isSchoolDay = True

        if isSchoolDay:
            breaks = Break.query.filter(
                Break.startDate <= dateNow, Break.endDate >= dateNow).count()
            if breaks:
                isBreak = True
        if not isBreak:
            ringTimes = Time.query.all()
            for t in ringTimes:
                dbTime = t.time.strftime("%H:%M")
                if dbTime >= timeNow:
                    if t.days[dayNumber] == '1':
                        nextDate = printDate
                        nextTime = dbTime
                        isTime = True
                        break
        if isTime:
            if Override.setting_value != 1:
                lcd.backlight_enabled = True
                lcdText = "\x01 %s %s" % (lcdDate, lcdTime)
                lcdText2 = "\x00 %s %s" % (nextDate, nextTime)
            else:
                lcd.clear()
                lcd.backlight_enabled = True
                lcdText = "\x01 %s %s" % (lcdDate, lcdTime)
                lcdText2 = "\x00 Overridden"
            lcd.cursor_pos = (0, 0)
            lcd.write_string(lcdText)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(lcdText2)
            lcd.close(clear=False)
            break
        else:
            lcd.backlight_enabled = False
            lcd.close(clear=True)
            break

    return "OK", 200
