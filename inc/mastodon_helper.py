import requests
import conf_loader as conf
import re


# API endpoint for Mastodon
base_url = "https://{}/api/v1/".format(conf.INSTANCE_DOMAIN)

# Authentication details
headers = {"Authorization": "Bearer " + conf.ACCESS_TOKEN}


def get_toots_from_user_id(user_id, max_id=None, limit=conf.SHOW_TOOTS_AT_ONCE):
    params = {
        "exclude_reblogs": "false",
    }

    if max_id:
        params["max_id"] = max_id

    if limit:
        params["limit"] = limit

    #response = requests.get(base_url + "timelines/tag/" + username, headers=headers, params=params)
    #https://docs.joinmastodon.org/methods/accounts/#statuses
    #/api/v1/accounts/:id/statuses
    response = requests.get(base_url + f"accounts/{user_id}/statuses", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving toots.")
        return []


def get_bookmarks_from_user(max_id=None, limit=conf.SHOW_TOOTS_AT_ONCE):
    params = {}

    if max_id:
        params["max_id"] = max_id

    if limit:
        params["limit"] = limit

    #response = requests.get(base_url + "timelines/tag/" + username, headers=headers, params=params)
    #https://docs.joinmastodon.org/methods/accounts/#statuses
    #/api/v1/accounts/:id/statuses
    response = requests.get(base_url + f"bookmarks", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving toots.")
        return []


def get_mastodon_id(user_name):
    response = requests.get(base_url + f"accounts/lookup?acct=" + user_name, headers=headers)
    response.raise_for_status()  # Raise exception if the request failed

    data = response.json()

    if len(data) == 0:
        raise Exception("No user found with this handle.")

    return data["id"]


def find_mastodon_account(user_name):
    params = {
        "q": user_name
    }

    response = requests.get(base_url + f"accounts/search", headers=headers, params=params)
    response.raise_for_status()  # Raise exception if the request failed

    data = response.json()

    return data


def url_to_filename(url):
    # Remove the 'https://' part
    url = re.sub(r'https?://', '', url)

    # Replace any non-alphanumeric characters (except for underscores) with underscores
    url = re.sub(r'\W', '_', url)

    # Replace periods with underscores
    url = url.replace('.', '_')

    return url
