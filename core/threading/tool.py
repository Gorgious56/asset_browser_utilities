import threading


from asset_browser_utilities.core.log.logger import Logger


class ThreadManager:
    threads: list[threading.Thread]
    threads_progress: list[float]

    @staticmethod
    def init(execute_function, thread_count, callback=None):
        ThreadManager.execute_function = execute_function
        ThreadManager.thread_count = thread_count
        ThreadManager.threads = [
            threading.Thread(name="Thread %d" % i, target=ThreadManager.execute_function_wrapper)
            for i in range(ThreadManager.thread_count)
        ]
        ThreadManager.callback = callback

    @staticmethod
    def run(wait_for_execution=True):
        for thread in ThreadManager.threads:
            thread.start()
        if wait_for_execution:
            for thread in ThreadManager.threads:
                thread.join()
            Logger.display("All threads are closed !")

    @staticmethod
    def execute_function_wrapper():
        ThreadManager.execute_function(index=ThreadManager.threads.index(threading.current_thread()))
        ThreadManager.callback()
