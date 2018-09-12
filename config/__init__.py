
import os
import logging

LOCAL_FS_STORAGE = "local_fs"
MONGO_DB_STORAGE = "mongodb"

"""
The config module provides default set of settings that will be used in the app
it includes settings sucn as:
- the storage backend and configuration related to each type
- the port where the app will be running
"""
CONFIG = {
    # Storage Backend DB can be one of:
    # local_fs
    # mongodb
    "storage_backend": os.getenv("RETAIL_STORAGE_BACKEND", LOCAL_FS_STORAGE),
    "local_fs_base_path": os.getenv("RETAIL_LOCAL_STORAGE_BASE_PATH",
                                    "/tmp/retail"),
    "api_port": os.getenv("RETAIL_API_PORT", 5000),
    "api_log_level": logging._nameToLevel[os.getenv("RETAIL_API_PORT", "INFO")]
}
