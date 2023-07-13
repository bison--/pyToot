from conf import *

try:
    from conf_local import *
except ModuleNotFoundError:
    # local_conf.py does not exist is in theory valid, but the ACCESS_TOKEN should not be set in conf.py
    print('WARNING: conf_local.py does not exist.')

if TERMINAL_IMAGES:
    try:
        import img2unicode
    except ModuleNotFoundError:
        print('img2unicode is not installed, disabling TERMINAL_IMAGES')
        TERMINAL_IMAGES = False

if INSTANCE_USER_HANDLE == '' or INSTANCE_USER_HANDLE.startswith('<'):
    print('INSTANCE_USER_HANDLE is not set, please set it in conf_local.py')

INSTANCE_HANDLE = '@' + INSTANCE_USER_HANDLE + '@' + INSTANCE_DOMAIN

