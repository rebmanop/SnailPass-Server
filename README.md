# SnailPass-REST-API
**STILL IN DEVELOPMENT**</br></br>
SnailPass is a future password manager that will be supporting three platforms: Windows, Android and IOS.
And this repository is a REST API for the project. We will be using AES-256-CBC and PBKDF2(SHA-512) algorithms to encrypt all the password data and hash master passwords.</br></br>
The goal is to copy [Bitwarden's](https://github.com/bitwarden) system architecture as close as possible.

# Documentation
**Add user**
--
  Creates new user (sign up procedure).

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
    **Content:** `{ "message": "User '&' created successfully" }`<br />
    *& - user email*
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": { "&": "& is missing" }}` <br />
    *& - required data param name*

  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{ "message": "User with received id '&' already exists }` <br />
    *& - received id*
    
  OR

  * **Code:** 409 CONFLICT <br />
    **Content:** `{ "message": "User with received email '&' already exists }` <br />
    *& - received email*
    
    
**Delete user**
--
 Deletes user based on id (authentication and admin rights required).

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
    **Content:** `{ "message": "User '&' deleted successfully" }`<br />
    *& - user email*
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": { "&": "& is missing" }}` <br />
    *& - required data param name*
    
  OR
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "message": "User with that id doesn't exist" }`
    
  OR
  
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "message": "User id not found in the request params" }`
  
    
    
