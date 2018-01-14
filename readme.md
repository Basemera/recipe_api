[![Build Status](https://travis-ci.org/Basemera/recipe_api.svg?branch=user_authentication)](https://travis-ci.org/Basemera/recipe_api)
[![Coverage Status](https://coveralls.io/repos/github/Basemera/recipe_api/badge.svg?branch=master)](https://coveralls.io/github/Basemera/recipe_api?branch=master)

The andela recipe api that allows users to create and manage their recipes.

Python Dependancy
Python v3.5.2 used

Installation
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
If you are on Windows, then use the following commands instead:

$ virtualenv venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt
Database Setup
Once installation is complete, we need to set up the postgres database.

Postgres installation

Use the OS link that applies to you, if it's not available please go to https://www.google.com

http://www.techrepublic.com/blog/diy-it-guy/diy-a-postgresql-database-server-setup-anyone-can-handle/ [any debian distribution]

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04 [ubuntu 16.04]

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04 [ubuntu 14.04]

https://labkey.org/Documentation/wiki-page.view?name=installPostgreSQLWindows [windows]

https://www.postgresql.org/download/windows/ [official docs windows]

https://www.postgresql.org/download/macosx/ [Mac osx]

If you're more comfortable with a desktop application give this a shot https://www.postgresapp.com

Database Setup

To set up the database, please follow this document https://www.codementor.io/devops/tutorial/getting-started-postgresql-server-mac-osx .

Follow the following instructions to get your database up and running. (Begin from step 3 if postgres is already installed, MacOsX users can use it to both install and set up)

1. Create role ‘Phiona’ with password ‘phiona’ (Step 3 A)
2. Give this role a privilege of CREATEDB (Step 3 A)
3. Create DB with name ‘recipe_api’ (Step 3 B)
The following must be done with ALL the above steps completed. Execute these commands in the order they appear.

#4 must be run only once

4. python manage.py db init
#5 and #6 must be every time you make changes to the application models

5. python manage.py db migrate
6. python manage.py db upgrade
Running
To run the server use the following command:

export the enviroment variables using the command:
source .env
Then run the server with the command flask run or python run.py
 * Serving Flask app "run"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 114-587-409
Then from a different terminal window you can send requests or an API test client like Postman.

Testing
To run the application tests, use the following command:

(recipe_api) $ py.test tests/
API Documentation
The following routes are accessible publicly i.e. you don't need to log in.

POST /register

Register a new user.
The body must contain a JSON object that defines email, ``username,password`, `confirm_password` and first_name fields.
The passwords must match and the email should have the proper email format 
On success a status code 201 is returned. The body of the response contains a JSON object with the newly added user. 
On failure an error message is returned.
Notes:

The password is hashed before it is stored in the database. Once hashed, the original password is discarded.
In a production deployment secure HTTP must be used to protect the password in transit.
POST /login

Login to access protected routes.
The body must contain a JSON object that defines username and password fields.
On success a status code 200 is returned. The body of the response contains a JSON object with the a success message and a token that should be used for subsequent requests to protected routes.
On failure status code 401 (Unauthorised) is returned with a JSON object with an error message
Notes: - The token is valid for 10 minutes

The following routes are not accessible publicly i.e. you need to log in and use your token returned on login to access them.
POST /category
Add a new recipe category.
The body must contain a JSON object that defines a category_name field.
On success a status code 201 is returned. The body of the response contains a JSON object with the newly added category.
On failure status code
- 400 is returned with a JSON object with an error message.
- 401 (unauthorized) is returned if the user is not logged in, the token is expired, invalid or the token was not provided.
PUT /category/<category_id>
Update a recipe category with category_id:category_id.
The body must contain a JSON object that defines a category_name field.
On success a status code of 201 is returned with a success message.
On failure status codes:
400 when an incorrect format for catergory name is given
404 when the category for editing doesnot exist
DELETE /category/<category_id>
Delete a recipe category with category_id:category_id.
The body must contain a JSON object that defines a category_name field.
On success a status code of 201 is returned with a success message.
On failure status codes:
404 when the category for editing doesnot exist

GET /category/search
Search for categories based on a given name parameter
On success an object containing the items that match the criteria with a code of 200.
Failure status codes.
400 if no search parameter is provided
404 if the no category satsifies the search criteria

POST /<category>/recipe
Add a new recipe to a category.
The body must contain a JSON object that defines a name and description fields.
On success a status code 201 is returned. The body of the response contains a JSON object with the newly added recipe.
On failure status code
- 400 is returned with a JSON object with an error message.
- 401 (unauthorized) is returned if the user is not logged in, the token is expired, invalid or the token was not provided.

PUT /recipes/<recipe_id>
Update a recipe with recipe_id:recipe_id.
The body must contain a JSON object that defines name and description fields.
On success a status code of 201 is returned with a success message.
On failure status codes:
400 when an incorrect format for  name is given
404 when the recipe for editing doesnot exist

DELETE /recipes/<category>/<recipe_id>
Delete a recipe with recipe_id:recipe_id.
The body must contain a JSON object that defines a category_name field.
On success a status code of 201 is returned with a success message.
On failure status codes:
404 when the recipe to be deleted doesnot exist

GET /category/recipes/search
Search for recipes based on a given name parameter
On success an object containing the items that match the criteria with a code of 200.
Failure status codes.
400 if no search parameter is provided
404 if the no recipes satsify the search criteria
