import pymongo
from scrapy.utils.project import get_project_settings
from . import (GithubItem, ReleaseInfo, CommitInfo)
from dataclasses import asdict


settings = get_project_settings()


class MongoDBPipeline:

    def __init__(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )
        db = conn[settings.get('MONGO_DB_NAME')]
        self.collection = db[settings['MONGO_COLLECTION_NAME']]

    def process_item(self, item, spider):
        if isinstance(item, GithubItem):
            self.collection.update_one({"_id": item._id}, {"$set": asdict(item)}, upsert=True)
        else:
            if item.get('last_release') is not None:
                self.collection.update_one({"_id": item.get("repo_id")}, {"$set": {"last_release": asdict(item['last_release'])}}, upsert=True)
            if item.get('last_commit') is not None:
                self.collection.update_one({"_id": item.get("repo_id")}, {"$set": {"last_commit": asdict(item['last_commit'])}}, upsert=True)


        return item