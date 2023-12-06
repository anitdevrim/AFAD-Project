from src.scrape import ScrapeData


def main():
    page = ScrapeData()
    page.get_url()
    page.get_all()
    #page.get_live()

main()
