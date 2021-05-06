FROM selenium/standalone-chrome:85.0
USER seluser
COPY main.py requirements.txt /app/
COPY chromedriver /usr/local/bin
WORKDIR /app
RUN set -xe \
    && apt-get update \
    && apt-get install python-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python main.py
# CMD echo $PATH

# build image: docker build -t test-alpha-crawler .
# run container: docker run test-alpha-crawler