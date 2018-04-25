import logging
from flask import Flask, render_template
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


from functions import add_records, calc_stand, add_UsrScores, limit
from app import views


@app.before_request
def load_users():
    if current_user.is_authenticated():
        v_usr = current_user.get_id() # return username in get_id()
        add_records(v_usr)
        add_UsrScores(v_usr)
        # calc_stand()
    else:
        v_usr = '0' # user 0 = none

@app.route("/query", methods=['GET', 'POST'])
def query():
    usr = current_user.get_id() # return username in get_id()
    res = db.session.execute('SELECT * FROM comp_stand WHERE user_id ='+usr+' order by groups_id, pts desc')
    list = ['usr','Grp','Team','TPts','Won','Loss','Draw','G-Fa','G-Ag','GDif','Pts','Won','Loss','Draw','G-Fa','G-Ag','GDif']
    return render_template('query.html', res=res, list=list)

# @app.route("/comp_games", methods=['GET', 'POST'])
# def comp_games():
#     usr = current_user.get_id() # return username in get_id()
#     res = db.session.execute('SELECT * FROM comp_games WHERE user_id ='+usr)
#     list = ['usr','Group','Team1','Team2','Goals_T1','Goals_T2','Ur_Pred_T1','Ur_Pred_T2']
#     return render_template('comp_games.html', res=res, list=list)

class MyView(BaseView):
    route_base = "/myview"

    @expose('/method1/<string:param1>')
    def method1(self, param1):
        # do something with param1
        # and return it
        return param1

    @expose('/method2/<string:param1>')
    def method2(self, param1):
        # do something with param1
        # and render it
        param1 = 'Hello %s' % (param1)
        return param1

    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        usr = current_user.get_id() # return username in get_id()
        res = db.session.execute('SELECT * FROM comp_games WHERE user_id ='+usr)
        list = ['usr','Group','Team1','Team2','Goals_T1','Goals_T2','Ur_Pred_T1','Ur_Pred_T2']
        # self.update_redirect()
        return self.render_template('comp_games.html', res=res, list=list)
        # return self.render_template('comp_games.html',
        #                    param1 = param1)

appbuilder.add_view_no_menu(MyView())
appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')
