
import os

LOCAL_FS_STORAGE = "local_fs"

CONFIG = {
    "storage_backend": os.getenv("RETAIL_STORAGE_BACKEND", LOCAL_FS_STORAGE),
    "local_fs_base_path": os.getenv("RETAIL_LOCAL_STORAGE_BASE_PATH",
                                    "/tmp/retail")
}