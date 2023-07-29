# DON'T make changes here
# copy this file to `conf_local.py` and make your changes there
# recommended: only have variables in `conf_local.py` which you actually change

ACCESS_TOKEN = '<your access token HERE>'  # REQUIRED
INSTANCE_DOMAIN = 'mastodon.social'
INSTANCE_USER_HANDLE = ''  # REQUIRED, without @, eg: 'bison' for @bison@mastodon.social
LANGUAGE = 'en'
SHOW_TOOTS_AT_ONCE = 10

# 300 requests per 5 minutes is the limit for mastodon.social
# seconds to wait before the timeline scroller requests the next toot if there was no new toot
SCROLLER_DELAY_HAS_NO_TOOTS = 10
# time you have to read a new toot before the scroller requests the next toot
SCROLLER_DELAY_HAS_TOOTS = 5

TERMINAL_IMAGES = True  # if requirements-full.txt is not installed, this will be set to False automatically
TERMINAL_IMAGE_OPTIMIZER = 'space'

TERMINAL_IMAGE_MAX_WIDTH = -1     # -1 means auto-detected width
TERMINAL_IMAGE_MAX_HEIGHT = None  # None means scaled to width without limit
