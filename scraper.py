from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests

class JobScraper:
    def __init__(self):
        pass

    def scrape_indeed(self, keyword:str, location:str):
        res = []
        session = HTMLSession()

        url = 'https://indeed.com/jobs?q={0}&l={1}'.format(keyword.replace(' ', '+'), location)
        source = session.get(url)
        source.html.render(sleep=1, keep_page=True, scrolldown=1)

        items = source.html.find('td.resultContent')
        
        for item in items:
            res.append(item.text.split("\n"))
        for item in res:
            if item[0]=='new':
                del item[0]
        return res


    def scrape_monster(self, keyword:str, location:str):
        res = []
        session = HTMLSession()

        url = 'https://www.monster.com/jobs/search?q={0}&where={1}'.format(keyword.replace(' ', '+'), location)
        source = session.get(url)
        source.html.render(sleep=1, keep_page=True)
        try:
            items = source.html.find('div.title-company-location')
        except Exception:
            pass
        for item in items:
            res.append(item.text.split("\n"))

        return res

    def scrape_linkedin(self, keyword:str, location:str):
        res = []
        session = HTMLSession()

        url = 'https://www.linkedin.com/jobs/search?keywords={0}&location={1}&pageNum=0'.format(keyword.replace(' ', '%20'), location)
        source = session.get(url)
        source.html.render(sleep=1, keep_page=True)
        
        items = source.html.find('div.base-search-card__info')

        for item in items:
            print(item.find('span.job-search-card__location')[0].text)

if __name__ == "__main__":
    job_scraper = JobScraper()
    job_scraper.scrape_linkedin('computer science', 'california')
    #job_scraper.scrape_monster('computer science', 'california')
    #job_scraper.scrape_indeed('computer science', 'usa')
