# Render Me This CTF
Created by Mikołaj Kozok and Mateusz Kaczmarek.

## Instructions
### Run in docker
1. Default run:
```
docker build -t ctf .
docker run -p 5000:5000 ctf
```
2. Run with prefix (eg. not on `127.0.0.1:5000/`, but `127.0.0.1:5000/prefix`):

This may be helpful when running different ctfs on the same server.
```
docker build -t ctf .
docker run -p 5000:5000 -e PREFIX=/prefix ctf
```

### Run locally
1. Make sure you have both Chrome Browser and Chrome Driver installed. If not run:
```
export CHROMEDRIVER_VERSION=134.0.6998.88

wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$CHROMEDRIVER_VERSION-1_amd64.deb
apt-get install -y ./google-chrome-stable_$CHROMEDRIVER_VERSION-1_amd64.deb

wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver
```
2. Create python environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run both ctf and bot locally:
```
python3 main.py
python3 admin_bot.py
```
