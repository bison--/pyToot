import requests
import conf_loader as conf


def do_toot():
    # API endpoint for Mastodon
    # eg <instance_name>.mastodon.social / mastodon.social
    base_url = "https://{}/api/v1/".format(conf.INSTANCE_DOMAIN)

    # Authentication details
    headers = {"Authorization": "Bearer " + conf.ACCESS_TOKEN}

    # Get current visibility setting
    response = requests.get(base_url + "accounts/verify_credentials", headers=headers)

    visibility = 'private'  # fallback
    language = 'english'  # fallback
    if response.status_code == 200:
        visibility = response.json()["source"]["privacy"]
        language = response.json()["source"]["language"]  # iso2

        # when empty settings use "interface" language by default
        if language == '':
            language = conf.LANGUAGE
    else:
        print("Error retrieving visibility settings.")

    # show toot settings
    print('visibility:', visibility)
    print('language:', language)

    # Publish Toot
    toot_text = input('enter toot: ')
    response = requests.post(base_url + "statuses", headers=headers, json={
        "status": toot_text,
        "visibility": visibility,
        'language': language
    })

    # Check if the publication was successful
    if response.status_code == 200:
        print("Toot published!")
    else:
        print("Error publishing Toot. Error Code:", response.status_code)
