import logging, datetime
from models import Predict, Games, Stand32, UsrStand32, UsrScores
from app import db

log = logging.getLogger(__name__)

def is_correct(g1,g2,g21,g22):
    return (((g1 > g2) and True) == ((g21 > g22) and True)) and (((g2 > g1) and True) == ((g22 > g21) and True))


def limit():
    now=datetime.datetime.now()
    last_day='2018-06-13'
    today=now.strftime("%Y-%m-%d")
    if (today>last_day):
        return ['']
    else:
        return ['can_list','can_edit']


def add_records(usr):
    e=db.session.query(Predict).filter_by(user = usr).count()
    if e==0:
        games=db.session.query(Games).filter_by(round = 'Round of 32')
        for r in games:
            n = Predict()
            n.round = r.round
            n.user = usr
            n.team1_id = r.team1_id
            n.team2_id = r.team2_id
            n.date = r.date
            n.stadium = r.stadium
            n.goal1 = None
            n.goal2 = None
            db.session.add(n)
        try:
            db.session.commit()
            return True
        except Exception as e:
            log.error('Group creation error: %s', e)
            db.session.rollback()
            return False
            exit(1)

    e=db.session.query(UsrStand32).filter_by(user_id = usr).count()
    if e==0:
        stand=db.session.query(Stand32).all()
        for r in stand:
            n = UsrStand32()
            n.teams_id=r.teams_id
            n.user_id=usr
            n.pts=0
            n.won=0
            n.loss=0
            n.draw=0
            n.gf=0
            n.ga=0
            n.gd=0
            db.session.add(n)
        try:
            db.session.commit()
            return True
        except Exception as e:
            log.error('UsrStand32 creation error: %s', e)
            db.session.rollback()
            return False
            exit(1)

    return True

def add_UsrScores(usr):
    e=db.session.query(UsrScores).filter_by(user_id = usr).count()
    if e==0:
        n = UsrScores()
        n.round = 'Round of 32'
        n.user_id = usr
        n.pts_total = 0
        n.pts_game = 0
        n.pts_score = 0
        n.pts_stand = 0
        db.session.add(n)
    try:
        db.session.commit()
        return True
    except Exception as e:
        log.error('UsrScores creation error: %s', e)
        db.session.rollback()
        return False
        exit(1)

    return True


def calc_stand():
    db.session.execute('UPDATE Stand32 set pts=0, won=0, loss=0, draw=0, gf=0, ga=0, gd=0')
    db.session.commit()
    e=db.session.query(Games).filter(Games.goal1 != None)
    for r in e:
        # Search Standing team_1
        x=db.session.query(Stand32).filter(Stand32.teams_id == r.team1_id)
        x[0].gf=x[0].gf+r.goal1
        x[0].ga=x[0].ga+r.goal2
        x[0].gd=x[0].gf-x[0].ga
        if r.goal1>r.goal2:
            x[0].pts=x[0].pts+3
            x[0].won=x[0].won+1
        elif r.goal1<r.goal2:
            x[0].loss=x[0].loss+1
        else:
            x[0].draw=x[0].draw+1
            x[0].pts=x[0].pts+1
        db.session.commit()
        # Search Standing team_2
        x=db.session.query(Stand32).filter(Stand32.teams_id == r.team2_id)
        x[0].gf=x[0].gf+r.goal2
        x[0].ga=x[0].ga+r.goal1
        x[0].gd=x[0].gf-x[0].ga
        if r.goal2>r.goal1:
            x[0].pts=x[0].pts+3
            x[0].won=x[0].won+1
        elif r.goal1<r.goal2:
            x[0].loss=x[0].loss+1
        else:
            x[0].draw=x[0].draw+1
            x[0].pts=x[0].pts+1
        db.session.commit()

def calc_usr_stand(usr):
    db.session.execute('UPDATE usr_stand32 set pts=0, won=0, loss=0, draw=0, gf=0, ga=0, gd=0 WHERE user_id='+str(usr))
    db.session.commit()
    e=db.session.query(Predict).filter(Predict.goal1 != None, Predict.user == usr)
    for r in e:
        # Search Standing team_1
        x=db.session.query(UsrStand32).filter(UsrStand32.teams_id == r.team1_id, UsrStand32.user_id == usr)
        x[0].gf=x[0].gf+r.goal1
        x[0].ga=x[0].ga+r.goal2
        x[0].gd=x[0].gf-x[0].ga
        if r.goal1>r.goal2:
            x[0].pts=x[0].pts+3
            x[0].won=x[0].won+1
        elif r.goal1<r.goal2:
            x[0].loss=x[0].loss+1
        else:
            x[0].draw=x[0].draw+1
            x[0].pts=x[0].pts+1
        db.session.commit()
        # Search Standing team_2
        x=db.session.query(UsrStand32).filter(UsrStand32.teams_id == r.team2_id, UsrStand32.user_id == usr)
        x[0].gf=x[0].gf+r.goal2
        x[0].ga=x[0].ga+r.goal1
        x[0].gd=x[0].gf-x[0].ga
        if r.goal2>r.goal1:
            x[0].pts=x[0].pts+3
            x[0].won=x[0].won+1
        elif r.goal1<r.goal2:
            x[0].loss=x[0].loss+1
        else:
            x[0].draw=x[0].draw+1
            x[0].pts=x[0].pts+1
        db.session.commit()


def calc_bet():
    db.session.execute('UPDATE usr_scores set pts_total=0, pts_game=0, pts_score=0, pts_stand=0')
    db.session.commit()
    e=db.session.query(Games).filter(Games.goal1 != None)
    if e.count() !=0:
        for r in e:
            x=db.session.query(Predict).filter(Predict.team1_id == r.team1_id, Predict.team2_id == r.team2_id, Predict.goal1 != None)
            if x.count() !=0:
                for i in x:
                    z=db.session.query(UsrScores).filter(UsrScores.user_id == i.user)
                    if z.count() !=0:
                        zz=z[0]
                        if is_correct(r.goal1,r.goal2,i.goal1,i.goal2):
                            zz.pts_game=zz.pts_game+1
                        if (r.goal1==i.goal1)&(r.goal2==i.goal2):
                            zz.pts_score=zz.pts_score+1
                        zz.pts_total=zz.pts_game+zz.pts_score+zz.pts_stand
                        db.session.commit()

        # if x[0].goal1 != None:
        #     if r.goal1==x[0].goal1:
        #         print 'Bingo'
        #     else:
        #         print 'Fail'
        # print x[0].goal1 , x[0].goal2
