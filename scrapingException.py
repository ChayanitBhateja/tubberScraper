# Create ScrapingException a custom exception which will print the error sent as a message
class ScrapingException(Exception):
    def __init__(self, message):
        super().__init__(message)
        # print(f"Scraping Error: {message}")