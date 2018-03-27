from .db.db_manager_abc import DbManagerABC
from .queue_manager import QueueManager
from .filters import filter_by_dict


class MainController(object):
    def __init__(self, queue_manager: QueueManager, db_manager: DbManagerABC):
        self._queue_manager = queue_manager
        self._db_manager = db_manager
        self._queue_manager.bind_to(self.run_filter)
        self._vulgarisms = set(i[0] for i in self._db_manager.select_from_table('banned_words', ('word', )))

    def run_filter(self):
        while not self._queue_manager.is_queue_empty():
            post_id = self._queue_manager.get_from_queue()
            post_content, post_flag = self._db_manager.select_from_table('tweets', ('tweet', 'flag'),
                                                                         'id_twt=' + str(post_id), True)[0]
            print(str(post_id) + ": " + post_content + " " + str(post_flag))
            print(filter_by_dict(self._vulgarisms, post_content))
            if filter_by_dict(self._vulgarisms, post_content):
                self._db_manager.update_columns('tweets', {'flag': '3'}, 'id_twt=' + str(post_id), True)
            # if vulgarism detected update flag column with 3
            # else run nn filter and update with 1 or 2
        self._db_manager.commit()
        self._db_manager.disconnect()

    def add_to_queue(self, content):
        self._queue_manager.add_to_queue(content)
