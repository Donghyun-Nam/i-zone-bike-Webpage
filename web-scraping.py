from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
path = "C:/Users/DongHyeon_Nam/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path, options=options)
driver.get("https://www.samchuly.co.kr/index.php/bicycle/style?code=T003001")
driver.implicitly_wait(1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
bikes = soup.select('#series_S000001 > div > ul.prodt_lst > li')
print(bikes)
for bike in bikes:
    name = bike.select_one('a > div.prodt_Info > strong').get_text()
    tag = bike.select_one('ul').get_text().split('#')
    del tag[0]
    img = bike.select_one('a > div.prodt_Img > img')['src']
    size = bike.select_one('a > div.prodt_Info > strong > span')
    # list(db.bikes.find({}, {'_id': 0}))
    print(name, tag, img, size.text)
    doc = {
        'name': name,
        'tag': tag,
        'img': 'www.samchuly.co.kr' + img  # DB에는 숫자처럼 생긴 문자열 형태로 저장됩니다.
    }
    db.bikes.insert_one(doc)