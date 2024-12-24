import os

import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from a LinkedIn profiles, Manually scrape the information from the LinkedIn profile page."""

    if mock:
        linkedin_profile_url = "https://gist.github.com/nikolas1993/f6eb2dcba5d702c0de55c05c4c931432#file-profile-info-json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        header_dict = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers=header_dict, timeout=10)

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in (None, "", []) and k not in ["people_also_viewed", "certifications"]
    }

    return data

def person_lookup_endpoint():
    """Lookup a person on LinkedIn by their name and company."""
    api_key = os.environ.get("PROXYCURL_API_KEY")
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/resolve'
    params = {
        'company_domain': 'gatesfoundation.org',
        'first_name': 'Bill',
        'similarity_checks': 'include',
        'enrich_profile': 'enrich',
        'location': 'Seattle',
        'title': 'Co-chair',
        'last_name': 'Gates',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)
    data = response.json()
    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile("https://www.linkedin.com/in/nikolas-sturaro-01376515a/"))

    #print(person_lookup_endpoint())

    #print(scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco/"))

