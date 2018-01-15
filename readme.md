[![Build Status](https://travis-ci.org/Basemera/recipe_api.svg?branch=user_authentication)](https://travis-ci.org/Basemera/recipe_api)
[![Coverage Status](https://coveralls.io/repos/github/Basemera/recipe_api/badge.svg?branch=master)](https://coveralls.io/github/Basemera/recipe_api?branch=master)

The andela recipe api that allows users to create and manage their recipes.

###Python Dependancy
Python v3.6 used

###Installation
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:
```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
If you are on Windows, then use the following commands instead:
```
$ virtualenv venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt
```
###Database Setup
Once installation is complete, we need to set up the postgres database.

###Postgres installation

Use the OS link that applies to you, if it's not available please go to https://www.google.com

1) http://www.techrepublic.com/blog/diy-it-guy/diy-a-postgresql-database-server-setup-anyone-can-handle/ [any debian distribution]

2) https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04 [ubuntu 16.04]

3) https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04 [ubuntu 14.04]

4) https://labkey.org/Documentation/wiki-page.view?name=installPostgreSQLWindows [windows]

5) https://www.postgresql.org/download/windows/ [official docs windows]

6) https://www.postgresql.org/download/macosx/ [Mac osx]

If you're more comfortable with a desktop application give this a shot https://www.postgresapp.com

###Database Setup

To set up the database, please follow this document https://www.codementor.io/devops/tutorial/getting-started-postgresql-server-mac-osx .

Follow the following instructions to get your database up and running. (Begin from step 3 if postgres is already installed, MacOsX users can use it to both install and set up)

1. Create role ‘Phiona’ with password ‘phiona’ (Step 3 A)
2. Give this role a privilege of CREATEDB (Step 3 A)
3. Create DB with name ‘recipe_api’ (Step 3 B)
The following must be done with ALL the above steps completed. Execute these commands in the order they appear.
4. python manage.py db init (must be run only once)
5. python manage.py db migrate
6. python manage.py db upgrade (5 and 6 must be run every time you make changes to the application models)

###To get the application running

1. To run the server use the following command:

export the enviroment variables using the command:
```
source .env
```
2. Then run the server with the command flask run or python run.py
```
 * Serving Flask app "run"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 114-587-409
 ```
3. Then from a different terminal window you can send requests or an API test client like Postman.

###Testing

To run the application tests, use the following command:
```
(recipe_api) $ py.test tests/
```
###API Documentation
Endpoint | Functionality | Access
------------ | ------------- | -------------
POST /register | Register a new user | Public
POST /login | Login to access protected routes | Public
POST /category | Add a new recipe category | Private
GET /category/search | Search for categories based on a given name parameter | Private
PUT /category/<category_id> | Edit a category | Private
DELETE /category/<category_id> | Delete a category | Private
POST /<category>/recipes | Add a new recipe to a category | Private
PUT /category/recipes/<recipe_id> | Edit a recipe | Private
DELETE /category/<category>/recipes/<recipe_id> | Delete a recipe | Private
GET /category/<category>/recipes/search | Search for recipes based on a given name parameter | Private
POST /logout | Logout a user | Private
