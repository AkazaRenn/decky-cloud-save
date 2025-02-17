import decky

import signal
from typing import Any

from rclone_manager import RcloneManager
from sync_target import *
from config import Config
import utils


class Plugin:

    # rclone.conf Setup

    async def spawn(self, backend_type: str) -> str:
        utils.logger.debug(f"Executing spawn(backend_type={backend_type})")
        return RcloneManager.spawn(backend_type)

    async def spawn_probe(self) -> int:
        utils.logger.debug(f"Executing probe()")
        return RcloneManager.probe()

    async def get_backend_type(self) -> str:
        utils.logger.debug(f"Executing get_backend_type()")
        return RcloneManager.get_backend_type()

    # Sync Paths

    async def get_syncpaths_include(self, app_id: int = 0) -> list[str]:
        utils.logger.debug(f"Executing get_syncpaths_include(app_id={app_id})")
        return get_sync_target(app_id).get_syncpaths(SyncPathType.INCLUDE)

    async def get_syncpaths_exclude(self, app_id: int = 0) -> list[str]:
        utils.logger.debug(f"Executing get_syncpaths_exclude(app_id={app_id})")
        return get_sync_target(app_id).get_syncpaths(SyncPathType.EXCLUDE)

    async def add_syncpath_include(self, path: str, app_id: int = 0) -> None:
        utils.logger.debug(f"Executing add_syncpath_include(path={path}, app_id={app_id})")
        return get_sync_target(app_id).add_syncpath(SyncPathType.INCLUDE)

    async def add_syncpath_exclude(self, path: str, app_id: int = 0) -> None:
        utils.logger.debug(f"Executing add_syncpath_exclude(path={path}, app_id={app_id})")
        return get_sync_target(app_id).add_syncpath(SyncPathType.EXCLUDE)

    async def remove_syncpath_include(self, path: str, app_id: int = 0) -> None:
        utils.logger.debug(f"Executing remove_syncpath_include(path={path}, app_id={app_id})")
        return get_sync_target(app_id).remove_syncpath(SyncPathType.INCLUDE)

    async def remove_syncpath_exclude(self, path: str, app_id: int = 0) -> None:
        utils.logger.debug(f"Executing remove_syncpath_exclude(path={path}, app_id={app_id})")
        return get_sync_target(app_id).remove_syncpath(SyncPathType.EXCLUDE)

    async def test_syncpath(self, path: str) -> int:
        utils.logger.debug(f"Executing test_syncpath({path})")
        return utils.test_syncpath(path)

    # Syncing

    async def sync_local_first(self, app_id: int = 0) -> int:
        utils.logger.debug(f"Executing sync_local_first(app_id={app_id})")
        return await self._sync(RcloneSyncWinner.LOCAL, app_id)

    async def sync_cloud_first(self, app_id: int = 0) -> int:
        utils.logger.debug(f"Executing sync_cloud_first(app_id={app_id})")
        return await self._sync(RcloneSyncWinner.CLOUD, app_id)

    async def resync_local_first(self, app_id: int = 0) -> int:
        utils.logger.debug(f"Executing resync_local_first(app_id={app_id})")
        return await self._resync(RcloneSyncWinner.LOCAL, app_id)

    async def resync_cloud_first(self, app_id: int = 0) -> int:
        utils.logger.debug(f"Executing resync_cloud_first(app_id={app_id})")
        return await self._resync(RcloneSyncWinner.CLOUD, app_id)

    async def sync_screenshot(self, screenshot_path: str) -> int:
        utils.logger.debug(f"Executing sync_screenshot()")
        return await ScreenshotSyncTarget(screenshot_path).sync()

    async def delete_lock_files(self):
        utils.logger.debug(f"Executing delete_lock_files()")
        return utils.delete_lock_files()

    async def _sync(self, winner: RcloneSyncWinner, app_id: int = 0) -> int:
        return await get_sync_target(app_id).sync(winner)

    async def _resync(self, winner: RcloneSyncWinner, app_id: int = 0) -> int:
        return await get_sync_target(app_id).resync(winner)

    # Processes

    async def pause_process(self, pid: int) -> None:
        utils.logger.debug(f"Executing pause_process(pid={pid})")
        utils.send_signal(pid, signal.SIGSTOP)

    async def resume_process(self, pid: int) -> None:
        utils.logger.debug(f"Executing resume_process(pid={pid})")
        utils.send_signal(pid, signal.SIGCONT)

    # Configuration

    async def get_config(self):
        utils.logger.debug(f"Executing get_config()")
        return Config.get_config()

    async def set_config(self, key: str, value: Any):
        utils.logger.debug(f"Executing set_config(key={key}, value={value})")
        Config.set_config(key, value)

    async def mkdir_dest_dir(self):
        utils.logger.debug(f"Executing cloud_mkdir()")
        utils.mkdir_dest_dir()

    # Logger

    async def log_debug(self, msg: str) -> None:
        utils.logger.debug(msg)

    async def log_info(self, msg: str) -> None:
        utils.logger.info(msg)

    async def log_warning(self, msg: str) -> None:
        utils.logger.warning(msg)

    async def log_error(self, msg: str) -> None:
        utils.logger.error(msg)

    async def get_last_sync_log(self) -> str:
        utils.logger.debug(f"Executing get_last_sync_log()")
        # return logger_utils.get_last_sync_log()
        return "unimplemented"

    async def get_plugin_log(self) -> str:
        utils.logger.debug(f"Executing get_plugin_log()")
        return utils.get_plugin_log()

    # Lifecycle

    async def _main(self):
        logger_level = Config.get_config_item("log_level")
        utils.logger.setLevel(logger_level)

        utils.logger.debug(f"rclone exe path: {RCLONE_BIN_PATH}")
        utils.logger.debug(f"rclone cfg path: {RCLONE_CFG_PATH}")

    async def _unload(self):
        RcloneManager.cleanup()

    async def _migration(self):
        # plugin_config.migrate()
        pass
