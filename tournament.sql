-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Players Table
CREATE TABLE players(
	id SERIAL PRIMARY KEY,
	name TEXT);

--Matches Table
CREATE TABLE matches(
	id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(id),
	loser INTEGER REFERENCES players(id));

--View for player standing
--Returns id, player, wins, matches of each of the registered player
CREATE VIEW player_standings AS 
	SELECT players.id AS id, players.name AS name, CASE WHEN win_lose_table.wins IS NULL THEN 0 ELSE win_lose_table.wins END AS wins,
		CASE WHEN win_lose_table.matches IS NULL THEN 0 ELSE win_lose_table.matches END AS matches 
		FROM players LEFT JOIN 
		(SELECT CASE WHEN winners_table.winner IS NULL THEN losers_table.loser ELSE winners_table.winner END AS id,
			CASE WHEN winners_table.a IS NULL THEN 0 ELSE winners_table.a END AS wins,
  			(CASE WHEN winners_table.a IS NULL THEN 0 ELSE winners_table.a END + CASE WHEN losers_table.b IS NULL THEN 0 ELSE losers_table.b END) AS matches 
  			FROM (SELECT winner, count(winner) AS a FROM matches GROUP BY winner) AS winners_table FULL OUTER JOIN 
  				 (SELECT loser, count(loser) AS b FROM matches GROUP BY loser) as losers_table 
  				 on winners_table.winner = losers_table.loser) AS win_lose_table ON players.id = win_lose_table.id ORDER BY wins;


