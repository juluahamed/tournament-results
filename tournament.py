#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()



def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()



def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players")
    return c.fetchone()[0]
    db.close()



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players(name) VALUES(%s)", (name,))
    db.commit()
    db.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("select players.id as id, players.name as name, CASE WHEN joined_table.wins IS NULL THEN 0 ELSE joined_table.wins END As wins, CASE WHEN joined_table.matches IS NULL THEN 0 ELSE joined_table.matches END AS matches "
			"from players left join "
			"(SELECT  CASE WHEN winners.winner IS NULL THEN losers.loser ELSE winners.winner END as id, CASE WHEN winners.a IS NULL THEN 0 ELSE winners.a END as wins, CASE WHEN losers.b IS NULL THEN 0 ELSE losers.b END as loses,( CASE WHEN winners.a IS NULL THEN 0 ELSE winners.a END + CASE WHEN losers.b IS NULL THEN 0 ELSE losers.b END) as matches FROM "
			"(select winner, count(winner) as a from matches group by winner) as winners FULL outer join "
			"(select loser, count(loser) as b from matches group by loser) as losers "
			"on winners.winner = losers.loser order by winners.a desc) as joined_table on players.id = joined_table.id order by wins")
    playerstanding = c.fetchall()
    db.close()
    return playerstanding



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches(winner, loser) VALUES(%s, %s)", (winner, loser,))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    swisspairs = []
    c.execute("SELECT id, name FROM p_standings")
    while 1:
		result = c.fetchmany(2)
		if result:
			swisspairs.append(result[0] + result[1])
		else:
			db.close()
			return swisspairs



