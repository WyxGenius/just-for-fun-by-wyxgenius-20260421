import json
import subprocess
import time
import random
from ddgs import DDGS


def exec_command(cmd: str) -> str:
    """
    打开命令行并执行一条bash命令，可以用来进行系统信息获取，文件阅读与修改等操作。
    执行完后，命令行会关闭。

    - 耗时任务（如下载）请使用`nohup`

    :param cmd: bash命令
    :return: 执行结果
    """
    try:
        result = subprocess.run(
            ["docker", "exec", "-i", "debian-sandbox", "/bin/sh", "-c", cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        return result.stdout + result.stderr
    except Exception as e:
        return e.__str__()

def exec_download_command(cmd: str) -> str:
    """
    打开命令行并执行一条bash命令，有更长的时间限制，可以用来下载软件包。
    执行完后，命令行会关闭。

    - `cd` 命令不可用

    :param cmd: bash命令
    :return: 执行结果
    """
    try:
        result = subprocess.run(
            ["docker", "exec", "-i", "debian-sandbox", "/bin/sh", "-c", cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300
        )
        return result.stdout + result.stderr
    except Exception as e:
        return e.__str__()

def exec_long_time_command(cmd: str) -> str:
    """
    打开命令行并执行一条bash命令，有极长的时间限制，可以用来下载大型文件。
    执行完后，命令行会关闭。

    - `cd` 命令不可用
    - 使用此工具时尽可能在后台执行任务

    :param cmd: bash命令
    :return: 执行结果
    """
    try:
        result = subprocess.run(
            ["docker", "exec", "-i", "debian-sandbox", "/bin/sh", "-c", cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=1800
        )
        return result.stdout + result.stderr
    except Exception as e:
        return e.__str__()


def web_search(key_words: str) -> str:
    """
    搜索引擎，使用关键词获取一页搜索结果

    :param key_words: 搜索关键词
    :return:
    """
    with DDGS() as ddgs:
        results = ddgs.text(key_words)

    time.sleep(random.uniform(2, 3))

    if not results:
        return f"抱歉，没有找到与“{key_words}”相关的结果"

    output_lines = [f"搜索关键词：{key_words}\n"]
    for i, r in enumerate(results, 1):
        output_lines.append(f"{i}. {r['title']}")
        output_lines.append(f"   链接：{r['href']}")
        output_lines.append(f"   摘要：{r['body']}")
        output_lines.append("")

    return "\n".join(output_lines)