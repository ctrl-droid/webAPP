from selenium import webdriver

class News:
    def __init__(self, title=None, writing=None, date=None, url=None):
        self.title = title
        self.writing = writing
        self.date = date
        self.url = url

    def __str__(self):
        return self.title+' / '+self.writing+' / '+self.url

class NewsService:
    def __init__(self):
        self.driver = None

    def NewsCrawler(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome(r'./static/chromedriver', chrome_options=options)
        self.driver.implicitly_wait(3)
        self.driver.get('https://land.naver.com/news/')

        newslist = []
        for i in range(1, 5):
            xpath = '//*[@id="headline_news_area"]/div[3]/ul[1]/li[' + str(i) + ']/span[2]/a/strong'
            title = self.driver.find_element_by_xpath(xpath).text
            xpath = '//*[@id="headline_news_area"]/div[3]/ul[1]/li[' + str(i) + ']/span[2]/a'
            url = self.driver.find_element_by_xpath(xpath).get_attribute('href')
            xpath = '//*[@id="headline_news_area"]/div[3]/ul[1]/li[' + str(i) + ']/span[3]'
            writing = self.driver.find_element_by_xpath(xpath).text
            xpath = '//*[@id="headline_news_area"]/div[3]/ul[1]/li[' + str(i) + ']/span[4]'
            date = self.driver.find_element_by_xpath(xpath).text
            newslist.append(News(title=title, writing=writing, date=date, url=url))
        return newslist
