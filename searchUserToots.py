import requests
import html2text
from datetime import datetime
#from inc.TerminalImage import TerminalImage
from inc.Cacher import Cacher
import inc.mastodon_helper as mastodon_helper
import conf_loader as conf
import readToots


# API endpoint for Mastodon
base_url = "https://{}/api/v1/".format(conf.INSTANCE_DOMAIN)

# Authentication details
headers = {"Authorization": "Bearer " + conf.ACCESS_TOKEN}
cacher = Cacher()


def search_user_toots(_user_name, search_term):
    user_id = mastodon_helper.get_mastodon_id(_user_name)
    for toot in cacher.get_all_cached_user_toots(user_id):
        if toot_contains(toot, search_term):
            readToots.display_toots([toot])

            #print(toot["created_at"])
            #print(toot["url"])
            #print(toot["content"])
            #print('*************')


def toot_contains(toot, search_term):
    if search_term in toot["content"].lower():
        return True

    return False


def save_toots(_toots, _user_id):
    for toot in _toots:
        cacher.save_user_toot(toot, _user_id)


def download_toots(_user_id):
    toot_counter = 0
    cacher.create_user_toots_dir(_user_id)

    toots = mastodon_helper.get_toots_from_user_id(_user_id, None)
    save_toots(toots, _user_id)
    toot_counter = len(toots)
    print('Toots:', len(toots))

    keep_running = True
    while keep_running:
        toots = mastodon_helper.get_toots_from_user_id(_user_id, toots[-1]["id"])
        save_toots(toots, _user_id)

        toot_counter += len(toots)
        print('Toots:', len(toots), toot_counter)

        keep_running = len(toots) > 0


def do_search():
    user_name = input("Enter user name/handle: ")
    if user_name == '':
        user_name = "@bison@mastodon.social"

    search_for = input("Enter search term: ")
    search_user_toots(user_name, search_for)


def do_download():
    user_name = input("Enter user name/handle: ")

    if user_name == '':
        user_name = "@bison@mastodon.social"

    user_id = mastodon_helper.get_mastodon_id(user_name)
    download_toots(user_id)


if __name__ == '__main__':
    do_search()
