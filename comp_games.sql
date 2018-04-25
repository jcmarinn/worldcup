create view comp_games as
select b.user, c.groups_id, c.name, d.name, 
a.goal1, a.goal2,
b.goal1 as goal21, b.goal2 as goal22
from Games as a
LEFT JOIN  Predict as b ON a.team1_id = b.team1_id and a.team2_id=b.team2_id
join teams as c on a.team1_id = c.id
join teams as d on a.team2_id = d.id
where b.user=2
