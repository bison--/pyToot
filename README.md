# pyToot
a simple mastodon terminal client in python

## setup

Best you use the `requirements.txt`  

```shell
pip install -r requirements.txt
```

## config

Copy the `conf.py` to `conf_local.py` and change the settings to your needs.

### Access Token

Create a new app under: https://YOUR_INSTANCE_DOMAIN/settings/applications    
eg: https://mastodon.social/settings/applications  

## run

Launch main.py with python

```bash
python main.py
```

### docker

Build/update the container with `dockerBuild.sh` (Mac / Linux) or `dockerBuild.bat` (Windows).    

Run the container with `dockerStart.sh` (Mac / Linux) or `dockerStart.bat` (Windows).  

## TODO

### Exceptions

No internet / network
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='mastodon.social', port=443): Max retries exceeded with url: /api/v1/timelines/home?limit=1 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x000001B051A7A3B0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
```
