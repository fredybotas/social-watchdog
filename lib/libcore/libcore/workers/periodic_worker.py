import schedule
import time


class PeriodicWorkerBase:
    def __init__(self, every: int) -> None:
        self.scheduler = schedule.Scheduler()
        self.scheduler.every(every).seconds.do(self.work)

    def start(self) -> None:
        while True:
            self.scheduler.run_pending()
            time.sleep(1)

    def work(self):
        raise NotImplementedError()
