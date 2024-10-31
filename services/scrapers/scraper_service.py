from models.models import Apartment, db, Configuration
from services.scrapers.olx_scraper_service import scrape_olx
from services.scrapers.storia_scraper_service import scrape_storia


def scrape_apartments(config: Configuration):
    selected_sites = config.selected_sites.lower()
    if "olx" in selected_sites:
        scrape_olx(config)
    if "storia" in selected_sites:
        scrape_storia(config)