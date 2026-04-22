import time
import random  # 👈 新增随机模块喵~
from ddgs import DDGS

with DDGS() as ddgs:
    results = ddgs.text("Python 多线程")
    print(results)

    for r in results:
        print(f"标题：{r['title']}")
        print(f"链接：{r['href']}")
        print(f"描述：{r['body']}")
        print("-" * 30)

        # 每次请求后随机等待 2~3 秒
        delay = random.uniform(2, 3)
        time.sleep(delay)