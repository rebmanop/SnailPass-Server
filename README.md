# SnailPass-Server

*SnailPass* is a simple, opensource and multiplatform password manager. At the moment there are clients only for [Windows](https://github.com/badlocale/SnailPass-Desktop-Client) and [Android](https://github.com/IlyaYDen/SnailPass-Android-Client). This repository is the server. *SnailPass-Server* project contains the RESTful API, database, and other core infrastructure items needed for the "backend" of all client applications.

The server project is written in Python using Flask. The codebase can be developed, built, run, and deployed cross-platform on Windows, macOS, and Linux distributions.

# How it works
Encryption in client applications implemented using a symmetric algorithm with a hashed master password as a key. At the same time a key isn't stored anywhere and never transmitted over the network. For this reason, the data can be decrypted only locally and the server stores only the cipher.
#### Cryptographic algorithms
- AES-CBC as a symmetric-key algorithm.
- Pbkdf2 as a key derivation function.
- SHA-512 as a hash function.
# Developer Documentation
Please refer to the [Deployment Guide](https://github.com/rebmanop/SnailPass-Server/edit/master/README.md#deploy) down below to quickly spin up server container. And check out [API Documentation](https://github.com/rebmanop/SnailPass-REST-api/wiki/api-Documentation) to get information about all the endpoints and request/response structure.

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

```
docker-compose build
docker-compose run -d
```

### Production configuration

```
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d
docker-compose -f docker-compose-prod.yml exec api python manage.py recreate_db 
```
**NOTE:** Execute last command in production config only if you starting container for the first time. Or if you want to **CLEAR** production database. 





    
    
