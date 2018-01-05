import threading

class Timer(threading.Thread):
    def __init__(self, time, func):
        threading.Thread.__init__(self, target=self.__exec, daemon=True)
        self.__time = time
        self.__func = func
        self.__stop_evt = threading.Event()
    def stop(self):
        self.__stop_evt.set()
    def __exec(self):
        while not self.__stop_evt.wait(self.__time):
            self.__func()