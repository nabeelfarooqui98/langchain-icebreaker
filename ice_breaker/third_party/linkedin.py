import requests


def scrape_linkedin_profile(linkedin_url, mock=False):
    """
    Given a LinkedIn profile URL, scrape the profile and return the information
    """
    if mock:
        linkedin_url = 'https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json'
        response = requests.get(linkedin_url, timeout=10)
    else:
        response = requests.get(linkedin_url, timeout=10)

    data = response.json().get('person')
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", '', None)
        and k not in ['certifications']
    }
    return data


if __name__ == '__main__':
    linkedin_url = 'https://www.linkedin.com/in/edenmarco/'
    output = scrape_linkedin_profile(linkedin_url, True)
    print(output)
