from bs4 import BeautifulSoup
import requests
import time

def get_book_info(page_num):
    url = f"https://book.douban.com/latest?subcat=%E5%85%A8%E9%83%A8&p={page_num}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://book.douban.com/"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_list = soup.select('ul.chart-dashed-list > li')
    
    # 检查是否还有书籍数据
    if not book_list:
        return False
        
    # 遍历每本书
    for book in book_list:
        try:
            # 提取书名
            title = book.select_one('h2.clearfix a').text.strip()
            
            # 提取作者和出版信息
            info = book.select_one('p.subject-abstract').text.strip()
            
            # 提取评价人数
            rating_people = book.select_one('span.color-gray').text.strip()
            rating_people = rating_people.replace('(', '').replace('人评价)', '')
            
            # 提取价格
            price = book.select_one('span.buy-info a').text.strip()
            
            print(f'书名：{title}')
            print(f'出版信息：{info}')
            print(f'评价人数：{rating_people}')
            print(f'价格信息：{price}')
            print('-' * 50)
            
        except AttributeError:
            continue
    
    return True

# 主程序
page = 1
while True:
    print(f"\n正在抓取第 {page} 页...")
    if not get_book_info(page):
        print(f"已到达最后一页，共抓取 {page-1} 页数据")
        break
    page += 1
    # 添加延时，避免请求过快
    time.sleep(1)

