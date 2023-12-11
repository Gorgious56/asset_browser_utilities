import threading

from asset_browser_utilities.core.log.logger import Logger


class ThreadManager:
    THREAD_POOL: int = 25
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
        ThreadManager.threads_to_run = ThreadManager.threads[:]
        ThreadManager.running_threads = 0

        def internal_callback():
            ThreadManager.running_threads -= 1
            ThreadManager.update_threads()
            callback()

        ThreadManager.callback = internal_callback

    @staticmethod
    def update_threads():
        while ThreadManager.running_threads < ThreadManager.THREAD_POOL:
            if ThreadManager.threads_to_run:
                ThreadManager.threads_to_run.pop(0).start()
                ThreadManager.running_threads += 1
            else:
                break

    @staticmethod
    def run(wait_for_execution=True):
        ThreadManager.update_threads()
        if wait_for_execution:
            for thread in ThreadManager.threads:
                thread.join()
            Logger.display("All threads are closed !")

    @staticmethod
    def execute_function_wrapper():
        # TODO : use a queue to throttle a fixed thread pool and assign it tasks. But next line won't work anymore.
        ThreadManager.execute_function(index=ThreadManager.threads.index(threading.current_thread()))
        ThreadManager.callback()
