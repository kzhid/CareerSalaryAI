import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        pass

    def scrape(self):
        pass

    def start(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return self._parse_html(response.text)
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
            return None
    
    def _parse_html(self, html):
        """
        Private method to parse HTML content.
        
        Args:
            html (str): The HTML content to parse.
        
        Returns:
            BeautifulSoup: Parsed HTML object.
        """
        if html:
            self.soup = BeautifulSoup(html, 'html.parser')
            return self.soup
        return None
    def extract_salary_data(self):
        """
        Extracts the median, 25th percentile, 75th percentile, and 90th percentile salaries from the parsed HTML.

        Returns:
            dict: A dictionary containing 'median', '25th_percentile', '75th_percentile', and '90th_percentile' salaries if found, None otherwise.
        """
        median_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_median__ZQVGl > h3"
        percentile_25_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_twentyFifth__jWb67 > h6"
        percentile_75_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_seventyFifth__5JM0W > h6"
        percentile_90_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_ninetieth__wsuGa > h6"
        
        median_element = self.soup.select_one(median_selector)
        percentile_25_element = self.soup.select_one(percentile_25_selector)
        percentile_75_element = self.soup.select_one(percentile_75_selector)
        percentile_90_element = self.soup.select_one(percentile_90_selector)
        
        result = {}
        
        if median_element:
            result['median'] = median_element.text.strip()
        else:
            print("Median salary element not found.")
        
        if percentile_25_element:
            result['25th_percentile'] = percentile_25_element.text.strip()
        else:
            print("25th percentile salary element not found.")
        
        if percentile_75_element:
            result['75th_percentile'] = percentile_75_element.text.strip()
        else:
            print("75th percentile salary element not found.")
        
        if percentile_90_element:
            result['90th_percentile'] = percentile_90_element.text.strip()
        else:
            print("90th percentile salary element not found.")
        
        return result if result else None
    
scraper = Scraper()
x = scraper.start("https://www.levels.fyi/t/software-engineer/locations/london-metro-area")
y = scraper.extract_salary_data()
print(y)