import datetime
from flask import Markup, url_for, g
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from flask_appbuilder.models.mixins import AuditMixin, BaseMixin, FileColumn, ImageColumn
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

"""
You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who
"""

def get_user():
    usr = g.user.id
    return usr

class Control(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ab_user.id'), default=get_user, nullable=False)
    name = Column(String(10), nullable=False)
    total = Column(Integer)

    def __repr__(self):
        return self.name

class Groups(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(1), nullable=False)

    def __repr__(self):
        return self.name

class Teams(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    flag = Column(ImageColumn(size=(48, 48, True), thumbnail_size=(30, 30, True)))
    groups_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    groups = relationship("Groups")

    @renders('flag')
    def flg_img(self):
        clean = self.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' >')

    def __repr__(self):
        return self.name

class Games(Model):
    id = Column(Integer, primary_key=True)
    round = Column(String(15), nullable=False)
    team1_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team2_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team1 = relationship("Teams", foreign_keys=[team1_id])
    team2 = relationship("Teams", foreign_keys=[team2_id])
    date = Column(DateTime) # FIXME: JcMarin: Sqlite does not have dattime change for MySQL
    stadium = Column(String(25))
    goal1 = Column(Integer)
    goal2 = Column(Integer)

    def date_nice(self):
        return '{:%a, %b %d @ %H:%M}'.format(self.date)

    @renders('team1.flag')
    def flg1_img(self):
        clean = self.team1.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')

    @renders('teams2.flag')
    def flg2_img(self):
        clean = self.team2.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')


class Predict(Model):
    id = Column(Integer, primary_key=True)
    round = Column(String(15), nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'), default=get_user, nullable=False)
    ab_user = relationship("User")
    team1_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team2_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team1 = relationship("Teams", foreign_keys=[team1_id])
    team2 = relationship("Teams", foreign_keys=[team2_id])
    date = Column(DateTime)
    stadium = Column(String(25))
    goal1 = Column(Integer)
    goal2 = Column(Integer)

    def date_nice(self):
        return '{:%a, %b %d @ %H:%M}'.format(self.date)

    @renders('team1.flag')
    def flg1_img(self):
        clean = self.team1.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')

    @renders('teams2.flag')
    def flg2_img(self):
        clean = self.team2.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')


class Stand32(Model):
    id = Column(Integer, primary_key=True)
    pts = Column(Integer)
    won = Column(Integer)
    loss = Column(Integer)
    draw = Column(Integer)
    gf = Column(Integer)
    ga = Column(Integer)
    gd = Column(Integer)
    pos = Column(Integer)
    teams_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    teams = relationship("Teams")

    @renders('teams.flag')
    def flg_img(self):
        clean = self.teams.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')

class UsrStand32(Model):
    id = Column(Integer, primary_key=True)
    id_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('ab_user.id'), default=get_user, nullable=False)
    ab_user = relationship("User")
    pts = Column(Integer)
    won = Column(Integer)
    loss = Column(Integer)
    draw = Column(Integer)
    gf = Column(Integer)
    ga = Column(Integer)
    gd = Column(Integer)
    pos = Column(Integer)
    teams_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    teams = relationship("Teams")

    @renders('teams.flag')
    def flg_img(self):
        clean = self.teams.flag.replace(' ', '%20')
        return Markup('<img src=/static/flags/' + clean + ' height=30 width=30 >')

class  UsrScores(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ab_user.id'), default=get_user, nullable=False)
    ab_user = relationship("User")
    round = Column(String(15), nullable=False)
    pts_total = Column(Integer)
    pts_game = Column(Integer)
    pts_score = Column(Integer)
    pts_stand= Column(Integer)

    def __repr__(self):
        return self.name

class TmpStd(Model):
    id = Column(Integer, primary_key=True)
    id_id = Column(Integer)
    pos = Column(Integer)
    user_id = Column(Integer, default=get_user, nullable=False)

    def __repr__(self):
        return self.name
