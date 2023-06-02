# SnailPass-Server

<p align="center">
  <img src="https://user-images.githubusercontent.com/45130182/223817450-925448be-83a0-4ca9-9a09-d92caeacf606.svg" width=25% height=25%>
</p>

*SnailPass* is a simple, opensource and multiplatform password manager. At the moment there are clients only for [Windows](https://github.com/badlocale/SnailPass-Desktop-Client) and [Android](https://github.com/IlyaYDen/SnailPass-Android-Client). This repository is the server. *SnailPass-Server* project contains the RESTful API, database, and other core infrastructure items needed for the "backend" of all client applications.

The server project is written in Python using Flask. The codebase can be developed, built, run, and deployed cross-platform on Windows, macOS, and Linux distributions.

# How it works
Encryption in client applications implemented using a symmetric algorithm with a hashed master password as a key. At the same time the key isn't stored anywhere and never transmitted over the network. For this reason, the data can be decrypted only locally and the server stores only the cipher.
#### Cryptographic algorithms
- AES-CBC as a symmetric-key algorithm.
- Pbkdf2 as a key derivation function.
- SHA-512 as a hash function.

#### Libraries and extensions 
- `Flask-RESTful` as an extension for Flask that adds an abstraction for building REST APIs
- `SQLAlchemy` as a SQL toolkit and ORM
- `pytest` as a library for codebase testing

# Developer Documentation
Please refer to the [Deployment Guide](https://github.com/rebmanop/SnailPass-Server#deploy) down below to quickly spin up a server container. Check out [API Documentation](https://github.com/rebmanop/SnailPass-Server/wiki) to learn about all the features, endpoints and request/response structures.

# Deploy
<p align="center">
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://i.imgur.com/SZc8JnH.png" alt="docker" />
  </a>
</p>

You can deploy *SnailPass-Server* using Docker containers on Windows, macOS, and Linux distributions. Use the provided terminal commands to get started. 

### Requirements

- [Docker](https://www.docker.com/community-edition#/download)
- [Docker Compose](https://docs.docker.com/compose/install/) (already included with some Docker installations)


### Development configuration
Uses Flask's development server (port 5000) and SQLite database which recreates every time container is started. 

```
docker-compose build
docker-compose up -d
```

### Production configuration
Uses uWSGI server, postgres database and nginx as reverse proxy (port 80).
```
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d
docker-compose -f docker-compose-prod.yml exec flask python manage.py recreate_db 
```
**NOTE:** Execute last command only if you starting container for the first time or if you want to **CLEAR** production database.<br>
Production config also requires `.env`, `nginx.conf` and `uwsgi.ini` files with sensitive info in the project directory. <br><br>**`.env` file template:** 
```
PROD_POSTGRES_USER=username
PROD_POSTGRES_PASSWORD=userpassword
PROD_POSTGRES_DB=databasename
SNAILPASS_DATABASE_URI=postgresql://username:userpassword@postgres/databasename
SNAILPASS_SECRET_KEY=secretkey
MAIL_DEFAULT_SENDER=maildefaultsender
MAIL_USERNAME=mailusername
MAIL_PASSWORD=mailpassword
```
 




    
    
