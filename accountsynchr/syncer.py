from abc import ABCMeta, abstractmethod
from accountsynchr.dao.trumba import CalPermManager
from accountsynchr.ucalgroup.group_manager import GroupManager


class Syncer:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.cal_per_m = CalPermManager()
        self.gro_m = GroupManager()
        self.errors = []

    def append_error(self, message):
        self.errors.append(message)

    def get_error_report(self):
        return ',\n'.join(self.errors)

    def has_err(self):
        return len(self.errors) > 0

    @abstractmethod
    def sync(self):
        """
        Action
        """
