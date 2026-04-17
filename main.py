from src.fetcher import BooruFetcher, FetcherConfig
from pydantic import HttpUrl
from src.parser import BooruParser
from src.storage import DataManager

if __name__ == "__main__":
    mconfig = FetcherConfig(
        base_url=HttpUrl("https://example.net"),
        username="Example",
        project_name="WahWhisperer"
    )
    fetcher = BooruFetcher(config=mconfig)
    raw_data = fetcher.fetch_posts(tags="red_panda", limit=1)
    if raw_data is not None:
        parser = BooruParser()
        clean_data = parser.parse_post(raw_post=raw_data['posts'][0])
        print(clean_data)
        data_outputer = DataManager("wah_data.json")
        data_outputer.save_post(clean_post=clean_data)
