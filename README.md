# INSHORT

## Practice 2020
Service like bitly.com for creating and managing short links.

## Quickstart
1. Clone repository `git clone ssh://git@gl.knu.ua:22003/klochkov/inshort.git`
2. Create virtual enviroment `python -m venv venv`
3. Activate virtual enviroment:
    * Windows: `venv/Scripts/activate`
    * Unix-like: `source venv/bin/activate` 
4. Install all dependencies `pip install -r requirements.txt`
5. Create database tables `python manage.py migrate`
6. Run server `python manage.py runserver`

