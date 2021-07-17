from requests_html import HTMLSession

class JobScraper:
    def __init__(self):
        self.URLS = {'indeed': 'https://indeed.com/jobs?q={0}&l={1}',
                     'monster': 'https://www.monster.com/jobs/search?q={0}&where={1}',
                     'linkedin': 'https://www.linkedin.com/jobs/search?keywords={0}&location={1}&pageNum=0'}

    def scrape_all(self, keyword:str, location:str):
        res = []
        for website in self.URLS:
            source = self.generate_source(keyword, location, website)
            result = self.scrape(website, source)
            for elem in result:
                res.append(elem)
        return res

    def generate_source(self, keyword:str, location:str, website:str):
        session = HTMLSession()

        url = self.URLS[website].format(keyword, location)
        s = session.get(url)
        return s

    def scrape(self, website:str, source):
        res = []
        source.html.render(sleep=1)

        if website == 'indeed':
            items = source.html.find('td.resultContent')
            for item in items:
                if len(item.find('span.salary-snippet')):
                    res.append(item.text.split("\n")[:3])
                else: res.append(item.text.split("\n"))
            for item in res:
                if item[0]=='new':
                    del item[0]
            return res
        if website == 'monster':
            try:
                items = source.html.find('div.title-company-location')
            except Exception:
                items = source.html.find('div.title-company-location')
            for item in items:
                res.append(item.text.split("\n"))
            return res
        if website == 'linkedin':
            items = source.html.find('div.base-search-card__info')
            for item in items:
                location = source.html.find('span.job-search-card__location')[0].text
                element = item.text.split('\n')[:3]
                element[2] = location
                res.append(element)
            return res

if __name__ == "__main__":
    job_scraper = JobScraper()
    print(job_scraper.scrape_all('computer science', 'california'))
    