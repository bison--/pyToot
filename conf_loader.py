from conf import *

try:
    from conf_local import *
except ModuleNotFoundError:
    # local_conf.py does not exist is in theory valid, but the ACCESS_TOKEN should not be set in conf.py
    print('WARNING: conf_local.py does not exist.')

