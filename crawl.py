from typing import Iterator, List
import requests


def make_pages_iterator(content: str) -> Iterator[str]:
    content: List[str] = content.split("\n\n")

    page: str = ""
    for part in content:
        if len(page) < 20000 and ((len(page) + len(part)) < 30000):
            page += f"\n\n{part}"
        else:
            yield page
            page = part

    page += "[Reading Finished]"
    yield page

pages: Iterator[str]

def crawl(target_url: str) -> str:
    """
    这个工具用于访问指定网址。
    如果访问成功了，你就可以使用 `read_pages` 工具一页一页地阅读网页了。

    :param target_url: 指定网址
    :return: 访问状态
    """
    url = "http://localhost:8082/crawl"
    payload = {
        "url": target_url
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        #print("*****" + response.text + "*****")
        if response.text:
            page = response.text
            global pages
            pages = make_pages_iterator(page)
            return "已拉取网页内容"
        else:
            return "当前工具不支持对此网站的访问"
    else:
        return response.text

def read_pages() -> str:
    """
    网页阅读器，由于网页太长，我进行了分页，每次调用都会返回新的一页的内容。
    如果内容以 `[Reading Finished]` 结尾，则已浏览完当前网页所有内容。
    如果内容类似“数据加载中”请直接放弃，这意味着访问失败。

    :return:
    """
    global pages
    return next(pages, "[Reading Finished]")