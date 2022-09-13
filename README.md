# Kaffee Shop Full Stack ☕

## Description

Udacity's new digitally enabled café for students to order drinks, socialize, and study hard.

Built as a project in the [Udacity's Full Stack web developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Tech Stack

### 1. Backend dependencies
- **virtual environment** as a tool to create isolated Python environments
- **SQLAlchemy** as an ORM library of choice
- **SQLite** as our database of choice
- **Python3** and **Flask** as our server language and framework respectively.
- **Flask-CORS** to handle cross origin resource sharing from the client side (frontend).

### 2. Frontend dependencies
- A complete **Ionic** frontend to consume the data from the Flask server.

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── backend
  │   ├── src
  │   │   ├── auth
  │   │   │   ├── auth.py
  │   │   ├── database
  │   │   │   ├── models.py  
  │   │   ├── api.py
  │   └── requirements.txt *** The dependencies to be installed with "pip install -r requirements.txt"
  ├── frontend
  └── ├── src
      │   ├── app
      │   ├── assets
      │   ├── environments
      │   ├── index.html
      └── package.json
  ```

## Getting Started (Backend)

### Installing Dependencies

#### Python3

Follow instructions to install the latest version of python for your platform in the [python docs](https://www.python.org/downloads/)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Code for database setup can be found here; `./src/database/models.py`.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python api.py
```
[View the README.md within ./backend for more details.](./backend/README.md)

## Getting Started (frontend)

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you start up the server (backend) first following the instructions above and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

> _tip_: Do not use **ionic serve** in production. Instead, build Ionic into a build artifact for your desired platforms.
> [Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)

[View the README.md within ./frontend for more details.](./frontend/README.md)

## Deployment N/A

## Author
[Sonde Omobolaji](https://github.com/omobolajisonde)

## Acknowledgements
My awesome tutor [Gabriel Ruttner](https://www.linkedin.com/in/gruttner/) and the entire team at Udacity.