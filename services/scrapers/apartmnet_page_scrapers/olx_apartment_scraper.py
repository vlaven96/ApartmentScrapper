import requests
from bs4 import BeautifulSoup
from services.scrapers.apartmnet_page_scrapers.apartment_scraper import ApartmentScraper
from models.models import Apartment
from datetime import datetime

class OlxApartmentScraper(ApartmentScraper):
    def get_apartment(self, url: str) -> Apartment:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        title_div = soup.find("div", {"data-cy": "ad_title", "data-testid": "ad_title"})
        title = None

        if title_div:
            title_element = title_div.find("h4", class_="css-11nsr42")
            if title_element:
                title = title_element.get_text(strip=True)

        price_div = soup.find("div", {"data-testid": "ad-price-container"})
        price = None

        if price_div:
            price_element = price_div.find("h3", class_="css-uhl2ga")
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Extract only digits and join them
                price_digits = ''.join(char for char in price_text if char.isdigit())
                if price_digits:
                    price = float(price_digits)

        description_div = soup.find("div", {"data-cy": "ad_description", "data-testid": "ad_description"})
        description = None

        if description_div:
            # Find the nested div containing the actual description text
            content_div = description_div.find("div", class_="css-1o924a9")
            if content_div:
                description = content_div.get_text(separator="\n", strip=True)

        info_list = soup.find("ul", class_="css-rn93um")

        floor = None
        square_meters = None
        year_built = None

        if info_list:
            # Loop through each <li> in the <ul>
            for item in info_list.find_all("li", class_="css-1r0si1e"):
                text = item.get_text(strip=True)

                # Check for keywords in each item's text
                if "Etaj:" in text:
                    floor = text.split(":")[1].strip()
                elif "Suprafata utila:" in text:
                    try:
                        square_meters_text = text.split(":")[1].strip()
                        square_meters = float(
                            square_meters_text.split()[0])  # Extract numeric part and convert to float
                    except Exception as e:
                        square_meters = None
                elif "An constructie:" in text:
                    try:
                        year_built = int(text.split(":")[1].strip())
                    except Exception as e:
                        year_built = None

        price_square_meter = None
        if price and square_meters:
            price_square_meter = round(price / square_meters, 3)


        return Apartment(
            title=title,
            price=price,
            description=description,
            url=url,
            seen=False,
            liked=False,
            available=True,
            floor=floor,
            square_meters=square_meters,
            price_sqr_meters=price_square_meter,
            build_year=year_built,

        )
