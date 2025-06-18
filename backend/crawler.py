import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time
import re


def get_article_details(article_url):
    """
    获取单篇文章的详细信息
    """
    try:
        response = requests.get(article_url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取标题
        title = soup.find('div', class_='title').find('h2').get_text(strip=True)

        # 提取日期和来源
        art_ori = soup.find('div', class_='artOri')
        date_source = art_ori.get_text(strip=True)

        # 使用正则表达式提取日期和来源
        date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{2})', date_source)
        date = date_match.group(1) if date_match else ""

        source_match = re.search(r'来源：(.+?)(?:\||<|$)', date_source)
        source = source_match.group(1).strip() if source_match else ""

        # 提取内容
        content_div = soup.find('div', class_='artDet')
        paragraphs = content_div.find_all('p', style='text-indent: 2em;')
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])

        return {
            "title": title,
            "date": date,
            "source": source,
            "content": content
        }
    except Exception as e:
        print(f"Error processing article {article_url}: {str(e)}")
        return None


def crawl_health_articles(base_url, max_pages=5):
    """
    爬取养生栏目的所有文章
    """
    documents = []
    article_id = 1

    for page in range(1, max_pages + 1):
        if page == 1:
            page_url = base_url
        else:
            page_url = urljoin(base_url, f"index{page}.html")

        print(f"Processing page {page}: {page_url}")

        try:
            response = requests.get(page_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取文章列表
            news_items = soup.find('ul', class_='list_02').find_all('div', class_='newsItems')

            for item in news_items:
                link = item.find('a')
                if not link:
                    continue

                article_url = urljoin(base_url, link['href'])
                print(f"Processing article {article_id}: {article_url}")

                article_details = get_article_details(article_url)
                if article_details:
                    documents.append({
                        "_id": str(article_id),
                        "_source": {
                            "title": article_details["title"],
                            "author": article_details["source"],
                            "date": article_details["date"],
                            "content": article_details["content"]
                        }
                    })
                    article_id += 1

                # 避免请求过快
                time.sleep(1)

        except Exception as e:
            print(f"Error processing page {page_url}: {str(e)}")
            continue

    return documents


def save_to_json(data, filename):
    """
    将数据保存为JSON文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    base_url = "http://health.people.com.cn/GB/408572/index.html"
    max_pages = 6  # 爬取的页数，可以根据实际情况调整

    print("Starting crawling...")
    documents = crawl_health_articles(base_url, max_pages)

    print(f"\nTotal articles crawled: {len(documents)}")
    save_to_json(documents, "people_health_articles.json")
    print("Data saved to people_health_articles.json")