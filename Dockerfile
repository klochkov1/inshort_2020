FROM python:3
ENV PYTHONUNBUFFERED 1

RUN pip install django
# create and set working directory
RUN mkdir /app
WORKDIR /app


# Add current directory code to working directory
ADD requirements.txt /app
#COPY requirements.txt /app
# set default environment variables

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        mariadb-client \
	netcat \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies

# Install project dependencies
RUN pip install -r requirements.txt
RUN mkdir inshort
ADD ./ /app/inshort
#RUN git clone https://gl.knu.ua/klochkov/inshort.git
#RUN cd  ./inshort && python3 manage.py makemigrations custom_urls admin auth contenttypes sessions social_django && python manage.py migrate
