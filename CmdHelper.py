import subprocess as cmd
from pathlib import Path


class AdbCommandHelper:
    selected_device = ""

    # Set the selected device
    def set_selected_device(self, device):
        self.selected_device = device

    def _run_adb(self, command):
        if not self.list_devices():
            return ["There's no devices connected"]

        device = ""
        if self.selected_device:
            device = f" -s {self.selected_device}"
        command = f"adb{device} {command}"
        print("RUN: " + command)
        result = cmd.check_output(command).splitlines()
        return [line.decode('utf-8') for line in result if line and len(line) > 0]

    # Return a Pair with Device ID and Device Status
    def list_devices(self):
        result = cmd.check_output("adb devices").splitlines()
        result = [line.decode('utf-8') for line in result if line and len(line) > 0]
        del result[0]
        return [tuple(device.split('\t')) for device in result]

    #
    def list_available_db(self):
        result = self._run_adb("shell ls /data/system")
        return [db for db in result if db.endswith(".db")]

    def pull_db(self, db: str):
        output_path = (Path.cwd() / "temp").resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        self._run_adb(f"pull /data/system/{db} \"{output_path}\"")
        return (output_path / db).resolve()
