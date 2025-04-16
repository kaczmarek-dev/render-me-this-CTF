# Add Python 3.8 to the image
FROM python:latest

# please review all the latest versions here:
# https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROMEDRIVER_VERSION=134.0.6998.88
ENV PREFIX=/

### install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$CHROMEDRIVER_VERSION-1_amd64.deb
RUN apt-get install -y ./google-chrome-stable_$CHROMEDRIVER_VERSION-1_amd64.deb

### install current chrome
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb


### install chromedriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod a+x start.sh

CMD ["./start.sh"]
