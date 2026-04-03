import tweepy
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

load_dotenv()


class TwitterConfig(BaseModel):
    api_key: str
    api_secret: str
    access_token: str
    access_secret: str
    bearer_token: str


class TwitterPublisher():
    def __init__(self, config: TwitterConfig):
        auth = tweepy.OAuth1UserHandler(
            config.api_key, config.api_secret, config.access_token,
            config.access_secret
        )
        self.api_v1 = tweepy.API(auth)
        self.client_v2 = tweepy.Client(
            consumer_key=config.api_key,
            consumer_secret=config.api_secret,
            access_token=config.access_token,
            access_token_secret=config.access_secret
        )

    def post_wah(self, image_url: str, caption: str):
        try:
            print(f"[1/4]Downloading image from: {image_url}")
            image = requests.get(image_url)
            image.raise_for_status()
            with open("temp.png", "wb") as e:
                e.write(image.content)
            print("[2/4] Uploading media to Twitter v1.1...")
            media_id = self.api_v1.media_upload("temp.png")
            print(f"[3/4] Media uploaded! ID: {media_id.media_id_string}. "
                  "Publishing Tweet v2...")
            self.client_v2.create_tweet(text=caption, 
                                        media_ids=[media_id.media_id_string])
            print("[4/4] Tweet published successfully! Cleaning up...")
            os.remove("temp.png")
            print("Posted")
        except Exception as e:
            print(f"Failed to post [Error]: {e}")
            os.remove("temp.png")
