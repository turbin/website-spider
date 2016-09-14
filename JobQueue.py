#coding=utf-8


from Queue import Queue
from threading import Thread
from Log import Logger
import os

log=Logger(__name__)


class JobHandler(object):
    def run_job(self):
        raise NotImplementedError
        pass



def _do_job(q):
    assert q and isinstance(q,Queue),log.fatal('queue is invalid!')
    handler = q.get()

    assert handler and isinstance(handler,JobHandler),log.fatal('queue is invalid!')
    log.info('job run !')
    try:
        handler.run_job()
    except KeyboardInterrupt:
        log.warn('user cancel it !')

    finally:
        q.task_done()
    pass

def _LaunchThread(run=None, args=(),daemon = False):
    t = Thread(target=run,args=args)
    t.daemon = daemon
    t.start()
    return t

class JobQ(object):

    def __init__(self, max_queue_num):
        self.max_queue_num = max_queue_num
        self.q = Queue(max_queue_num)
        self.jobs = []

    def addJob(self, job_handler=None):
        log.info("add jobs! jobobject %s" % repr(job_handler))
        assert job_handler,log.fatal('job handler is invalid!')
        #self.q.put(job_handler)
        self.jobs.append(job_handler)

    def wait_for_done(self):
        log.info("wait_for_done")
        self.q.join()


    def startAll(self):
        log.info('start all !')
        for job in self.jobs:
            self.q.put(job)
            _LaunchThread(run=_do_job, args=(self.q,), daemon=True)
