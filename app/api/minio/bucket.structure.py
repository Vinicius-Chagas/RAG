from client import client

class BucketStructure:        

    def build():
        needed_buckets = ("bronze", "silver", "gold")
        for b in needed_buckets:
            if not client.bucket_exists(b):
                client.make_bucket(b)
