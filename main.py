# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
from selenium import webdriver
from requests_html import HTMLSession
import selenium
import random
import time
import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
# driver = webdriver.Chrome(executable_path="D:\software\chromedriver_win32\chromedriver.exe")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 库
headers = {"User-Agent": random.choice(

    [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",

        "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",

        "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/78.0.3904.97 Safari/535.11"

    ]),

    "X-Forwarded-For": str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(

        random.randint(0, 255)) + "." + str(random.randint(0, 255))

}


# headers
def get_subtitle(url):

    import requests

    response = requests.get(url)
    html = response.text

    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("div", class_="c-article-header")
    journal_tag = soup.find("i")
    abs_tag = soup.find("div", class_="c-article-section__content")
    text_list = []
    # 遍历每个标签，获取它的文本，并添加到列表中
    text_list.append(journal_tag.get_text())
    text_list.append(title_tag.find("h1").text)
    if abs_tag:
        text_list.append(abs_tag.text)
    else:
        pass
    # 分期刊
    # if soup.find("section", attrs={"data-title": "Results"}):
    #     # 找到<section data-title="Results"标签
    #     section_tag = soup.find("section", attrs={"data-title": "Results"})
    #     # 在该标签下找到所有的<h3 class="c-article__sub-heading">标签
    #     h3_tags = section_tag.find_all("h3", class_="c-article__sub-heading")
    #     # 创建一个空列表，用来存储提取的文本
    #     for tag in h3_tags:
    #         text = tag.get_text()
    #         text_list.append(text)
    # elif journal_tag.get_text() == "Nature Energy":
    #     # # section_tag = soup.find_all("div", class_="c-article-section")
    #     # h2_tags = soup.find_all("h2", class_="c-article-section__title js-section-title "
    #     #                                      "js-c-reading-companion-sections-item")
    #     h2_tags = soup.find("div", class_="main-content")
    #     print(soup)
    #     # h2_text = h2_tag.text
    #     for tag in h2_tags:
    #         text = tag.get_text()
    #         text_list.append(text)
    # else:
    #     pass
    # 打印列表
    return text_list


def get_pages(page):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器（为了使网页在后台运行）
    url = "https://www.nature.com/search?q=policy%20renewable&order=relevance&page=" + str(page)
    driver.get(url=url)
    time.sleep(1)
    text = driver.page_source
    bf = BeautifulSoup(text, features="lxml")
    pic_url = bf.find_all("a", class_="c-card__link u-link-inherit")
    pagelist = []
    namelist = []  # 为了命名
    for i in pic_url:
        try:
            data = "https://www.nature.com" + i.get("href")
        except TypeError:
            continue
        pagelist.append(data)
        namelist.append(i.get("href"))
    return pagelist  # 把论文的href返回


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    df = pd.DataFrame()
    for num in range(2, 4):
        page_lists = get_pages(num)
        # url = "https://www.nature.com/articles/s41467-023-39397-2#Abs1"
        # page_lists.append(url)
        for page_list in page_lists:
            Data = get_subtitle(page_list)
            df = df._append(pd.Series(Data), ignore_index=True)
        print(str(num) + "finish")
    df.to_excel('paper_subtitle.xlsx', sheet_name='Sheet1', index=False, header=False)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
