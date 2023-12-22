# cs_project_new

This site is not in production, you have to run it locally

Installation (linux):
----------------
-clone this repo to your local machine

-create .env file to the root folder of the cloned folder and make it say this:

	DATABASE_URL=<*>
 	SECRET_KEY=<**>

	(in my case <*> is postgresql://hyxhyx and <**> is a random key I genereated)

-activate virtual environment and install dependencies with these commands in project folder:

 	$ python3 -m venv venv
	$ source venv/bin/activate
	$ pip install -r ./requirements.txt

-start your database:
	
 	$ start-pg.sh

-define the schema of the project database:
	
 	>option 1 (if your database has no same tables as this project):
		$ psql < schema.sql
	>option 2 (if you know or suspect your database has same tables as this project):
		+run psql and create a new database:
			$ psql
			user=# CREATE DATABASE <new_database>;
			$ psql -d <new_database> < schema.sql
		+in the project folder modify .env to point to this new database
			if you named your database testi, then in .evn:
				DATABASE_URL=portgresql://testi
-run the project:
	
 	$ flask run
		(flask will propt a local address where the site is running)

-make an admin user:

	after you have signed up you can make a user admin with psql:
		$pslq
		database=# UPDATE users WHERE username=<created user> SET admin=TRUE;

----------

