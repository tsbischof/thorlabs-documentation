import bs4
import logging
import os
import pathlib
import re
import requests
from urllib.parse import urljoin
from urllib.request import urlretrieve

VERSION = "0.0.1"
THORLABS_URL_BASE = "https://www.thorlabs.de"


def fetch_soup_for_part_number(catalog_part_number: str):
    r = requests.get(
        urljoin(THORLABS_URL_BASE, "thorproduct.cfm"),
        params={"partnumber": catalog_part_number},
    )
    r.raise_for_status()
    if r.url.endswith("PageNotFound.cfm"):
        return None

    return bs4.BeautifulSoup(r.text, "html.parser")


def find_documents_in_soup(part_soup):
    for doc in part_soup.find_all("a", class_="downloadDoc"):
        product_code = doc["data-productcode"]
        filename = doc["data-filename"]
        href = urljoin(THORLABS_URL_BASE, re.sub("^/", "", doc["href"]))
        yield product_code, filename, href


def fetch_documents_for_part(catalog_part_number, db_path):
    db_path = pathlib.Path(db_path)
    logging.info(f"fetching documents for {catalog_part_number}")
    soup = fetch_soup_for_part_number(catalog_part_number)
    if not soup:
        logging.error(f"part not found: {catalog_part_number}")
        return

    for product_code, filename, href in find_documents_in_soup(soup):
        logging.debug(f"fetch? {product_code=},{filename=},{href=}")
        local_path = (
            db_path / sanitize_catalog_part_number(catalog_part_number) / filename
        )
        if not os.path.exists(local_path):
            local_path.parent.mkdir(parents=True, exist_ok=True)
            urlretrieve(href, filename=local_path)


def sanitize_catalog_part_number(catalog_part_number: str):
    """
    Part numbers may contain non-filesystem friendly characters such as /.
    This method translates the part numbers into something suitable for file storage

        :param catalog_part_number: The part number used in the Thorlabs catalog
        :type catalog_part_number: str
        :returns: url_part_number (str): An equivalent path-friendly name

    """
    number = re.sub("/", "", catalog_part_number)
    return number
