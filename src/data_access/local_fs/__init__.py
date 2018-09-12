from config import CONFIG


class BaseLocalFsDal(object):

    def __init__(self):
        self.base_path = CONFIG["local_fs_base_path"]
