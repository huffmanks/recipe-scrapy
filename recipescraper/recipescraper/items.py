import scrapy

# class RecipescraperItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     pass


class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    slug = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    cuisine = scrapy.Field()
    keywords = scrapy.Field()
    rating = scrapy.Field()
    prepTime = scrapy.Field()
    cookTime = scrapy.Field()
    servings = scrapy.Field()
    nutrition = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    _status = scrapy.Field()
    datePublished = scrapy.Field()
    image_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
