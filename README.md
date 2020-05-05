# INSHORT

## Practice 2020
Service like bitly.com for creating and managing short links.

## Quickstart
1. Clone repository `git clone https://gl.knu.ua/klochkov/inshort.git`
2. Create virtual enviroment `python -m venv venv`
3. Activate virtual enviroment:
    * Windows: `venv\Scripts\activate`
    * Unix-like: `source venv/bin/activate` 

### Plain install with sqlite database
4. Install all dependencies `pip install -r requirements.txt`
5. Make migrations `python manage.py migrate`
6. Run gunicorn server `python manage.py runserver`

Login: admin passwd www12345 

### Docker-compose instalation
4. Install [Docker Comunity Edition](https://docs.docker.com/)
    * For Ubuntu simply run `sudo apt-get install docker-ce`
    * For Fedora ` sudo dnf install docker`
5. For executing without sudo run `sudo groupadd docker && sudo usermod -aG docker $USER`
6. Install docker-compose `pip install docker-compose`
7. Building docker container `docker-compose build`
8. Run `docker-compose up`

Login: admin passwd www12345 

