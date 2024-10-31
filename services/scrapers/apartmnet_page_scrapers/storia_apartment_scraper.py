import requests
from bs4 import BeautifulSoup
from services.scrapers.apartmnet_page_scrapers.apartment_scraper import ApartmentScraper
from models.models import Apartment
import re
from datetime import datetime


class StoriaApartmentScraper(ApartmentScraper):
    def get_apartment(self, url: str) -> Apartment:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_element = soup.find("h1", {"data-cy": "adPageAdTitle", "class": "css-9pzx6y e1hgrwm21"})
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            title = None

        price_element = soup.find("strong", {"aria-label": "Preț", "data-cy": "adPageHeaderPrice"})

        # Extract the text and clean it to get the numerical price
        if price_element:
            price_text = price_element.get_text(strip=True)
            price_text = price_text.replace("€", "").replace(" ", "")
            price = float(price_text)  # Convert to a float for further processing if needed
        else:
            price = None

        info_div = soup.find("div", class_="css-58w8b7 eezlw8k0")

        square_meters = None
        rooms = None

        if info_div:
            buttons = info_div.find_all("button", class_="eezlw8k1 css-zej2ui")

            for button in buttons:
                value_div = button.find("div", class_="css-1ftqasz")
                if value_div:
                    text = value_div.get_text(strip=True)
                    if "m²" in text:
                        match = re.search(r"\d+(\.\d+)?", text)  # Find decimal number
                        if match:
                            square_meters = float(match.group())

                        # Extract rooms as integer
                    elif "camere" in text:
                        match = re.search(r"\d+", text)  # Find integer number
                        if match:
                            rooms = int(match.group())

        price_per_sqm_element = soup.find("div",
                                          {"aria-label": "Prețul pe metru pătrat", "class": "css-z3xj2a e1w5xgvx5"})
        # Extract the price per square meter and clean it
        if price_per_sqm_element:
            price_per_sqm_text = price_per_sqm_element.get_text(strip=True)
            price_per_sqm_text = price_per_sqm_text.replace("€/m²", "").replace(" ", "")
            price_per_sqm = float(price_per_sqm_text)  # Convert to float if needed
        else:
            price_per_sqm = None

        description_element = soup.find("div", {"data-cy": "adPageAdDescription", "class": "css-vefeq0 e1f0p0zw1"})
        if description_element:
            description = description_element.get_text(" ", strip=True)
        else:
            description = None

        divs = soup.find_all("div", class_="css-t7cajz e15n0fyo1")

        floor = None
        year_built = None
        for div in divs:
            label = div.find("p", class_="e15n0fyo2 css-nlohq6")  # Label (e.g., "Etaj:", "Anul construcției:")
            value = label.find_next_sibling("p") if label else None  # The following p tag contains the value
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                if "Etaj" in label_text:
                    floor = value_text
                elif "Anul construcției" in label_text:
                    year_built = int(value_text)
        published_date = None
        updated_date = None
        # Loop through each <p> element and extract dates
        for p_tag in soup.find_all("p", class_="e82kd4s2 css-1o5temi"):
            text = p_tag.get_text(strip=True)
            if "Actualizat:" in text:
                # Extract the date after "Actualizat:"
                date_str = text.split(":")[1].strip()
                try:
                    updated_date = datetime.strptime(date_str, "%d.%m.%Y")
                except ValueError as e:
                    print(f"Failed to parse updated date: {e}")
            elif "Publicat:" in text:
                # Extract the date after "Publicat:"
                date_str = text.split(":")[1].strip()
                try:
                    published_date = datetime.strptime(date_str, "%d.%m.%Y")
                except ValueError as e:
                    print(f"Failed to parse published date: {e}")

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
            price_sqr_meters=price_per_sqm,
            build_year=year_built,
            rooms=rooms,
            published_at=published_date,
            modified_at=updated_date
        )
