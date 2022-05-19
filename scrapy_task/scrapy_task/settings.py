BOT_NAME = 'scrapy_task'

SPIDER_MODULES = ['scrapy_task.spiders']
NEWSPIDER_MODULE = 'scrapy_task.spiders'

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = "github"
MONGO_COLLECTION_NAME = "github_tb"

RETRY_HTTP_CODES = [429]

DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 5
COOKIES_ENABLED = False

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'scrapy_task.pipelines.MongoDBPipeline': 300,
}

