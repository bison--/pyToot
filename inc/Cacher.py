import hashlib
import json
import os
import requests
from glob import glob
import inc.mastodon_helper as mastodon_helper


class Cacher:
    def __init__(self):
        self.path_images = 'cache/images'
        self.path_toots = 'cache/toots'
        self.path_user_toots = 'cache/user_toots'

    def _get_cache_toot_file(self, url, path_toots=None):
        if path_toots is None:
            path_toots = self.path_toots

        #url_hash = hashlib.md5(
        #   url.encode()
        #).hexdigest()

        return os.path.join(path_toots, mastodon_helper.url_to_filename(url) + '.json')

    def _get_cache_image_file(self, url):
        url_hash = hashlib.md5(url.encode()).hexdigest()
        image_extension = os.path.splitext(url)[-1]
        return os.path.join(self.path_images, url_hash + image_extension)

    def get_user_toots_dir(self, user_id):
        return os.path.join(self.path_user_toots, user_id)

    def save_toot(self, url, toot, path_toots=None, force_overwrite=False):
        file_path = self._get_cache_toot_file(url, path_toots)
        if os.path.isfile(file_path) and not force_overwrite:
            return False

        open(file_path, 'w').write(json.dumps(toot))
        return True

    def create_user_toots_dir(self, user_id):
        user_toot_dir = self.get_user_toots_dir(user_id)
        if not os.path.isdir(user_toot_dir):
            os.makedirs(user_toot_dir, exist_ok=True)

    def save_user_toot(self, toot, user_id, force_overwrite=False):
        toot_id = toot['url']
        if toot_id is None:
            print('No toot url found', toot)
            #toot_id = toot['uri']
            return False

        file_path = self._get_cache_toot_file(toot_id, os.path.join(self.path_user_toots, user_id))
        if os.path.isfile(file_path) and not force_overwrite:
            return False

        open(file_path, 'w').write(json.dumps(toot))
        return True

    def get_cached_user_toot(self, url, user_id):
        user_toot_path = os.path.join(self.path_user_toots, str(user_id))

        local_file = self._get_cache_toot_file(url, user_toot_path)

        if os.path.isfile(local_file):
            return json.loads(local_file)

        return ''

    def get_all_cached_user_toots(self, user_id):
        user_toot_path = os.path.join(self.path_user_toots, str(user_id))

        for file_name in glob(user_toot_path + '/*.json'):
            yield json.loads(open(file_name, 'r').read())

    def get_cached_toot(self, url):
        local_file = self._get_cache_toot_file(url)

        if os.path.isfile(local_file):
            return json.loads(local_file)

        return ''

    def set_cached_toot(self, url, toot):
        local_file = self._get_cache_toot_file(url)

        if os.path.isfile(local_file):
            return

        open(local_file, 'w').write(json.dumps(toot))

    def get_image_cached(self, url):
        local_file = self._get_cache_image_file(url)
        if os.path.isfile(local_file):
            return local_file

        if self._download_image(url, local_file):
            return local_file

        return None

    def _download_image(self, url, local_file):
        response = requests.get(url, stream=True)

        if response.status_code != 200:
            # print("Image '{0}' Couldn't be retrieved".format(url))
            return False

        with open(local_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return True

