import argparse

from src.scraper import ListingsScraper


parser = argparse.ArgumentParser()
parser.add_argument("-release_id")


if __name__ == "__main__":
    args = parser.parse_args()
    listings = ListingsScraper().scrape(args.release_id)
