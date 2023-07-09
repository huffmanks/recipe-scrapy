import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter


class RecipescraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip outer list wrapper
        list_keys = ['title', 'slug', 'description', 'categories', 'cuisine', 'keywords', 'rating', 'prepTime',
                     'cookTime', 'servings', 'nutrition', 'ingredients', 'instructions', '_status', 'datePublished', 'image_name']
        for list_key in list_keys:
            value = adapter.get(list_key)
            [adapter[list_key]] = value

        return item


class CustomImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'image_name': item["image_name"]})
                for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{request.meta["image_name"]}.jpg'
