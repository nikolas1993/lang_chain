from langchain_community.tools import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res