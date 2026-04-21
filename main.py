from queue import Queue
from threading import Thread
from oak_deepseek.engine import AgentEngine

from prompt import main_prompt, test_prompt, env_prompt
from tools import exec_command, exec_download_command, exec_long_time_command

engine = AgentEngine()

input_queue = Queue()
history_queue = Queue()

engine.create_agent(key=("system", "main"),
                    description="一名开发者",
                    prompt=main_prompt,
                    tools=[exec_command],
                    sub_agents=[("system", "test"), ("system", "env")]
                    )

engine.create_agent(key=("system", "test"),
                    description="""测试人员，负责编写单元测试文件""",
                    prompt=test_prompt,
                    tools=[exec_command],
                    sub_agents=[])

engine.create_agent(key=("system", "env"),
                    description="""运维助手，负责环境管理，可以检查依赖或下载软件包""",
                    prompt=env_prompt,
                    tools=[exec_command, exec_download_command, exec_long_time_command],
                    sub_agents=[])

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