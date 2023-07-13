import requests
import html2text
from datetime import datetime
from inc.TerminalImage import TerminalImage
from inc.TootRendererBase import TootRendererBase
from inc.TootRendererSimple import TootRendererSimple
from inc.TootRendererSimpleImages import TootRendererSimpleImages
import conf_loader as conf


# API endpoint for Mastodon
base_url = "https://{}/api/v1/".format(conf.INSTANCE_DOMAIN)

# Authentication details
headers = {"Authorization": "Bearer " + conf.ACCESS_TOKEN}

html_converter = html2text.HTML2Text()
html_converter.body_width = 0
terminal_image = TerminalImage()


# Get the latest toots from the home timeline
def get_toots(max_id=None, limit=conf.SHOW_TOOTS_AT_ONCE):
    params = {}

    if max_id:
        params["max_id"] = max_id

    if limit:
        params["limit"] = limit

    response = requests.get(base_url + "timelines/home", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving toots.")
        return []


# Get the original toot for a repost
def get_original_toot(repost_id):
    response = requests.get(base_url + "statuses/" + str(repost_id), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving original toot.")
        return {}


def print_media_attachments(attachments):
    for attachment in attachments:
        if attachment["type"] == 'image':
            terminal_image.render_image(attachment["url"])

        print(attachment["type"] + ":", attachment["url"])
        print("Description:", attachment["description"])


# Display the toots in the terminal
def display_toots(toots):
    for toot in toots:
        original_toot = None
        retoot = None

        if toot.get("reblog") is not None:
            retoot = toot
            original_toot = get_original_toot(toot["reblog"]["id"])
        else:
            original_toot = toot

        toot_renderer: TootRendererBase
        if conf.TERMINAL_IMAGES:
            toot_renderer = TootRendererSimpleImages(original_toot, retoot)
        else:
            toot_renderer = TootRendererSimple(original_toot, retoot)
        toot_renderer.render()

        print('#' * 80)

    return


def read_toots():
    # Get the first set of toots
    toots = get_toots()
    display_toots(toots)

    # Prompt the user to display more toots or abort
    while True:
        print()
        print()

        more = input("> Do you want to see more toots? (Y/n) ")
        if more.lower() != "n":
            toots = get_toots(toots[-1]["id"])
            display_toots(toots)
        else:
            break


if __name__ == '__main__':
    read_toots()
