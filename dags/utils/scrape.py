import requests
import re
import typing
from bs4 import BeautifulSoup as soup
import pandas as pd
import contextlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class WeatherScraper:
    def __init__(
        self,
        chromedriver_path: str = "",
        headless: bool = True,
        remote_driver: bool = False,
        remote_url: str = "",
    ):
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = None
        self.latest_date = datetime.now() - timedelta(days=15)
        self.remote_driver = remote_driver
        self.remote_url = remote_url
        logger.info(
            "Initialized WeatherScraper with chromedriver path: %s",
            self.chromedriver_path,
        )

    def _setup_driver(self):
        logger.info("Setting up WebDriver")
        prefs = {"profile.default_content_setting_values.geolocation": 2}
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--deny-permission-prompts")
        options.add_experimental_option("prefs", prefs)

        if self.remote_driver:
            self.driver = webdriver.Remote(self.remote_url, options=options)
        else:
            service = Service(self.chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        logger.info("WebDriver setup complete")

    def _remove(self, d: list) -> list:
        return list(filter(None, [re.sub("\xa0", "", b) for b in d]))

    @contextlib.contextmanager
    def get_weather_data(
        self, url: str, by_url=True
    ) -> typing.Generator[dict, None, None]:
        d = soup(requests.get(url).text if by_url else url, "html.parser")
        _table = d.find("table", {"id": "wt-his"})
        _data = [
            [[i.text for i in c.find_all("th")], *[i.text for i in c.find_all("td")]]
            for c in _table.find_all("tr")
        ]
        [h1], [h2], *data, _ = _data
        _h2 = self._remove(h2)
        yield {
            tuple(self._remove(h1)): [
                dict(zip(_h2, self._remove([a, *i]))) for [[a], *i] in data
            ]
        }

    def _generate_url(self, month: int, year: int) -> str:
        return f"https://www.timeanddate.com/weather/vietnam/ho-chi-minh/historic?month={month}&year={year}"

    def get_latest_weather_data(self):
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        current_day = now.day

        # Generate URLs for the current and previous month
        current_month_url = self._generate_url(current_month, current_year)
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        previous_month_url = self._generate_url(previous_month, previous_year)

        logger.info(
            "Starting data scraping for the current month URL: %s", current_month_url
        )
        logger.info(
            "Starting data scraping for the previous month URL: %s", previous_month_url
        )

        self._setup_driver()
        try:
            weather_data = {}

            # Process previous month data
            self.driver.get(previous_month_url)
            dropdown = self.driver.find_element(By.ID, "wt-his-select")
            options = dropdown.find_elements(By.TAG_NAME, "option")

            for option in options:
                value = option.get_attribute("value")
                date_str = f"{value[:4]}-{value[4:6]}-{value[6:]}"
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= self.latest_date and date.month == previous_month:
                    logger.info("Processing data for %s", option.text)
                    option.click()
                    with self.get_weather_data(
                        self.driver.page_source, False
                    ) as weather:
                        weather_data[value] = weather

            # Process current month data
            self.driver.get(current_month_url)
            dropdown = self.driver.find_element(By.ID, "wt-his-select")
            options = dropdown.find_elements(By.TAG_NAME, "option")

            for option in options:
                value = option.get_attribute("value")
                date_str = f"{value[:4]}-{value[4:6]}-{value[6:]}"
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= self.latest_date and date.month == current_month:
                    logger.info("Processing data for %s", option.text)
                    option.click()
                    with self.get_weather_data(
                        self.driver.page_source, False
                    ) as weather:
                        weather_data[value] = weather

            logger.info("Data scraping completed")
            return weather_data
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
        finally:
            self.driver.quit()
            logger.info("WebDriver quit")

    def process_weather_data(self, weather_data: dict) -> pd.DataFrame:
        logger.info("Processing weather data")
        merged_df = pd.DataFrame()
        for date_key, data in weather_data.items():
            df = pd.DataFrame(data[("Conditions", "Comfort")])
            df["Time"] = df["Time"].str[:5]
            df["Time"] = df["Time"].str.strip()
            logger.debug("Time column before parsing: %s", df["Time"].head())

            date_key_clean = date_key.strip()
            logger.debug("Date key: %s", date_key_clean)

            try:
                df["Time"] = pd.to_datetime(
                    date_key_clean + " " + df["Time"],
                    format="%Y%m%d %H:%M",
                    errors="coerce",
                )
            except Exception as e:
                logger.error("Date conversion error: %s", str(e))
                continue

            df.drop(columns=["Humidity"], inplace=True)
            df.columns = ["Time", "Temp", "Weather", "Wind", "Humidity", "Barometer"]
            df.rename(
                columns={
                    "Temp": "Temperature (°C)",
                    "Wind": "Wind (km/h)",
                    "Humidity": "Humidity (%)",
                    "Barometer": "Barometer (mbar)",
                },
                inplace=True,
            )

            df["Temperature (°C)"] = (
                df["Temperature (°C)"]
                .str.extract("(\d+)", expand=False)
                .ffill()
                .astype(int)
            )
            df["Wind (km/h)"] = (
                df["Wind (km/h)"].str.extract("(\d+)", expand=False).ffill().astype(int)
            )
            df["Humidity (%)"] = (
                df["Humidity (%)"]
                .str.extract("(\d+)", expand=False)
                .ffill()
                .astype(int)
            )
            df["Barometer (mbar)"] = (
                df["Barometer (mbar)"]
                .str.extract("(\d+)", expand=False)
                .ffill()
                .astype(int)
            )

            merged_df = pd.concat([merged_df, df], ignore_index=True)
        logger.info("Weather data processing completed")
        return merged_df


if __name__ == "__main__":
    CHROMEDRIVER_PATH = "packages/chromedriver"  # Update this path

    scraper = WeatherScraper(chromedriver_path=CHROMEDRIVER_PATH)
    weather_data = scraper.get_latest_weather_data()
    processed_data = scraper.process_weather_data(weather_data)
    print(processed_data)
