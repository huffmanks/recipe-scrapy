from dotenv import load_dotenv
import uuid
from ingredient_parser import parse_multiple_ingredients
import scrapy
from recipescraper.items import RecipeItem
from urllib.parse import urlencode
from urllib.parse import urljoin
from slugify import slugify
import json
import os
import re
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('averaged_perceptron_tagger')
load_dotenv()


API_KEY = os.environ.get("SCRAPEOPS_API_KEY")

cuisines = ['American', 'Chinese', 'French', 'Fusion', 'Greek', 'Indian', 'Italian',
            'Japanese', 'Korean', 'Mexican', 'Middle Eastern', 'Thai', 'West African']
categories = ['Breakfast', 'Brunch', 'Lunch', 'Dinner', 'Appetizer', 'Dessert', 'Drink', 'Snack', 'Soup', 'Weeknight',
              'Beef', 'Pork', 'Chicken', 'Pasta', 'Seafood', 'Turkey', 'Vegetarian', 'Baking', 'Grill', 'Instant Pot', 'Slow Cooker']


def filter_keywords(keywords):
    keywords = keywords.split(', ')
    filtered_keywords = [
        keyword for keyword in keywords if keyword not in cuisines and keyword not in categories]
    filtered_categories = [
        category for category in categories if category in keywords]

    result = [{'keywords': ', '.join(filtered_keywords)}]

    if filtered_categories:
        result.append({'categories': filtered_categories})

    return result


def filter_categories(recipeCategory):
    filtered_categories = [
        category for category in recipeCategory if category in categories]
    return filtered_categories


def parse_iso_duration(duration_string=None):
    duration = {
        'hours': '',
        'minutes': ''
    }

    if duration_string:
        match = re.match(r'PT(\d+H)?(\d+M)?', duration_string)

        if match.group(1):
            duration['hours'] = int(match.group(1)[:-1])

        if match.group(2):
            duration['minutes'] = int(match.group(2)[:-1])

    return duration


def format_recipe_nutrition(recipe_nutrition):
    if "@type" in recipe_nutrition:
        del recipe_nutrition['@type']

    if "servingSize" in recipe_nutrition:
        del recipe_nutrition['servingSize']

    formatted_nutrition = {}

    for key, value in recipe_nutrition.items():
        quantity, unit = value.split()

        formatted_nutrition[key] = {
            'quantity': quantity,
            'unit': unit
        }

    return formatted_nutrition


def format_recipe_ingredients(recipe_ingredients):

    ingredients = parse_multiple_ingredients(recipe_ingredients)

    for ingredient in ingredients:
        ingredient['id'] = str(uuid.uuid4())
        del ingredient['other']
        if ingredient['quantity'] == '' and ingredient['unit'] == '' and ingredient['name'] == '':
            ingredient['isLabel'] = True
        else:
            ingredient['isLabel'] = False

    return ingredients


def format_recipe_instructions(recipe_instructions):
    instructions = []

    for instruction in recipe_instructions:
        if "name" in instruction:
            formatted_heading = {
                "type": "h3",
                "children": [{"text": instruction["name"]}]
            }
            instructions.append(formatted_heading)

            for sub_instruction in instruction["itemListElement"]:
                if ":" in sub_instruction["text"]:
                    heading_text = sub_instruction["text"].split(":")[0]
                    formatted_heading = {
                        "type": "h4",
                        "children": [{"text": f"{heading_text}:"}]
                    }
                    instructions.append(formatted_heading)

                    instruction_text = sub_instruction["text"].split(":")[1].strip()
                    formatted_text = {
                        "children": [{"text": instruction_text}]
                    }
                    instructions.append(formatted_text)
                else:
                    formatted_heading = {
                        "type": "h4",
                        "children": [{"text": sub_instruction["text"].strip()}]
                    }
                    instructions.append(formatted_heading)

        else:
            if ":" in instruction["text"]:
                heading_text = instruction["text"].split(":")[0]
                formatted_heading = {
                    "type": "h3",
                    "children": [{"text": f"{heading_text}:"}]
                }
                instructions.append(formatted_heading)

                instruction_text = instruction["text"].split(":")[1].strip()
                formatted_text = {
                    "children": [{"text": instruction_text}]
                }
                instructions.append(formatted_text)
            else:
                formatted_heading = {
                    "type": "h3",
                    "children": [{"text": instruction["text"].strip()}]
                }
                instructions.append(formatted_heading)

    return instructions


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


