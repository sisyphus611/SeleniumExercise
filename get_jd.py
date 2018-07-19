from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from lxml import etree

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

KEYWORD = '耳机'

def page_turn(page):
    print('正在爬取第', page, '页')
    try:
        url = 'https://search.jd.com/Search?keyword=' + quote(KEYWORD) + '&enc=utf-8'
        browser.get(url)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        if page > 1:
            #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
            #submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
            #input.clear()
            #input.send_keys(page)
            #submit.click()
            input = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > input')
            submit = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > a')
            input.clear()
            input.send_keys(page)
            submit.click()


        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li')))
        get_infos()
    except TimeoutException:
        page_turn(page)

def get_infos():
    html = browser.page_source
    infos = etree.HTML(html)
    titles = infos.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i/text()')
    for title in titles:
        print(title)

MAX_PAGE = 10
def main():
    for i in range(1, MAX_PAGE + 1):
        page_turn(i)

if __name__ == '__main__':
    main()