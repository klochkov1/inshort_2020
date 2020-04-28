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
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies

# Install project dependencies
RUN pip install -r requirements.txt
RUN git clone https://gl.knu.ua/klochkov/inshort.git
