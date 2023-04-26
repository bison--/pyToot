import requests
from datetime import datetime
import conf


# API endpoint for Mastodon
base_url = "https://{}/api/v1/".format(conf.INSTANCE_DOMAIN)

# Authentication details
headers = {"Authorization": "Bearer " + conf.ACCESS_TOKEN}


# Get the latest toots from the home timeline
def get_toots(max_id=None):
    params = {"limit": 10}
    if max_id:
        params["max_id"] = max_id
    response = requests.get(base_url + "timelines/home", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving toots.")
        return []


# Display the toots in the terminal
def display_toots(toots):
    for toot in toots:
        toot_time = datetime.strptime(toot["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        current_time = datetime.utcnow()
        time_difference = current_time - toot_time
        print("=" * 20)
        print("Username: @" + toot["account"]["username"])
        print("Tooted on: " + toot_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Time difference: " + str(time_difference))
        print("\n" + toot["content"])


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
