from services.scrapers.apartmnet_page_scrapers.olx_apartment_scraper import *
from services.scrapers.apartmnet_page_scrapers.storia_apartment_scraper import *


def get_apartments_info(apartments_urls: list[str]):
    apartments_info = []
    for ap_url in apartments_urls:
        if "olx" in ap_url:
            scraper = OlxApartmentScraper()
        elif "storia" in ap_url:
            scraper = StoriaApartmentScraper()
        else:
            print(f"The scraper for the URL '{ap_url}' is not implemented yet.")
            continue

        apartment = scraper.get_apartment(ap_url)
        apartments_info.append(apartment)

    return apartments_info