# START_URL = 'https://www.allrecipes.com/recipes/80/main-dish/'


class RecipespiderSpider(scrapy.Spider):
    name = 'recipespider'
    allowed_domains = ['allrecipes.com', 'simplyrecipes.com', 'proxy.scrapeops.io']
    # start_urls = START_URL
    with open("urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    custom_settings = {
        'FEEDS': {
            'recipedata.json': {'format': 'json', 'overwrite': True},
        }
    }

    # +++ START single URL
    # def start_requests(self):
    #     url = START_URL
    #     yield scrapy.Request(url=get_proxy_url(url), callback=self.parse_recipe_page)

    # +++ END single URL
    # +++
    # +++ START multiple URLs
    # def parse(self, response):

    #     recipes = response.css(
    #     #     # All Recipes
    #     #     # '#tax-sc__recirc-list_1-0 a').xpath("@href").getall()
    #     #     # Simply Recipes
    #         '#mntl-taxonomysc-article-list_1-0 a').xpath("@href").getall()

    #     for recipe in recipes:
    #         recipe_url = urljoin(response.url, recipe)

    #         yield scrapy.Request(url=get_proxy_url(recipe_url), callback=self.parse_recipe_page)

    # +++ END multiple URLs
    def parse(self, response):

        # LD+ json
        schemaScript = response.css('script[type="application/ld+json"]::text').get()
        data = json.loads(schemaScript)

        # Title/slug
        title = str(data[0]["headline"]).strip()
        slug = slugify(title)

        datePublished = data[0]["datePublished"]

        description = data[0]["description"]

        imageUrls = data[0]["image"]["url"]

        cuisine = data[0]["recipeCuisine"]

        groupedTags = filter_keywords(data[0]["keywords"])
        keywords = groupedTags[0]['keywords']
        categories = list(set(filter_categories(data[0]["recipeCategory"]) + groupedTags[1]['categories'])) if len(
            groupedTags) > 1 else filter_categories(data[0]["recipeCategory"])

        rating = ''
        if "aggregateRating" in data[0]:
            rating = data[0]["aggregateRating"]["ratingValue"]

        prepTime = parse_iso_duration(data[0]["prepTime"]) if "prepTime" in data[0] else parse_iso_duration()
        cookTime = parse_iso_duration(data[0]["cookTime"]) if "cookTime" in data[0] else parse_iso_duration()

        servings = data[0]["recipeYield"]
        servingQuantity = ''
        servingYield = ''

        if isinstance(servings, str):
            servingQuantity = servings

        if isinstance(servings, list):
            servingQuantity = data[0]["recipeYield"][0]
            servingYield = data[0]["recipeYield"][1]

        nutrition = format_recipe_nutrition(data[0]["nutrition"]) if "nutrition" in data[0] else None

        # Instructions and Ingredients
        instructions = format_recipe_instructions(data[0]["recipeInstructions"])
        ingredients = format_recipe_ingredients(data[0]["recipeIngredient"])

        # Recipe items
        recipe_item = RecipeItem()

        recipe_item['title'] = title,
        recipe_item['slug'] = slug,
        recipe_item['description'] = description,
        recipe_item['categories'] = categories,
        recipe_item['cuisine'] = cuisine,
        recipe_item['keywords'] = keywords,
        recipe_item['rating'] = rating,
        recipe_item['prepTime'] = prepTime,
        recipe_item['cookTime'] = cookTime,
        recipe_item['servings'] = {"quantity": servingQuantity, "yield": servingYield},
        recipe_item['nutrition'] = nutrition,
        recipe_item['ingredients'] = ingredients,
        recipe_item['instructions'] = instructions,
        recipe_item['_status'] = 'published',
        recipe_item['datePublished'] = datePublished,
        recipe_item['image_urls'] = imageUrls,
        # For multiple URL scrapes put in LIST
        # recipe_item['image_urls'] = [imageUrls],
        recipe_item['image_name'] = slug,

        yield recipe_item
