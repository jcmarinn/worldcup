from flask import render_template, flash, g, redirect, session
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction
from flask_appbuilder.actions import action
from flask_appbuilder.fieldwidgets import TextField
from flask_appbuilder import ModelView, CompactCRUDMixin, MasterDetailView, MultipleView, AppBuilder, expose, BaseView, has_access
from flask_babel import lazy_gettext as _ , gettext
from app import appbuilder, db
from models import *
from flask_appbuilder.widgets import FormInlineWidget
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from functions import calc_stand, calc_usr_stand, calc_bet, limit
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_login import current_user
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from widgets import MyEditWidget

class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


class GroupsView(ModelView):
    datamodel = SQLAInterface(Groups)
    list_columns = ['name']

class TeamsView(ModelView):
    datamodel = SQLAInterface(Teams)
    list_columns = ['flg_img', 'name', 'groups.name']
    label_columns = {'flg_img':'Flag'}
    base_permissions = ['can_list']
    base_order = ['name', 'asc']
    order_columns = ['name','groups.name']
    page_size = 32

class GroupsTeams(MasterDetailView):
    datamodel = SQLAInterface(Groups)
    related_views = [TeamsView]
    base_permissions = ['can_list']

class GamesView(ModelView):
    datamodel = SQLAInterface(Games)
    list_columns = ['date_nice','flg1_img','team1','flg2_img','team2','team1.groups.name','stadium','goal1','goal2','round']
    label_columns = {'date_nice':'Date','team1.groups.name':'Group', 'team1':'Team 1', 'team2':'Team 2', 'goal1':'Goals T1', 'goal2':'Goals T2'}
    base_filters = [['round', FilterStartsWith, "Round of 32" ]]
    base_order = ['date','asc']
    base_permissions = ['can_list','can_edit']
    edit_columns = ['goal1','goal2']
    page_size = 48

    @action("clear","Clear Results?","Do you really want to clear these games?","fa-exclamation-triangle", single=False)
    def clear(self, items):
        for i in items:
            i.goal1 = None
            i.goal2 = None
            self.datamodel.edit(i)
        self.update_redirect()
        return redirect(self.get_redirect())

class GamesView16(ModelView):
    datamodel = SQLAInterface(Games)
    list_columns = ['date_nice','flg1_img','team1','flg2_img','team2','team1.groups.name','stadium','goal1','goal2','round']
    label_columns = {'date_nice':'Date','team1.groups.name':'Group', 'team1':'Team 1', 'team2':'Team 2', 'goal1':'Goals T1', 'goal2':'Goals T2'}
    base_filters = [['round', FilterStartsWith, "Round of 16" ]]
    base_order = ['date','asc']
    base_permissions = ['can_list','can_edit']
    edit_columns = ['goal1','goal2']
    page_size = 8

class PredictView(ModelView):
    datamodel = SQLAInterface(Predict)
    list_columns = ['date_nice','flg1_img','team1','flg2_img','team2','team1.groups.name','stadium','goal1','goal2','round']
    label_columns = {'date_nice':'Date','team1.groups.name':'Group', 'team1':'Team 1', 'team2':'Team 2', 'goal1':'Goals T1', 'goal2':'Goals T2', 'flg1_img':' ','flg2_img':' '}
    base_filters = [['round', FilterStartsWith, "Round of 32" ],['user_id', FilterEqualFunction, get_user]]
    base_order = ['date','asc']
    order_columns = ['date','stadium']
    base_permissions = limit()
    edit_columns = ['goal1','goal2']
    edit_widget=FormInlineWidget
    page_size = 48

    @action("clear","Clear Scores","Do you really want to clear your prediction for these records?","fa-exclamation-triangle", single=False)
    def clear(self, items):
        for item in items:
            item.goal1 = None
            item.goal2=None
            self.datamodel.edit(item)
        self.update_redirect()
        return redirect(self.get_redirect())

class PredictView16(ModelView):
    datamodel = SQLAInterface(Predict)
    list_columns = ['date_nice','flg1_img','team1','flg2_img','team2','team1.groups.name','stadium','goal1','goal2','round']
    label_columns = {'date_nice':'Date','team1.groups.name':'Group', 'team1':'Team 1', 'team2':'Team 2', 'goal1':'Goals T1', 'goal2':'Goals T2', 'flg1_img':' ','flg2_img':' '}
    base_filters = [['round', FilterStartsWith, "Round of 16" ],['user_id', FilterEqualFunction, get_user]]
    base_order = ['date','asc']
    order_columns = ['date','stadium']
    base_permissions = limit()
    edit_columns = ['goal1','goal2']
    edit_widget=FormInlineWidget
    page_size = 8

class Stand32View(ModelView):
    datamodel = SQLAInterface(Stand32)
    list_columns = ['teams.groups.name','flg_img','teams.name','pos','pts','won','loss','draw','gf','ga','gd']
    label_columns = {'teams.groups.name':'Group', 'pos':'Grp Pos'}
    base_permissions = ['can_list']
    base_order = ('teams.groups_id','asc')
    order_columns = ['pos', 'pts']
    page_size = 32
    # list_template = 'list_stand.html'

    @action("update","Update Results","Go ahead?","fa-question", single=False)
    def update(self, items):
        calc_stand()
        self.update_redirect()
        return redirect(self.get_redirect())

class UsrStand32View(ModelView):
    datamodel = SQLAInterface(UsrStand32)
    list_columns = ['teams.groups.name','flg_img','teams.name','pos','pts','won','loss','draw','gf','ga','gd']
    label_columns = {'teams.groups.name':'Group', 'pos':'Grp Pos'}
    base_permissions = ['can_list']
    base_order = ('teams.groups_id','asc')
    order_columns = ['pts']
    base_filters = [['user_id', FilterEqualFunction, get_user]]
    page_size = 32
    # list_template = 'list_stand.html'

    @action("update","Update Results","Go ahead?","fa-question", single=False)
    def update(self, items):
        calc_usr_stand(get_user())
        self.update_redirect()
        return redirect(self.get_redirect())

