from enum import Enum


class Computation:

    comp = None

    class Status(Enum):
        NOT_STARTED = 0
        RUNNING = 1
        DONE = 2
        RESULTS_COLLECTED = 3

    def __init__(self):
        self.status = Computation.Status.NOT_STARTED

    @staticmethod
    def get_computation():
        if Computation.comp is None:
            comp = Computation()
        return comp

    def update_status(self):
        if self.status == Computation.Status.NOT_STARTED:
            self.status = Computation.Status.RUNNING
        elif self.status == Computation.Status.RUNNING:
            self.status = Computation.Status.DONE
        elif self.status == Computation.Status.DONE:
            self.status = Computation.Status.RESULTS_COLLECTED

    def get_status(self):
        return self.status

    def not_started(self):
        return self.status == Computation.Status.NOT_STARTED

    def running(self):
        return self.status == Computation.Status.RUNNING

    def done(self):
        return self.status == Computation.Status.DONE

