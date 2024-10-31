from models.models import Configuration, Apartment
import requests
from bs4 import BeautifulSoup
from services.scrapers.apartmnet_page_scrapers.scrapper_filter import get_apartments_info

BASE_URL: str = "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/"
PAGE_PLACEHOLDER: str = "[PAGE_PLACEHOLDER]"
DEFAULT_MAX_PAGE = 20


def get_categories_for_year(year: int):
    if year > 2000:
        return ["dupa-2000"]
    elif year > 1990:
        return ["1990-2000", "dupa-2000"]
    elif year > 1977:
        return ["1977-1990", "1990-2000", "dupa-2000"]
    else:
        return ["inainte-de-1977", "1977-1990", "1990-2000", "dupa-2000"]


def get_filter_by_year(year: int):
    categories = get_categories_for_year(year)
    filter = ""
    index = 0
    for category in categories:
        filter += f"&search%5Bfilter_enum_constructie%5D%5B{index}%5D={category}"
        index += 1
    return filter


def get_filter_for_city(city: str):
    city = city.lower()
    city = city.replace(" ", "-")

    if city == "iasi":
        return "iasi_39939"
    elif city == "galati":
        return "galati_76959"
    elif city == "satu-mare":
        return "satu-mare_58409"
    else:
        return city


def get_rooms(min_room: int):
    if min_room >= 1:
        return [""]
    if min_room >= 2:
        return ["/2-camere" "/3-camere", "/4-camere"]
    if min_room >= 3:
        return ["/3-camere", "/4-camere"]
    if min_room >= 4:
        return ["/4-camere"]
    return [""]


def construct_url(config: Configuration):
    rooms_list = get_rooms(config.rooms)
    urls = []
    for rooms_param in rooms_list:
        url = BASE_URL + rooms_param
        url += get_filter_for_city(config.city) + "/"
        url += "?currency=EUR"
        url += f"&page={PAGE_PLACEHOLDER}"
        url += "&search%5Border%5D=created_at:desc"
        if config.compartment:
            url += f"&search%5Bfilter_enum_compartimentare%5D%5B0%5D={config.compartment.lower()}"
        if config.min_price:
            url += f"&search%5Bfilter_float_price:from%5D={config.min_price}"
        if config.max_price:
            url += f"&search%5Bfilter_float_price:to%5D={config.max_price}"
        if config.min_square_meters:
            url += f"&search%5Bfilter_float_m:from%5D={config.min_square_meters}"
        if config.max_square_meters:
            url += f"&search%5Bfilter_float_m:to%5D={config.max_square_meters}"
        if config.min_year_built:
            url += get_filter_by_year(config.min_year_built)
        urls.append(url)
    return urls


def scrape_for_template(url_template: str):
    rooms = None
    if "/4-camere" in url_template:
        rooms = 4
    elif "/3-camere" in url_template:
        rooms = 3
    elif "/2-camere" in url_template:
        rooms = 2

    stop_url = ""  # retrive by room >= current room, latest records and from the correct config
    page_num = 1
    already_processed_urls = set()
    apartment_links = []
    stop = False
    while page_num <= DEFAULT_MAX_PAGE and not stop:
        url = url_template.replace(PAGE_PLACEHOLDER, str(page_num))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all apartment listings on the current page
        listings = soup.find_all("div", {"data-cy": "l-card", "data-testid": "l-card"})

        # Loop through each listing and extract the link
        for listing in listings:
            promoted_div = listing.find("div", class_="css-1dyfc0k", string="PROMOVAT")
            if promoted_div:
                continue
            link_tag = listing.find("a", href=True)
            if link_tag:
                href = link_tag["href"]
                if not href.startswith("https://"):
                    href = "https://www.olx.ro" + href

                # Check if the URL has already been processed
                if href in already_processed_urls:
                    stop = True
                    break  # Exit the loop early if duplicate is found

                # Add the new URL to the set and the list
                already_processed_urls.add(href)
                apartment_links.append(href)

        # Exit the loop if the stop condition is met
        if stop:
            break
        # Increment the page number for the next iteration
        page_num += 1

    return apartment_links

def scrape_olx(config: Configuration):
    urls_template = construct_url(config)
    apartment_links = []
    for url_template in urls_template:
        apartment_links.extend(scrape_for_template(url_template))

    apartments: list[Apartment] = get_apartments_info(apartment_links)
    for apartment in apartments:
        apartment.configuration_id = config.id
        apartment.location = config.city
        if apartment.build_year is None:
            apartment.build_year = config.min_year_built

