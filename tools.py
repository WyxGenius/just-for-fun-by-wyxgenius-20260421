import subprocess


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