import requests
from bs4 import BeautifulSoup

# example url: https://apnews.com/article/red-sea-shipping-houthi-attacks-drones-missiles-1acc4ca5ebcaf6fee932a2061d451f59

class APNewsScraper:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        if self.response.status_code != 200:
            raise Exception("Failed to load page {}".format(url))

        self.soup = BeautifulSoup(self.response.text, 'html.parser')


    def get_article_text(self) -> str:
        # Find and remove unwanted divs
        for unwanted_div in self.soup.find_all("div", {"class": "PageList-header-title"}):
            unwanted_div.decompose()

        for unwanted_div in self.soup.find_all("div", {"class": "PagePromo-content"}):
            unwanted_div.decompose()

        for unwanted_div in self.soup.find_all("div", {"class": "PageList-items-item"}):
            unwanted_div.decompose()

        for unwanted_div in self.soup.find_all("div", {"class": "Figure-content"}):
            unwanted_div.decompose()

        for unwanted_div in self.soup.find_all("div", {"class": "Enhancement"}):
            unwanted_div.decompose()

        # Now extract the main article text
        article_div = self.soup.find('div', class_='RichTextStoryBody RichTextBody')
        if article_div:
            article_text = article_div.get_text(separator=' ', strip=True)
            article_text = article_text.replace('\n\n\n', ' ').strip()

            article_text = article_text.split('___')[0] # TODO catch for errors of omissited ___

            # print(article_text)
            # Save to file
            # with open('apnews_cleaned.txt', 'w') as file:
                # file.write(article_text)
            
            return article_text

        else:
            # print("Article div not found")
            return None








# import requests
# from bs4 import BeautifulSoup

# url = "https://apnews.com/article/red-sea-shipping-houthi-attacks-drones-missiles-1acc4ca5ebcaf6fee932a2061d451f59"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find and remove unwanted divs
# for unwanted_div in soup.find_all("div", {"class": "PageList-header-title"}):
#     unwanted_div.decompose()

# for unwanted_div in soup.find_all("div", {"class": "PagePromo-content"}):
#     unwanted_div.decompose()

# for unwanted_div in soup.find_all("div", {"class": "PageList-items-item"}):
#     unwanted_div.decompose()

# for unwanted_div in soup.find_all("div", {"class": "Figure-content"}):
#     unwanted_div.decompose()

# for unwanted_div in soup.find_all("div", {"class": "Enhancement"}):
#     unwanted_div.decompose()

# # Now extract the main article text
# article_div = soup.find('div', class_='RichTextStoryBody RichTextBody')
# if article_div:
#     article_text = article_div.get_text(separator=' ', strip=True)
#     article_text = article_text.replace('\n\n\n', ' ').strip()

#     article_text = article_text.split('___')[0] # TODO catch for errors of omissited ___

#     print(article_text)
#     # Save to file
#     with open('apnews_cleaned.txt', 'w') as file:
#         file.write(article_text)

# else:
#     print("Article div not found")