class UsrScoresView(ModelView):
    datamodel = SQLAInterface(UsrScores)
    list_columns = ['ab_user.first_name', 'ab_user.last_name', 'round', 'pts_total', 'pts_game','pts_score','pts_stand','has_paid']
    label_columns = {'pts_total':'Total Points' ,'pts_game':'Correct Game Winner', 'pts_score':'Correct Game Score','pts_stand':'Correct Group Standing Pts','has_paid':'has paid?'}
    base_permissions = ['can_list']
    order_columns = ['pts_total']
    list_template = 'list_stand.html'
    page_size = 20
    extra_args = {'footer1':_('Points awarded as follow:'),
                  'footer2':_('1) 1 x Point for every correct Game Winner/Draw Result (1 pts per Game)'),
                  'footer3':_('2) 2 x Additional points for every exact Game Score (3 total pts per Game)'),
                  'footer4':_('3) 3 x Points for every correct Group standing (3 pts per Group Standing)'),
                  'footer5':'',
                  }

    @action("update","Calculate All Scores","This will update all people results","fa-check", single=False)
    def update(self, items):
        calc_bet()
        self.update_redirect()
        return redirect(self.get_redirect())

class AllGameScores(BaseView):
    route_base = "/GameScores"

    @expose('/list/<string:usr>')
    @has_access
    def list(self, usr):
        if usr == 'User':
            usr = current_user.first_name+' '+current_user.last_name
        usrs = db.session.execute('SELECT distinct usr_name from comp_stand')
        res = db.session.execute('SELECT * FROM comp_stand WHERE usr_name ='+r"'"+usr+r"'"+' order by grp, pos')
        list = ['usr','Grp','Team','Pos', 'Pts','Won','Loss','Draw','G-Fa','G-Ag','GDif','Pos','Pts','Won','Loss','Draw','G-Fa','G-Ag','GDif']
        return self.render_template('comp_stand.html', usrs=usrs, res=res, list=list)

    @expose('/listAll/<string:usr>')
    @has_access
    def listAll(self, usr):
        if usr == 'User':
            usr = current_user.first_name+' '+current_user.last_name
        usrs = db.session.execute('SELECT distinct name from comp_games')
        res = db.session.execute('SELECT * FROM comp_games where name ='+r"'"+usr+r"'")
        list = ['usr','Group','Team1','Team2','Goals_T1','Goals_T2','Ur_Pred_T1','Ur_Pred_T2']
        return self.render_template('comp_games.html', usrs=usrs, res=res, list=list)

    @expose('/Instructions')
    @has_access
    def Instructions(self):
        return self.render_template('Instructions.html')


class ControlView(ModelView):
    datamodel = SQLAInterface(Control)
    list_columns = ['id','user_id','name','total']

appbuilder.add_link("Instructions",label=_('Instructions'), href='/GameScores/Instructions', icon = "fa-question", category='Rules')

appbuilder.add_view(GroupsTeams, "Groups",
                    href='/groupsteams/list/1',
                    label=_('Groups'),
                    icon="fa-users",
                    category="Groups",
                    category_icon = "fa-flag")

appbuilder.add_view(TeamsView, "Teams",
                    label=_('Teams'),
                    icon = "fa-flag",
                    category="Groups")

appbuilder.add_view(GroupsView, "Edit Groups",
                    icon = "fa-users",
                    category="Groups")

appbuilder.add_view(GamesView, "Games",
                    label=_('Game Results'),
                    icon = "fa-calendar",
                    category="Game Results",
                    category_icon = "fa-list-ol")

appbuilder.add_view(Stand32View, "Standings",
                    label=_('Group Standings'),
                    icon = "fa-list-ol",
                    category="Game Results")

appbuilder.add_view(GamesView16, "Round 16",
                    label=_('Round 16'),
                    icon = "fa-calendar",
                    category="Game Results",
                    category_icon = "fa-list-ol")

appbuilder.add_view(PredictView, "Your Prediction",
                    label=_('Your Prediction'),
                    icon = "fa-futbol-o",
                    category="Your Prediction",
                    category_icon = "fa-thumbs-up")

appbuilder.add_view(UsrStand32View, "Your Group Prediction",
                    label=_('Your Group Prediction'),
                    icon = "fa-list",
                    category="Your Prediction")

appbuilder.add_view(PredictView16, "UR Pred Rnd 16",
                    label=_('UR Pred Rnd 16'),
                    icon = "fa-futbol-o",
                    category="Your Prediction",
                    category_icon = "fa-thumbs-up")

appbuilder.add_view_no_menu(AllGameScores())
appbuilder.add_link("Games Results Score", label=_('Games Results Score'), href='/GameScores/listAll/User', icon = "fa-check", category='Users Standings')
appbuilder.add_link("Group Standing Score",label=_('Group Standing Score'), href='/GameScores/list/User', icon = "fa-check", category='Users Standings')
appbuilder.add_link("Deposit your $10",label=_('Deposit your $20'), href='http://paypal.me/jcmarin/20', icon = "fa-money", category='$$$')

appbuilder.add_view(UsrScoresView, "Scores",
                    label=_('Participants Scores'),
                    icon = "fa-check",
                    category="Users Standings")

appbuilder.add_view(ControlView, "Control",
                    icon="fa-users",
                    category="Security")

appbuilder.security_cleanup()


# Application wide 404 error handler
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
