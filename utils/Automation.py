from utils.Scraper import Scraper
from utils.Exporter import Exporter

class Automation:
    def __init__(self):
        pass

    def get_list_of_weblinks_for_scraping(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def run_scraping_round(self):
        list_of_links = self.get_list_of_weblinks_for_scraping("links.txt")
        
        for link in list_of_links:
            print(f"Processing link: {link}")
            scraper = Scraper()
            scraper.screenshot_active_vouchers(link)

    def run_export(self):
        exporter = Exporter()
        exporter.run()


    def run(self):
        print("Starting automation run...")
        self.run_scraping_round()
        self.run_export()
        print("Automation run completed.")