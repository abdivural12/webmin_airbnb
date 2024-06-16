import re
import logging

import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup
from pathlib import Path

FILEPATH = Path(__file__).parent / "airbnb.txt"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


def fetch_content(url: str, from_disk: bool = False) -> str:
    """Fetch the content of the page"""

    if from_disk and FILEPATH.exists():
        return _read_from_file()

    try:
        logger.debug(f"Making request to {url}")
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        _write_to_file(content=html_content)
        return html_content
    except RequestException as e:
        logger.error(f"Couldn't fetch content from {url} due to {str(e)}")
        raise e


def _write_to_file(content: str) -> bool:
    """Write content to file"""
    logger.debug("Writing content to file")
    with open(FILEPATH, "a", encoding="utf-8") as f:
        f.write(content)

    return FILEPATH.exists()


def _read_from_file() -> str:
    """Read content from file"""
    logger.debug("Reading content from file")

    with open(FILEPATH, "r") as f:
        return f.read()


def get_average_price(html: str) -> int:
    """From the soup, we get the average price for the month"""
    prices = []

    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', itemprop="itemListElement")
    for div in divs:
        price = div.find("span", class_="_1y74zjx") or div.find("span", class_="_1l85cgq")
        if not price:
            logger.warning(f"Couldn't find price in {div}")
            continue

        price_text = price.text.strip()
        price_digits = re.sub(r"\D", "", price_text)
        if price_digits.isdigit():
            logger.debug(f"Price found : {price_digits}")
            prices.append(int(price_digits))
            clean_price = re.sub(r'[^\d€,]', '', price_text)
            print(f"Price: {clean_price}")
        else:
            logger.warning(f"Price {price_text} is not a digit")

    return prices if len(prices) else 0




