import signal
import decky_plugin
import plugin_config
import process_utils
import logger_utils
from rclone_setup_manager import RcloneSetupManager
from rclone_sync_manager import RcloneSyncManager


class Plugin:
    manager_setup = RcloneSetupManager()
    manager_sync = RcloneSyncManager()

# rclone.conf Setup

    async def spawn(self, backend_type: str):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.spawn(%s)", backend_type)
        return await self.manager_setup.spawn(backend_type)

    async def spawn_probe(self):
        decky_plugin.logger.debug("Executing: RcloneSetupManager.probe()")
        return await self.manager_setup.probe()

    async def get_backend_type(self):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.get_backend_type()")
        return await self.manager_setup.get_backend_type()

# Sync Paths

    async def get_syncpaths(self, file: str):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.get_syncpaths(%s)", file)
        return await self.manager_setup.get_syncpaths(file)

    async def test_syncpath(self, path: str):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.test_syncpath(%s)", path)
        return await self.manager_setup.test_syncpath(path)

    async def add_syncpath(self, path: str, file: str):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.add_syncpath(%s, %s)", path, file)
        return await self.manager_setup.add_syncpath(path, file)

    async def remove_syncpath(self, path: str, file: str):
        decky_plugin.logger.debug(
            "Executing: RcloneSetupManager.remove_syncpath(%s, %s)", path, file)
        return await self.manager_setup.remove_syncpath(path, file)

# Syncing

    async def sync_now_internal(self, winner: str, resync: bool):
        decky_plugin.logger.info(
            "Executing: RcloneSyncManager.sync_now(%s, %b)", winner, resync)
        return await self.manager_sync.sync_now(winner, resync)

    async def sync_now_probe(self):
        decky_plugin.logger.debug("Executing: RcloneSyncManager.probe()")
        return await self.manager_sync.probe()

    async def delete_lock_files(self):
        decky_plugin.logger.debug(
            "Executing: RcloneSyncManager.delete_lock_files()")
        return await self.manager_sync.delete_lock_files()

# Processes

    async def signal(self, pid: int, s: str):
        decky_plugin.logger.debug("Executing: send_signal(%s)", pid, s)
        if s == "SIGSTOP":
            return process_utils.send_signal(pid, signal.SIGSTOP)
        elif s == "SIGCONT":
            return process_utils.send_signal(pid, signal.SIGCONT)

# Configuration

    async def get_log_level(self):
        decky_plugin.logger.debug("Executing: get_log_level()")
        return decky_plugin.logger.level

    async def get_config(self):
        decky_plugin.logger.debug("Executing: get_config()")
        return plugin_config.get_config()

    async def set_config(self, key: str, value: str):
        decky_plugin.logger.debug("Executing: set_config(%s, %s)", key, value)
        plugin_config.set_config(key, value)

# Logger

    async def log(self, level: str, msg: str) -> int:
        decky_plugin.logger.debug("Executing: log()")
        return logger_utils.log(level, msg)

    async def get_last_sync_log(self) -> str:
        decky_plugin.logger.debug("Executing: get_last_sync_log()")
        return logger_utils.get_last_sync_log()

    async def get_plugin_log(self) -> str:
        decky_plugin.logger.debug("Executing: get_plugin_log()")
        return logger_utils.get_plugin_log()

# Lifecycle

    async def _main(self):
        logger_level = plugin_config.get_config_item("log_level", "INFO")
        decky_plugin.logger.setLevel(logger_level)

        decky_plugin.logger.debug(
            "rclone exe path: %s", plugin_config.rclone_bin)
        decky_plugin.logger.debug(
            "rclone cfg path: %s", plugin_config.rclone_cfg)

    async def _unload(self):
        self.manager_setup.cleanup()

    async def _migration(self):
        plugin_config.migrate()
