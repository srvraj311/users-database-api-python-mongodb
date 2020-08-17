# users-database-api-python-mongodb

A user authentication api build over docker container using Python and MongoDB for database

## Libraries Used
Flask - jsonify and request  
Flask_restful - Api and Resource  
Bcrypt - Hashing  
Pymongo - MongoDB 

## Features 
on localhost:5000/register  
  username and password json will register a user, no password criteria is set by default  
    
on localhost:5000/store  
  username and password that are already registered in the database and 
  a sentence field with string data that can be store on the database  
  * Password matching is done here  
 on local host:5000/get  
 you can acces the stored data frommthe database using correct username and password combo, 
 
 ### Tokens 
 on every store and get calls , one tokens get reduced , and if token is 0 , you cannot make any further calls.   
 default tokens is 6, 
 
 ### Error code
 200 - OK  
 301 - Invalid Credentials  
 302 - Out of Tokens
 
 
 
 
 #### Learned
 real- life use of database and how authentications works in real-world. Learned about hashingvalues and matching it.  
 Learned about docker , Its implementation and when and why to use it.
 Learned about Restful apis and its functions such as POST, GET, PUT , DELETE etc,  
 also implementation of it in a real life project
 
