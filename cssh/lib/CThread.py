import Queue
import threading
class CThread(threading.Thread):
    def __init__(self, queue,call):
        threading.Thread.__init__(self)
        self.job = queue
        self.threadCall=call
        
    def run(self):
        while True:
            self.threadCall(self.job.get())
            self.job.task_done()

job = Queue.Queue()

def initThread(num,threadCall):
    for i in range(num):
        t = CThread(job,threadCall)
        t.setDaemon(True)
        t.start()   

def putjob(ajob):
    job.put(ajob)

def waitDone():
    job.join()



