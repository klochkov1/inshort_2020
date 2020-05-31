# INSHORT
Service for creating and managing short links. It also provides statistics 
about visits.

## About
This project is part of Group's Technology Practice in 
The Faculty of Radiophysics, Electronics and Computer Systems,
Taras Shevchenko National University of Kyiv, 2020.

## Contributors
* Andrii Kozyrskyi
* Vladyslav Myrahovskiy
* Oleksii Yermolin
* Oleksandr Klochkov

## Usage
1. Clone repository and enter project directory
`git clone https://gl.knu.ua/klochkov/inshort.git && cd inshort`  
2. Create virtual enviroment `python3 -m venv venv`
3. Activate virtual enviroment:
    * Windows: `venv\Scripts\activate`
    * Unix-like: `source venv/bin/activate` 

### Plain install with sqlite database
4. Install all dependencies `pip install -r requirements.txt`
5. Make migrations `python3 manage.py migrate`
6. Run gunicorn server `python3 manage.py runserver`

### Docker-compose instalation
4. Install [Docker Comunity Edition](https://docs.docker.com/)
    * For Ubuntu simply run `sudo apt-get install docker-ce`
    * For Fedora ` sudo dnf install docker`
5. For executing without sudo run 
   `sudo groupadd docker && sudo usermod -aG docker $USER`
6. Install docker-compose `pip3 install docker-compose`
7. Building docker container `docker-compose build`
8. Run `docker-compose up`

Login: admin passwd www12345 

