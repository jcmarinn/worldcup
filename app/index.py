from datetime import datetime, timedelta
from flask_appbuilder import IndexView

class JCIndexView(IndexView):
    now=datetime.now()
    last_day=datetime(2018,6,14)
    dif=last_day-now
    index_template = 'index.html'
    extra_args = {'today':'Only '+str(dif.days)+' days left - make sure you input your predictions and deposit your $20'}
