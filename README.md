# cyber secu pollsite

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

-start your database (in a separate terminal):
 
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
   	 (flask will prompt a local address where the site is running)

---------------

FLAW 1 : Identification and Authentication Failures (OWASP Top Ten A07: 2021)
The site accepts any username and password without any checks on their length. And also the admin user is preset to the database on schema.sql with a very non secure username and password: admin, admin. 
Fixes: 
Remove the preset admin user from schema.sql: https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/schema.sql#L31

And make a admin user with these instructions:

after you have signed up you can make a user admin with psql:
    $pslq
    database=# UPDATE users WHERE username=<created user> SET admin=TRUE;

Uncomment the fix for username and password length check:
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L61-L62

Possible admins of the site should be educated and briefed about safe conduct regarding passwords and also the usage of “known” and easy to guess passwords or passwords that can be brute forced.

-------------

FLAW 2: Cryptographic Failures (OWASP Top Ten A02: 2021)

The passwords of users are stored in the database as plain text without any encryption. This is a very insecure solution to store user information.

Fixes:
Use a hash value to encrypt the password before storing it to the database:
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L66
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L68

Also when logging in you have to decrypt the password and check the decrypted password to allow user log in:
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L90-L94

Any sensitive data including eg. passwords, credit card numbers, personal info or addresses should never be stored as plain text. All sensitive data should be encrypted before it is stored so in case there is a data breach to the database the attackers are not able to use the stolen data in nefarious ways because the stolen data is not usable without the encryption key.

--------------

FLAW 3: Insecure Design (OWASP Top Ten A04: 2021)

The site is in development mode. And also the secret key is hardcoded to the app.py.
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L12

Fixes:
Even in development mode the secret key should be stored in a .env file separately as stated in the installation instructions:

    DATABASE_URL=<*>
	 SECRET_KEY=<**>

(in my case <*> is postgresql://hyxhyx and <**> is a random key I genereated)

And the .env file secret key should be addressed in the app.py:
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L13

One should have a robust checklist of things to do to a project before launching it to production. These secret key implementations and also other alterations to development code should add to the overall security to the project.

------------

FLAW 4 : Missing csrf token

Malicious users can exploit the site with attacks from multiple unknown sources with cross-site request forgery. The site actually has csrf tokens built in, but commented out.

Fixes (uncomment these):
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L72

https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L93

https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L126-L127

https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L151-L152


One other way to prevent csrf attacks are CATPCHA:s. These confirm that the user is indeed human and prevent brute force attacks by bots.

------------------

FLAW 5: Security Logging and Monitoring Failures (OWASP Top Ten A09: 2121)

By default the site has no logging of user activity. The fix has just a basic logging implementation to log user login info to a file. The site logs a successful login and a login failure due to a wrong password.

Fixes:
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L16-L38
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L98
https://github.com/aihyytiainen/cs_project_new/blob/36af497006615aedf7a8670cdcdde46a5582c7bc/app.py#L102

This is a very simple and possibly unsafe log but just an idea for real implementation. Before the site is in production there should be a robust system in place to log user activity and possible malicious activity on the site. The logs can be sent to system admins for analysis and stored securely off site. There should also be system for old log removal if the logs contain secure info about the users of the site.



