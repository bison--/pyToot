from conf import *

try:
    from conf_local import *
except FileNotFoundError:
    # local conf does not exist is in theory valid, but the ACCESS_TOKEN shoulöd not be set in conf.py
    print('WARNING: conf_local.py does not exist.')

