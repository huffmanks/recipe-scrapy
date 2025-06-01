# Recipe Scrapy

Python tool for scraping recipes.

## Create virtual environment

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

### Exit

```shell
deactivate
```

<br />

## Install packages

```shell
python3 -m pip install {PACKAGE_NAME}
```

### Update requirements.txt

```shell
pip freeze > requirements.txt
```

### Install from requirements.txt

```shell
pip install -r requirements.txt
```

<br />

## Run shell

```shell
scrapy shell
```

```shell
fetch('URL')
```

<br />

## Run crawler

```shell
cd recipescraper/recipescraper/spiders
```

```shell
scrapy crawl recipespider
```
