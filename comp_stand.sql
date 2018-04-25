create view comp_stand as
select b.user_id, c.groups_id, c.name, a.pts, a.won, a.loss, a.draw, a.gf, a.ga, a.gd, 
b.pts as pts2, b.won as won2, b.loss as loss2, b.draw as draw2, b.gf as gf2, b.ga as ga2, b.gd as gd2
from stand32 as a
LEFT JOIN  usr_stand32 as b ON a.teams_id = b.teams_id
join teams as c on a.teams_id = c.id
