from time import sleep
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from RPLCD.i2c import CharLCD
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Unable to load GPIO")

db = SQLAlchemy()


def init_lcd():
    lcd = CharLCD('PCF8574', 0x27)

    bell = (0b00000,
            0b00100,
            0b01110,
            0b01110,
            0b01110,
            0b11111,
            0b00100,
            0b00000)

    clock = (0b00000,
             0b01110,
             0b10101,
             0b10111,
             0b10001,
             0b01110,
             0b00000,
             0b00000)

    lcd.create_char(0, bell)
    lcd.create_char(1, clock)
    lcd.backlight_enabled = False
    lcd.clear()

    return lcd


lcd = init_lcd()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bananabread'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schoolBell.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,
        'pool_reset_on_return': 'commit',
        'pool_timeout': 5,
    }
    inclementBellGPIO = 18
    manualBellGPIO = 15
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(inclementBellGPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(manualBellGPIO, GPIO.OUT, initial=GPIO.LOW)

    db.init_app(app)
    lcd.backlight_enabled = True
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Loading.........')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('School Bell \x00 \x01')
    sleep(20)
    lcd.backlight_enabled = False

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .breaks import breaks as breaks_blueprint
    app.register_blueprint(breaks_blueprint, url_prefix='/')

    from .times import times as times_blueprint
    app.register_blueprint(times_blueprint, url_prefix='/')

    from .patterns import patterns as patterns_blueprint
    app.register_blueprint(patterns_blueprint, url_prefix='/')

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/')

    from .scheduled import scheduled as scheduled_blueprint
    app.register_blueprint(scheduled_blueprint, url_prefix='/')

    return app
