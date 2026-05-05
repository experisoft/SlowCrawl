import time
import random
import logging
from utils.Scraper import Scraper
from utils.Exporter import Exporter

logging.basicConfig(level=logging.INFO)

class Automation:
    def get_list_of_weblinks_for_scraping(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def run_scraping_round(self):
        list_of_links = self.get_list_of_weblinks_for_scraping("links.txt")
        
        for link in list_of_links:
            print(f"Processing link: {link}")
            try:
                scraper = Scraper()
                scraper.screenshot_active_vouchers(link)
                logging.info(f"Finished processing link: {link}")
            except Exception as e:
                logging.error(f"Error processing link {link}: {e}")
                
            # sleep_variance = 15
            # sleep_time = random.uniform(1, 3) + sleep_variance
            # logging.info(f"Sleeping for {sleep_time} seconds")
            # time.sleep(sleep_time)

    def run_export(self):
        exporter = Exporter()
        exporter.run()


    def run(self):
        print("Starting automation run...")
        self.run_scraping_round()
        self.run_export()
        print("Automation run completed.")