from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(search_query: str) -> str:
    """Searches for a social profile url using the search query, usually the name of the person"""
    search = TavilySearchResults()
    res = search.run(f"{search_query}")
    return res
