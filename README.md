# tournament-results
A simple PostgreSQL database for Swiss-pairings  based tournament structure implemented with psycopg2

##Requirement
- Python Environment
- psycopg2 library
- PostgreSQL Database 

##Files
- tournament.py - python file for executing different functionalities of the tournament
- initialize_script.py - contains python scripts for genearting sample values in to table
- tournament.sql - contains SQL script to create tables and views
- tournament_test.py - tests to verify different functionalities of swiss-pair tournament

##Usage
- Open psql on command line
- Connect to your database (eg: \c tournament)
- Run the tournament.sql file to create the tables and views
``` i\ tournament.sql```
- Use initialize_script.py to generate sample values to verify the working of the tables
``` python initialize_script.py```
- Use tournament_test.py to run tests on all the functionalities of swiss-pair tournament
```python tournament_test.py```

