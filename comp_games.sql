CREATE VIEW comp_games as 
select e.first_name||' '||e.last_name as name,
c.groups_id, c.name, 
d.name, b.goal1, b.goal2, a.goal1 as goal21, a.goal2 as goal22 
from Predict as a LEFT JOIN Games as b ON a.team1_id = b.team1_id and a.team2_id=b.team2_id 
join teams as c on a.team1_id = c.id 
join teams as d on a.team2_id = d.id 
join ab_user as e on a.user_id = e.id
where b.round='Round of 32'