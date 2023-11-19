import threading

from asset_browser_utilities.core.log.logger import Logger


class ThreadManager:
    def __init__(self, execute_function, thread_count):
        self.execute_function = execute_function
        self.thread_count = thread_count
        self.threads = [
            threading.Thread(name="Thread %d" % i, target=self.execute_function_wrapper)
            for i in range(self.thread_count)
        ]

    def run_and_wait_for_execution(self):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        Logger.display("All threads are closed !")

    def execute_function_wrapper(self):
        # Logger.display(f"{threading.current_thread().name} Starting")
        self.execute_function()
        Logger.display(f"{threading.current_thread().name} Exiting")
