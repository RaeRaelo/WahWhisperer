import requests
from pydantic import BaseModel, HttpUrl


class FetcherConfig(BaseModel):
    base_url: HttpUrl
    username: str
    project_name: str


class BooruFetcher:
    def __init__(self, config: FetcherConfig):
        self.base_url = config.base_url
        self.session = requests.Session()
        custom_agent = f"{config.project_name}/1.0 (by {config.username})"
        self.session.headers.update({'User-Agent': custom_agent})

    def fetch_posts(self, tags: str, limit: int):
        url = f"{str(self.base_url)}/posts.json"
        query_params = {
            'tags': tags,
            'limit': limit
        }
        try:
            response = self.session.get(url, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data: {e}")
            return None
