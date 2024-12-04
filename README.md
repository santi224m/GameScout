
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/santi224m/GameScout">
    <img src="img/game-controller.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GameScout</h3>

  <p align="center">
    A better shopping experience for gamers
    <br />
    <br />
    <!-- <a href="https://github.com/santi224m/GameScout">View Demo</a>
    · -->
    <a href="https://github.com/santi224m/GameScout/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/santi224m/GameScout/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#windows">Windows</a></li>
        <li><a href="#linux">Linux</a></li>
        <li><a href="#macos">MacOS</a></li>
        <li><a href="#setting-up-steamwebapi">Setting up SteamWebAPI</a></li>
        <li><a href="#setting-up-mailersend">Setting up Mailersend</a></li>
        <li><a href="#setting-up-itad">Setting up ITAD</a></li>
        <li><a href="#setting-up-postgresql">Setting up PostgreSQL</a></li>
        <li><a href="#run-flask-app">Run Flask App</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#top-contributors">Top Contributors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

PC game shopping should be an easy experience. In reality, PC gamers must visit many sites to find the best games and deals. This causes shoppers to pay more than necessary or purchase games that they regret buying.
GameScout will solve this by aggregating data from all the websites gamers must visit into a single site, making the shopping experience more pleasant.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![HTML][HTML]][HTML-url]
* [![CSS][CSS]][CSS-url]
* [![JavaScript][JavaScript]][JavaScript-url]
* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![Postgres][Postgres]][Postgres-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Clone the repository

```bash
git clone git@github.com:santi224m/GameScout.git
cd GameScout
```

### Windows

Redis is not offically supported on Windows so you will need to set up an Ubuntu version of WSL2, instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install). After successfulyl installing WSL, follow the [Linux](#linux) instructions.

### Linux

Setup a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Install Redis

```bash
sudo apt install redis-server
sudo nano /etc/redis/redis.conf
```
#### Configure Redis

* In the ```redis.conf``` file, change the line ```supervised no``` to ```supervised systemd```.

### MacOS

#### Setup a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Install Redis
Installing Redis on macOS requires Homebrew which you can install [here](https://brew.sh/)

```bash
brew install redis
```

### Setting up SteamWebAPI
*The SteamWebAPI is used to get information about users for review data*

To start you need a SteamWebAPI key, which you can get [here](https://steamcommunity.com/dev/apikey). Once you have your key, create a new file in the root GameScout folder called `.env`. Inside your newly created `.env` file, add the following:

```yaml
STEAM_API_KEY = "{{YOUR STEAM API KEY HERE}}"
```

### Setting up Mailersend
*Mailersend is used to send out our Email Verification and Password Reset emails*

Create a [mailersend account](https://www.mailersend.com/) and generate an API Token.
Once you have your token open your `.env` file and add the following:

```yaml
MAILERSEND_API_KEY = "{{YOUR MAILERSEND API KEY HERE}}"
```

### Setting up ITAD
*The ITAD API is used to get price information for the various games*

Create an [IsThereAnyDeal account](https://isthereanydeal.com/) and create a new app [here](https://isthereanydeal.com/apps/my/). Once you have your token, open your  `.env` file and add the following:

```yaml
ITAD_API_KEY = "{{YOUR ITAD API KEY HERE}}"
```

### Setting up PostgreSQL

1. Install [PostgreSQL](https://www.postgresql.org/download/) for your operating system. \
For MacOS you could also use something like [Postgres.app](https://postgresapp.com/)

1. Run the ```setup_db.py``` script located in ```database/``` to create the database and tables in the database.

### Run Flask app

1. Add values to your `.env` file

```yaml
FLASK_APP=src
FLASK_ENV=development
```

2. Run app

```bash
flask run
```

3. Open app url in browser `http://127.0.0.1:5000` or `localhost:5000`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Figma UI design
- [x] Setup Flask environment
- [x] Document API calls
  - [x] Steam Web API
    - [x] App Details API
    - [x] Steam Reviews API
  - [x] CheapShark API
- [x] Implement pages
  - [x] Home page
    * This page should display game deals
  - [x] Game page
    * This page displays information about a particular game that the user has clicked on
  - [x] Search results page
    * This page displays games that match the user's search term
  - [x] Sign up page
  - [x] Login page
  - [x] Edit user profile page
    * This page allows users to update their profile information
  - [x] Wishlist page
    * This page allows users to view and update their game wishlist
- [x] Database
  - [x] Database Conceptual Design
  - [x] Database Schema
  - [x] Setup PostgreSQL server
- [ ] Develop price alert system
- [ ] Change/Reset Password
- [ ] Working Currency (pull GameDetails from cache but then get current pricing)
- [ ] TOS and Privacy Policy

See the [open issues](https://github.com/santi224m/GameScout/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Top Contributors

<a href="https://github.com/santi224m/GameScout/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=santi224m/GameScout" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Gamepad icons created by Smashicons - Flaticon](https://www.flaticon.com/free-icons/gamepad)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/santi224m/GameScout.svg?style=for-the-badge
[contributors-url]: https://github.com/santi224m/GameScout/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/santi224m/GameScout.svg?style=for-the-badge
[issues-url]: https://github.com/santi224m/GameScout/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge

[JavaScript]: https://img.shields.io/badge/javascript-000000?style=for-the-badge&logo=javascript
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML]: https://img.shields.io/badge/html5-000000?style=for-the-badge&logo=html5
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS]: https://img.shields.io/badge/css-000000?style=for-the-badge&logo=css3
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Postgres]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql
[Postgres-url]: https://www.postgresql.org/
