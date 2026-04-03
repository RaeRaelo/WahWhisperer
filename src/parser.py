class BooruParser():
    def parse_post(self, raw_post: dict) -> dict:
        parsed_post = {
            "post_id": raw_post['id'],
            "author": raw_post['uploader_name'],
            "description": raw_post['description'],
            "tags": raw_post['tags'],
            "image_url": raw_post['file']['url'],
            "score": raw_post['score']
        }
        return parsed_post
