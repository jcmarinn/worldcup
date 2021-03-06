import logging
from datetime import datetime
from flask import Flask, render_template, g
from flask_appbuilder import SQLA, AppBuilder, BaseView, expose, has_access
from app.index import JCIndexView
from flask_login import current_user


# Logging configuration

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, indexview=JCIndexView)

from functions import add_records, calc_stand, add_UsrScores, limit, has_changed
from app import views

@app.context_processor
def todays():
    now=datetime.now()
    last_day=datetime(2018,6,13)
    dif=now-last_day
    return dict(dif=str(dif.days))

app.jinja_env.globals.update(todays=todays)

@app.before_request
def load_users():
    if current_user.is_authenticated():
        usr = current_user.get_id() # return username in get_id()
        add_records(usr)
        add_UsrScores(usr)
        has_changed(usr)
        # calc_stand()
    else:
        v_usr = '0' # user 0 = none
