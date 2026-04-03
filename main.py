from src.fetcher import BooruFetcher, FetcherConfig
from pydantic import HttpUrl
from src.parser import BooruParser
from src.storage import DataManager
from src.publisher import TwitterConfig, TwitterPublisher
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    mconfig = FetcherConfig(
        base_url=HttpUrl("https://e621.net"),
        username="RaeRaelo",
        project_name="WahWhisperer"
    )
    fetcher = BooruFetcher(config=mconfig)
    raw_data = fetcher.fetch_posts(tags="red_panda order:random "
                                   "rating:s", limit=1)
    tconfig = None
    try:
        tconfig = TwitterConfig(
            api_key=os.getenv('TWITTER_API_KEY', ''),
            api_secret=os.getenv('TWITTER_API_SECRET', ''),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN', ''),
            access_secret=os.getenv('TWITTER_ACESS_SECRET', ''),
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN', '')
        )
        print(tconfig.api_key)
    except Exception as e:
        print(f"Error creating Twitter config: {e}")
    if tconfig is not None:
        publisher = TwitterPublisher(
            config=tconfig
        )
        if raw_data is not None:
            parser = BooruParser()
            clean_data = parser.parse_post(raw_post=raw_data['posts'][0])
            print(clean_data)
            data_outputer = DataManager("wah_data.json")
            data_outputer.save_post(clean_post=clean_data)
            publisher.post_wah(clean_data['image_url'], "test")