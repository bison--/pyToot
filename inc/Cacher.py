import hashlib
import json
import os
import requests


class Cacher:
    def __init__(self):
        self.path_images = 'cache/images'
        self.path_toots = 'cache/toots'

    def _get_cache_toot_file(self, url):
        url_hash = hashlib.md5(url).hexdigest()
        return os.path.join(self.path_toots, url_hash + '.json')

    def _get_cache_image_file(self, url):
        url_hash = hashlib.md5(url.encode()).hexdigest()
        image_extension = os.path.splitext(url)[-1]
        return os.path.join(self.path_images, url_hash + image_extension)

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

