from queue import Queue
from threading import Thread
from oak_deepseek.engine import AgentEngine

from crawl import crawl, read_pages
from prompt import main_prompt, test_prompt, env_prompt, search_prompt
from tools import exec_command, exec_download_command, exec_long_time_command, web_search

engine = AgentEngine()

input_queue = Queue()
history_queue = Queue()

engine.create_agent(key=("system", "main"),
                    description="一名开发者",
                    prompt=main_prompt,
                    tools=[exec_command, exec_download_command, exec_long_time_command],
                    sub_agents=[("system", "search")])

engine.create_agent(key=("system", "search"),
                    description="""可以帮你查资料的助手，有疑问都可以问""",
                    prompt=search_prompt,
                    tools=[web_search, crawl, read_pages],
                    sub_agents=[],
                    rm_rf_memory=True)

def run():
    engine.run(history_queue=history_queue, input_queue=input_queue, key=("system", "main"))

def get_input():
    while True:
        cmd = input()
        if cmd:
            if cmd == "exit":
                return
            input_queue.put(cmd)

def print_line():
    while True:
        msg = history_queue.get(block=True)
        if not msg:
            return
        print(msg)


if __name__ == "__main__":
    run_thread = Thread(target=run, daemon=True)
    input_thread = Thread(target=get_input)
    print_thread = Thread(target=print_line)

    run_thread.start()
    input_thread.start()
    print_thread.start()

    input_thread.join()
    history_queue.put(None)
    print_thread.join()