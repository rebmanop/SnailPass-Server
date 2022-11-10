# SnailPass-REST-API
**STILL IN DEVELOPMENT**</br></br>
SnailPass is a future password manager that will be supporting three platforms: Windows, Android and IOS.
And this repository is a REST API for the project. We will be using AES-256-CBC and PBKDF2(SHA-512) algorithms to encrypt all the password data and hash master passwords.</br></br>
The goal is to copy [Bitwarden's](https://github.com/bitwarden) system architecture as close as possible.

# Documentation
[Click me]((../../wiki))


All requests with required token authentication can return error messages like:
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": "Token is missing" }`
    
    OR
   
  * **Code:** 401 UNAUTHORIZED <br />
     **Content:** `{ "message": "Token is invalid" }`
     
 All admin only requests can return error messages like:
 
   * **Code:** 403 FORBIDDEN <br />
     **Content:** `{ "message": "Admin only function" }`


**Add user**
--
  Creates new user (sign up procedure)

* **URL**

  /users

* **Method:**

  `POST`

* **Data Params**

  **Required:**
 
   `"id": "[string]"` `"email": "[string]"` `"master_password_hash": "[string]"` `"nonce": "[string]"`

   **Optional:**
 
   `"hint": "[string]"`

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:** `{ "message": "User 'user@email.com' created successfully" }`<br />
  
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": { "email": "email is missing" }}` <br />
    **Note:** instead of email can be any required data param

  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{ "message": "User with received id '2d536854-e9d8-471e-1111-230bc92bfc19' already exists }` <br />
    
  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{ "message": "User with received email 'user@email.com' already exists }` <br />
    
    
**Delete user**
--
 Deletes user based on id (authentication token and admin rights required)

* **URL**

  /users

* **Method:**

  `DELETE`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure
  
* **URL Params**

  **Required:**
 
   `id=[string]` - user with that id has to be an admin

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ "message": "User 'user@email.com' deleted successfully" }`<br />
 
* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "message": "User with that id doesn't exist" }`
    
  OR
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": "User id not found in the url params" }`
    
**Login**
--
 Returns authentication token if received (basic auth) credentials are correct

* **URL**

  /login

* **Method:**

  `GET`
  
* **Basic Auth**

  **Required:**

   `username=[email]`
   `password=[master_password_hash]`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...etc" }`<br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": "Authorization info missing or it's incomplete" }` <br />
    
  OR
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{  "message": "User with recieved email 'user@email.com' doesn't exist" }`
    
  OR
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ "message": "Incorrect password" }`
    
    
**Add record**
--
  Creates new record (authentication token required)

* **URL**

  /records

* **Method:**

  `POST`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure

* **Data Params**

  **Required:**
 
   `"id": "[string]"` `"name": "[string]"` `"login": "[string]"` `"encrypted_password": "[string]"`

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:** `{ "message": "Record 'Google' created successfully (user = 'user@email.com')" }`<br />
  
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": { "name": "Record name is missing" }}` <br />
    **Note:** instead of name can be any required data param

  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{ "message": "Record with id '2d536854-3333-471e-2222-230bc92bfc19' already exist" }` <br />
    
  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{  "message": "Record with name 'Google' already exist" }` <br />
    
**Edit record**
--
  Changes fields of an existing record

* **URL**

  /records

* **Method:**

  `PATCH`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure

* **Data Params**

  **Required:**
 
   `"id": "[string]"`
   
   **Optional:**
   
   `"name": "[string]"` `"login": "[string]"` `"encrypted_password": "[string]"`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{"message": "Changes for the record '2d536854-3333-471e-2222-230bc92bfc19' were successfully made"}`<br />
  
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"message": "Changes for the record '2d536854-3333-471e-2222-230bc92bfc19' weren't made because request body is empty"}` <br />

  OR

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `{"message": "You dont have access rights to edit this record"}` <br />
    
  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"message": "Record with id '2d536854-3333-471e-2222-230bc92bfc19' doesn't exist "}` <br />
    

**Delete record**
--
 Deletes record based on record id (authentication token required)

* **URL**

  /records

* **Method:**

  `DELETE`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure
  
* **URL Params**

  **Required:**
 
   `id=[string]`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ "message": "Record 'Google' deleted successfully (user = 'user@email.com')" }`<br />
 
* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "message": "Record with that id doesn't exist" }`
    
  OR
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": "Record id not found in the url params" }`
    
  OR
  
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `{ "message": "You dont have access rights to delete this record" }`
    
    
**Get all records**
--
 Returns json with all records stored in database (authentication token and admin rights required)

* **URL**

  /records

* **Method:**

  `GET`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure, user with that token has to be an admin

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ {
        "id": "1",
        "name": "Google",
        "login": "rebmanop@email.com",
        "encrypted_password": "jlkjfadasldjq",
        "user_id": "2d536854-e9d8-471e-b55f-230bc92bfc19",
        "is_favorite": false,
        "is_deleted": false,
        "creation_time": "Fri, 04 Nov 2022 03:02:59 -0000"
    },...etc }`  <br />
 
* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ message": "No records in the database" }`
    
    
**Get all users**
--
 Returns json with all users stored in database (authentication token and admin rights required)

* **URL**

  /users

* **Method:**

  `GET`
  
* **Headers**

  **Required:**
 
   `"x-access-token": "[string]"` - token recieved after login procedure, user with that token has to be an admin

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{     {
        "id": "2d536854-e9d8-471e-b55f-230bc92bfc19",
        "email": "rebmanop@email.com",
        "master_password_hash": "ef78adbfaa17db00ff9125f0fa3476601489a1630d17c4d37d712d694a79d7dd3c60731ffe32251ff56d5c30747f1069c1fc26f52884c349986cb5eef7de7503",
        "is_admin": true
    },...etc }`  <br />
 
* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ message": "No users in the database" }`
    

    
    
