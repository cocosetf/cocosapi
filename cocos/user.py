from enum import Enum


def implication(condition, result):
    return (not condition) or result


class User:
    class Status(Enum):
        NOT_LOGGED_IN = 0
        NOT_READY = 1
        READY = 2
        WAITING_RESULTS = 3
        DONE = 4
        RESULTS_COLLECTED = 5

    def __init__(self, username, provides_code, provides_data, uses_results, is_supervisor):
        self.username = username
        self.provides_code = bool(int(provides_code))
        self.code_submitted = False
        self.provides_data = bool(int(provides_data))
        self.data_submitted = False
        self.uses_results = bool(int(uses_results))
        self.result_key_submitted = False
        self.is_supervisor = bool(int(is_supervisor))
        self.started_computation = False
        self.current_status = User.Status.NOT_LOGGED_IN

    def set_data_submitted(self):
        self.data_submitted = True
        self.update_status()

    def set_code_submitted(self):
        self.code_submitted = True
        self.update_status()

    def set_result_key_submitted(self):
        self.result_key_submitted = True
        self.update_status()

    def set_started_computation(self):
        self.started_computation = True

    def check_ready(self):
        return implication(self.provides_code, self.code_submitted) \
               and implication(self.provides_data, self.data_submitted) \
               and implication(self.uses_results, self.result_key_submitted)
        # and implication(self.is_supervisor, self.started_computation) - Supervizor je uvek Ready i ceka ostale

    def check_uses_results(self):
        return self.uses_results

    def update_status(self):
        if self.current_status == User.Status.NOT_LOGGED_IN and self.check_ready():
            self.current_status = User.Status.READY
        elif self.current_status == User.Status.NOT_LOGGED_IN:
            self.current_status = User.Status.NOT_READY
        elif self.current_status == User.Status.NOT_READY and self.check_ready():
            self.current_status = User.Status.READY
        elif self.current_status == User.Status.READY:
            self.current_status = User.Status.WAITING_RESULTS if self.check_uses_results() else User.Status.DONE
        elif self.current_status == User.Status.WAITING_RESULTS:
            self.current_status = User.Status.DONE

    def not_logged_in(self):
        return self.current_status == User.Status.NOT_LOGGED_IN

    def not_ready(self):
        return self.current_status == User.Status.NOT_READY

    def ready(self):
        return self.current_status == User.Status.READY

    def collected_results(self):
        return self.current_status == User.Status.RESULTS_COLLECTED

    def get_status(self):
        return self.current_status
