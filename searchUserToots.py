import requests
import html2text
from datetime import datetime
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
    toot_count = 0
    for toot in cacher.get_all_cached_user_toots(user_id):
        toot_count += 1
        if toot_contains(toot, search_term):
            readToots.display_toots([toot])

        if toot_alt_contains(toot, search_term):
            readToots.display_toots([toot])

    if toot_count == 0:
        print('No local cached toots found for user: {0} ({1})'.format(_user_name, user_id))
        print('Please download toots first with option 3 in the main menu.')


def toot_contains(toot, search_term):
    if search_term in toot["content"].lower():
        return True

    return False


def toot_alt_contains(toot, search_term):
    for attachment in toot["media_attachments"]:
        if search_term in attachment["description"].lower():
            return True

    return False


def save_toots(_toots, _user_id, stop_on_cache_hit):
    for toot in _toots:
        if cacher.save_user_toot(toot, _user_id):
            continue

        if stop_on_cache_hit:
            print('Toot already cached', toot['url'])
            return False

    return True


def download_toots(_user_id, stop_on_cache_hit):
    cacher.create_user_toots_dir(_user_id)

    # always download the first block
    toots = mastodon_helper.get_toots_from_user_id(_user_id, None)
    save_toots(toots, _user_id, False)

    toot_counter = len(toots)
    print('Toots:', len(toots))

    keep_running = True
    while keep_running:
        toots = mastodon_helper.get_toots_from_user_id(_user_id, toots[-1]["id"])
        all_toots_new = save_toots(toots, _user_id, stop_on_cache_hit)

        toot_counter += len(toots)
        print('Toots:', len(toots), toot_counter)

        if stop_on_cache_hit and not all_toots_new:
            print('Cache hit, stopping.')
            keep_running = False
        else:
            keep_running = len(toots) > 0


def download_bookmarks(_user_id, stop_on_cache_hit):
    cacher.create_user_toots_dir(_user_id)

    # always download the first block
    toots = mastodon_helper.get_bookmarks_from_user()
    save_toots(toots, _user_id, False)

    toot_counter = len(toots)
    print('Toots:', len(toots))

    keep_running = True
    while keep_running:
        toots = mastodon_helper.get_bookmarks_from_user(toots[-1]["id"])
        all_toots_new = save_toots(toots, _user_id, stop_on_cache_hit)

        toot_counter += len(toots)
        print('Toots:', len(toots), toot_counter)

        if stop_on_cache_hit and not all_toots_new:
            print('Cache hit, stopping.')
            keep_running = False
        else:
            keep_running = len(toots) > 0


def do_search():
    user_name = input("Enter user name/handle (default: " + conf.INSTANCE_HANDLE + "): ")

    if user_name == '':
        user_name = conf.INSTANCE_HANDLE

    search_for = input("Enter search term: ")
    search_user_toots(user_name, search_for)


def do_download():
    user_name = input("Enter user name/handle (default: " + conf.INSTANCE_HANDLE + "): ")

    if user_name == '':
        user_name = conf.INSTANCE_HANDLE

    stop_on_cache_hit = True
    stop_on_cache_hit_user = input("Download Toots: Stop in first cache hit? (Y/n)")
    if stop_on_cache_hit_user == 'n':
        stop_on_cache_hit = False

    user_id = mastodon_helper.get_mastodon_id(user_name)
    download_toots(user_id, stop_on_cache_hit)

    # currently broken
    #stop_on_cache_hit_user = input("Download Bookmarks: Stop in first cache hit? (Y/n)")
    #if stop_on_cache_hit_user == 'n':
    #    stop_on_cache_hit = False

    #download_bookmarks(user_id, stop_on_cache_hit)


if __name__ == '__main__':
    do_search()
