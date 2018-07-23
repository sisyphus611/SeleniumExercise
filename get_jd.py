from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from selenium.webdriver.chrome.options import Options
import pymongo
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)


def jd_search():
    '''
    获取商品页数
    '''
    try:
        browser.get('https://www.jd.com/')
        # 引入WebDriverWait对象，指定等待最长时间
        wait = WebDriverWait(browser, 10)
        # 调用WebDriverWait对象的until方法，以节点的定位元组形式传入等待条件
        input = wait.until(EC.presence_of_element_located((By.ID, 'key')))
        input.send_keys('ipad')
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button')))
        button.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        return total.text
    except TimeoutError:
        print('---error----')


def next_page():
    '''
    模拟点击下一页
    '''
    try:
        wait = WebDriverWait(browser, 10)
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.pn-next > em')))
        button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul')))
        html = browser.page_source
        parse_item(html)
    except TimeoutError:
        print('----error---')


def parse_item(html_data):
    '''
    Xpath解析页面商品信息
    '''
    page_infos = etree.HTML(html_data)
    items = page_infos.xpath('//*[@id="J_goodsList"]/ul/li')
    for item in items:
        try:
            seller = item.xpath('./div/div[5]/span/a/@title')[0]
        except IndexError:
            seller = '空'

        product = {
            'title': item.xpath('./div/div[1]/a/@title')[0],
            'price': item.xpath('./div/div[2]/strong/i/text()')[0],
            'seller': seller,
            'commit': item.xpath('./div/div[4]/strong/a/text()')[0]
        }
        save_info(product)


def save_info(result):
    '''
    爬取的数据存入MongoDB数据库
    '''

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['mydb']
    try:
        if db['jd_products'].insert(result):
            print('存储成功')
    except Exception:
        print('存储失败')


def main():
    '''
    构造翻页函数
    :return:
    '''
    total_num = jd_search()
    print(total_num)
    for page_num in range(2, int(total_num)):
        time.sleep(3)
        print('开始爬取第', page_num, '页')
        next_page()


if __name__ == '__main__':
    main()