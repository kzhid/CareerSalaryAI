import requests
from bs4 import BeautifulSoup
import json

class LevelsFYI:
    def __init__(self):
        pass

    def scrape(self, location, jobtitle):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

        base_url = "https://www.levels.fyi/t"
        formatted_jobtitle = jobtitle.replace(" ", "-").lower()
        formatted_location = location.replace(" ", "-").lower()

        urls = [
            f"{base_url}/{formatted_jobtitle}/locations/{formatted_location}",
            f"{base_url}/{formatted_jobtitle}/levels/entry-level/locations/{formatted_location}",
            f"{base_url}/{formatted_jobtitle}/levels/senior/locations/{formatted_location}"
        ]

        results = []
        for url in urls:
            print(f"Scraping {url}")
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                parsed_html = self._parse_html(response.text)
                salary_data = self.extract_salary_data(parsed_html)
                results.append(salary_data)
            except requests.RequestException as e:
                print(f"An error occurred while fetching the URL: {e}")
                results.append(None)

        return {
            'overall': results[0],
            'entry_level': results[1],
            'senior': results[2]
        }

    def _parse_html(self, html):
        if html:
            return BeautifulSoup(html, 'html.parser')
        return None
 
    def extract_salary_data(self, soup):
        """
        Extracts the median, 25th percentile, 75th percentile, and 90th percentile salaries from the parsed HTML.

        Returns:
            dict: A dictionary containing 'median', '25th_percentile', '75th_percentile', '90th_percentile', and 'job_title' if found, None otherwise.
        """
        median_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_median__ZQVGl > h3"
        percentile_25_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_twentyFifth__jWb67 > h6"
        percentile_75_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_seventyFifth__5JM0W > h6"
        percentile_90_selector = "#__next > div > div.MuiContainer-root.MuiContainer-maxWidthXl.job-family-page_jobFamilyContainer__fV2kV.css-yp9our > div.MuiGrid-root.MuiGrid-container.locationSlug_percentileCardContainer__lMgf9.css-1d3bbye > div > article > div > div.percentiles_statsAndSelector__tGhxk > div.percentiles_percentiles__ISt_P > div.percentiles_ninetieth__wsuGa > h6"
        job_title_selector = "#__next > div > div.job-family-header_jobFamilyHeader__qkSDj > div > div.job-family-header_headerContent__hQkdm > h1"
        
        median_element = soup.select_one(median_selector)
        percentile_25_element = soup.select_one(percentile_25_selector)
        percentile_75_element = soup.select_one(percentile_75_selector)
        percentile_90_element = soup.select_one(percentile_90_selector)
        job_title_element = soup.select_one(job_title_selector)
        
        result = {}
        
        if median_element:
            result['median'] = median_element.text.strip()
        else:
            result['median'] = "Unavailable"
        
        if percentile_25_element:
            result['25th_percentile'] = percentile_25_element.text.strip()
        else:
            result['25th_percentile'] = "Unavailable"
        
        if percentile_75_element:
            result['75th_percentile'] = percentile_75_element.text.strip()
        else:
            result['75th_percentile'] = "Unavailable"
        
        if percentile_90_element:
            result['90th_percentile'] = percentile_90_element.text.strip()
        else:
            result['90th_percentile'] = "Unavailable"
        
        if job_title_element:
            result['job_title'] = job_title_element.text.strip()
        else:
            result['job_title'] = "Unavailable"
        
        return result if result else None
    
scraper = LevelsFYI()
x = scraper.scrape("london metro area", "data scientist")

print(json.dumps(x, indent=4, sort_keys=True, ensure_ascii=False))