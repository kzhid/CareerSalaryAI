import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
from typing import Dict, Any, List, Optional

class LevelsFYI:
    def scrape(self, location: str, jobtitle: str) -> Dict[str, Any]:
        """
        Scrape salary data for a given job title and location.

        Args:
            location (str): The location to search for.
            jobtitle (str): The job title to search for.

        Returns:
            Dict[str, Any]: A dictionary containing the scraped data and any error messages.
        """
        urls = self._generate_urls(location, jobtitle)
        results = [self._scrape_url(url) for url in urls]
        
        return {
            'status': 'success' if any(result['status'] == 'success' for result in results) else 'error',
            'data': {
                'overall': results[0],
                'entry_level': results[1],
                'senior': results[2]
            },
            'errors': [result['error'] for result in results if result['status'] == 'error']
        }

    def _generate_urls(self, location: str, jobtitle: str) -> List[str]:
        base_url = "https://www.levels.fyi/t"
        formatted_jobtitle = jobtitle.replace(" ", "-").lower()
        formatted_location = location.replace(" ", "-").lower()
        return [
            f"{base_url}/{formatted_jobtitle}/locations/{formatted_location}",
            f"{base_url}/{formatted_jobtitle}/levels/entry-level/locations/{formatted_location}",
            f"{base_url}/{formatted_jobtitle}/levels/senior/locations/{formatted_location}"
        ]

    def _scrape_url(self, url: str) -> Dict[str, Any]:
        print(f"Scraping {url}")
        try:
            response = self._make_request(url)
            parsed_html = self._parse_html(response.text)
            salary_data = self.extract_salary_data(parsed_html)
            if salary_data:
                return {'status': 'success', 'data': salary_data}
            else:
                return {'status': 'error', 'error': 'No salary data found', 'data': None}
        except requests.RequestException as e:
            return {'status': 'error', 'error': f"Request error: {str(e)}", 'data': None}
        except Exception as e:
            return {'status': 'error', 'error': f"Unexpected error: {str(e)}", 'data': None}

    def _make_request(self, url: str) -> requests.Response:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response

    def _parse_html(self, html: str) -> Optional[etree._Element]:
        return etree.HTML(html) if html else None

    def extract_salary_data(self, soup: Optional[etree._Element]) -> Optional[Dict[str, str]]:
        """
        Extracts the median, 25th percentile, 75th percentile, and 90th percentile salaries from the parsed HTML.

        Args:
            soup (Optional[etree._Element]): The parsed HTML.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing salary data if found, None otherwise.
        """
        if not soup:
            return None

        xpaths = {
            'median': '//*[@id="__next"]/div/div[2]/div[1]/div/article/div/div[1]/div[1]/h3',
            '25th_percentile': '//*[@id="__next"]/div/div[2]/div[1]/div/article/div/div[1]/div[2]/div[1]/h6',
            '75th_percentile': '//*[@id="__next"]/div/div[2]/div[1]/div/article/div/div[1]/div[2]/div[2]/h6',
            '90th_percentile': '//*[@id="__next"]/div/div[2]/div[1]/div/article/div/div[1]/div[2]/div[3]/h6',
            'job_title': '//*[@id="__next"]/div/div[1]/div/div[2]/h1'
        }

        result = {}
        for key, xpath in xpaths.items():
            element = soup.xpath(xpath)
            result[key] = element[0].text.strip() if element else "Unavailable"

        return result if any(value != "Unavailable" for value in result.values()) else None

# Example usage
if __name__ == "__main__":
    scraper = LevelsFYI()
    result = scraper.scrape("london metro area", "data scientist")
    print(json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))