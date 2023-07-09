# Scrapy settings for recipescraper project
#
#   https://docs.scrapy.org/en/latest/topics/settings.html
#   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#   https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from dotenv import load_dotenv
load_dotenv()

BOT_NAME = "recipescraper"

SPIDER_MODULES = ["recipescraper.spiders"]
NEWSPIDER_MODULE = "recipescraper.spiders"

FEEDS = {
    'recipedata.json': {'format': 'json'},
}

IMAGES_STORE = "images"

SCRAPEOPS_API_KEY = os.environ.get("SCRAPEOPS_API_KEY")
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "recipescraper.middlewares.RecipescraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
    #    'recipescraper.middlewares.ScrapeOpsProxyMiddleware': 725,
    'recipescraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
    #    "recipescraper.middlewares.RecipescraperDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "recipescraper.pipelines.RecipescraperPipeline": 300,
    "recipescraper.pipelines.CustomImagesPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
