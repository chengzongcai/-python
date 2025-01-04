from bs4 import BeautifulSoup
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor
import threading

def download_chapter(chapter_info):
    """下载单个章节的函数"""
    index, chapter, novel_name, headers = chapter_info
    try:
        chapter_url = f"https://www.biqukk.cc{chapter['href']}"
        chapter_title = chapter.text.strip()
        
        # 获取章节内容
        chapter_response = requests.get(chapter_url, headers=headers)
        chapter_response.encoding = 'gbk'
        chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')
        content = chapter_soup.select_one('div#content').text.strip()
        
        # 保存章节内容
        file_name = f"{index:04d}-{chapter_title}.txt"
        file_path = os.path.join(novel_name, file_name)
        
        # 使用线程锁确保文件写入安全
        with threading.Lock():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"{chapter_title}\n\n{content}")
        
        print(f"已保存: {file_name}")
        time.sleep(0.1)  # 保持小延迟
        
    except Exception as e:
        print(f"下载章节失败 {chapter_title}: {e}")

def get_novel_info():
    url = "https://www.biqukk.cc/38_38836/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.biqukk.cc/"
    }

    try:
        # 获取小说名称
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'html.parser')
        novel_name = soup.select_one('div.info h2').text.strip()
        
        # 创建小说文件夹
        if not os.path.exists(novel_name):
            os.makedirs(novel_name)
        
        # 获取章节列表
        chapter_list = soup.select('div.listmain dd a')
        
        # 准备线程池参数
        chapter_info_list = [
            (index, chapter, novel_name, headers)
            for index, chapter in enumerate(chapter_list, 1)
        ]
        
        # 使用线程池进行并发下载
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(download_chapter, chapter_info_list)
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    get_novel_info()
