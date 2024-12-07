import ctypes
import random
import subprocess
import sys
import uuid
from enum import Enum
from pathlib import Path
import platform


class P(Enum):
    win = 'Windows'
    linux = 'Linux'


try:
    p = P(platform.system())
except ValueError:
    print('未知平台')
    sys.exit(0)


class JB重置试用:
    def __init__(self):
        ok, msg = self.delete_file(self.will_del_file())
        if not ok:
            self.show_message(False, msg)
            return

        ok, msg = self.change_registry()
        if not ok:
            self.show_message(False, msg)
            return

        self.show_message(True, '重置试用成功')

    def show_message(self, ok: bool, message: str):
        title = ('失败', '成功')[ok]
        match p:
            case P.win:
                ctypes.windll.user32.MessageBoxW(0, message, title, 0)
            case P.linux:
                subprocess.run(['zenity', '--info', '--title', title, '--text', message])
            case _:
                ...

    def will_del_file(self):
        home_dir = Path.home()

        will_del_file: list[Path]
        match p:
            case P.win:
                will_del_file = [
                    home_dir / "AppData/Roaming/JetBrains/PermanentDeviceId",
                    home_dir / "AppData/Roaming/JetBrains/PermanentUserId"
                ]
            case P.linux:
                will_del_file = [
                    home_dir / ".java/.userPrefs/prefs.xml",
                    home_dir / ".java/.userPrefs/jetbrains/prefs.xml"
                ]
            case _:
                will_del_file = []

        return will_del_file

    def delete_file(self, will_del_file: list[Path]):
        try:
            for file in will_del_file:
                file.unlink(missing_ok=True)

            return True, None

        except Exception as e:
            return False, f"删除文件失败: {e}"

    def change_registry(self):
        if p == P.linux:
            return True, None

        import winreg

        try:
            # 生成随机ID
            device_id = f"{random.randint(0, int(1e7) - 1):07d}" + str(uuid.uuid4())
            user_id_on_machine = str(uuid.uuid4())

            # 注册表路径
            registry_path = r"Software\JavaSoft\Prefs\jetbrains"

            # 打开或创建注册表键
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
                winreg.SetValueEx(key, "device_id", 0, winreg.REG_SZ, device_id)
                winreg.SetValueEx(key, "user_id_on_machine", 0, winreg.REG_SZ, user_id_on_machine)

            return True, None

        except Exception as e:
            return False, f"修改注册表失败: {e}"


if __name__ == "__main__":
    JB重置试用()
