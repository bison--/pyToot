# pyToot
a simple mastodon terminal client in python

## setup

Best you use the `requirements.txt`  
For images in terminal use `requirements-full.txt` (that's a big installation!)    

basic:  
```shell
pip install -r requirements.txt
```

full:  
```shell
pip install -r requirements-full.txt
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

### Windows CLI global

1. Create a batch file, in this example `toot.bat`, to run your Python script: 
```batch
@echo off
cd C:\Users\Gamer\Documents\Projekte\coding\python\pyToot
call .\venvs\venv3_10\Scripts\activate
python main.py %*
```
2. Add the location of your batch file to the PATH:  
To do this, right-click on 'This PC' or 'My Computer' and select 'Properties'. Then, click on 'Advanced system settings' and select 'Environment Variables'. Under 'System Variables', find the PATH variable, select it, and click on 'Edit'. In the 'Variable value' field, append the full path to the directory containing your batch file. Separate it from the existing paths by a semicolon.
3. Restart your terminal:  
After making these changes, you may need to restart your terminal (or even your computer) for the changes to take effect.

Now, you should be able to type `toot` in your terminal, and your Python script will execute, no matter which directory you're in.

### docker

Build/update the container with `dockerBuild.sh` (Mac / Linux) or `dockerBuild.bat` (Windows).    

Run the container with `dockerStart.sh` (Mac / Linux) or `dockerStart.bat` (Windows).  

## TODO

### Exceptions

No internet / network
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='mastodon.social', port=443): Max retries exceeded with url: /api/v1/timelines/home?limit=1 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x000001B051A7A3B0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
```
