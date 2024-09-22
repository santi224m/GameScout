
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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#run-flask-app">Run Flask App</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

PC game shopping should be an easy experience. In reality, PC gamers must visit many sites to find the best games and deals. This causes shoppers to pay more than necessary or purchase games that they regret buying.
GameScout will solve this buy aggregating data from all the websites gamers must visit into a single site, making the shopping experience more pleasant.

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

### Prerequisites

Clone the repository

```bash
git clone git@github.com:santi224m/GameScout.git
cd GameScout
```

Setup a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Install and configure Redis

```bash
sudo apt install redis-server
sudo nano /etc/redis/redis.conf
```

* In the ```redis.conf``` file, change the line ```supervised no``` to ```supervised systemd```.

### Run Flask app

1. Export environment variables

```bash
export FLASK_APP=src
export FLASK_ENV=development
```

2. Run app

```bash
flask run
```

3. Open app url in browser ```http://127.0.0.1:5000```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Miro Flowchart Site Diagram
- [ ] Figma UI design
- [x] Setup Flask environment
- [ ] Document API calls
  - [ ] Steam Web API
    - [x] App Details API
    - [ ] Steam Reviews API
  - [ ] [Steam Python API](https://github.com/ValvePython/steam?tab=readme-ov-file)
  - [ ] Howlongtobeat API
    * Probably need to implement our own
  - [ ] CheapShark API
- [ ] Implement pages
  - [ ] Home page
  - [ ] Game page
  - [ ] Sign up page
  - [ ] Login page
  - [ ] Search results page
- [ ] Database
  - [ ] Database Conceptual Design
  - [ ] Database Schema
  - [ ] Setup PostgreSQL server
- [ ] Create User Accounts
- [ ] Implement wishlist
- [ ] Develop price alert system

See the [open issues](https://github.com/santi224m/GameScout/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

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