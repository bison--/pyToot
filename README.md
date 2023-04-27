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
