import requests
import html2text
import time
import inc.helper as helper
import inc.RateLimit as RateLimit
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
def get_toots(max_id=None, limit=conf.SHOW_TOOTS_AT_ONCE, timelines='home', min_id=None):
    if RateLimit.rate_limit.exceeded():
        helper.print_color("Rate limit exceeded. Please wait {} seconds.".format(RateLimit.rate_limit.time_until_reset()), helper.Color.RED)
        return []

    params = {}

    if max_id:
        params["max_id"] = max_id

    if min_id:
        params["min_id"] = min_id

    if limit:
        params["limit"] = limit

    response = requests.get(base_url + "timelines/" + timelines, headers=headers, params=params)
    RateLimit.rate_limit.update(response.headers)

    # rate limit debug
    #helper.print_color(RateLimit.rate_limit, helper.Color.BLUE)

    if response.status_code == 200:
        return response.json()
    else:
        helper.print_color("Error retrieving toots. {} Code: {}".format(response.reason, response.status_code), helper.Color.RED)
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
            toot_id = None
            if toots:
                toot_id = toots[-1]["id"]

            new_toots = get_toots(toot_id)

            if new_toots:
                toots = new_toots
                display_toots(toots)
        else:
            break


def scroller_choice():
    print('1. Home / My Timeline')
    print('2. Server / Local')
    print('3. Tag / Hashtag')
    print('4. Cancel')
    print()

    choice = input("> Choose a timeline (empty for own): ").strip()
    if choice == '1' or choice == '':
        scroller('home')
    elif choice == '2':
        scroller('public')
    elif choice == '3':
        tag = input("> Enter a # tag: ")
        tag = tag.replace('#', '')
        scroller('tag/' + tag)
    #elif choice == '5':
    #    user = input("> Enter a user name: ")
    #    scroller('accounts/' + user + '/statuses')
    #elif choice == '6':
    #    search_term = input("> Enter a search term: ")
    #    scroller('search?limit=40&q=' + search_term)
    elif choice == '4':
        return
    else:
        print('Invalid choice')


def scroller(timelines='home'):
    # Get the first set of toots
    toots = get_toots(limit=1, timelines=timelines)
    toots.reverse()
    display_toots(toots)

    try:
        while True:
            toot_id = None
            if toots:
                toot_id = toots[0]["id"]

            new_toots = get_toots(limit=1, min_id=toot_id, timelines=timelines)

            if new_toots:
                toots = new_toots
                display_toots(toots)
                time.sleep(conf.SCROLLER_DELAY_HAS_TOOTS)
            else:
                time.sleep(conf.SCROLLER_DELAY_HAS_NO_TOOTS)

    except KeyboardInterrupt:
        # allow canceling the scroller
        return


if __name__ == '__main__':
    read_toots()
