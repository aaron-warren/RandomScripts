import re
import psutil
from pywinauto.application import Application
import pywinauto.keyboard
import warnings

PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"

class PID:
    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid()

    def find_pid(self) -> int:
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    pid = int(query.group(1))
            except psutil.AccessDenied:
                pass
        return pid

    def connect_to_pid(self):
        if not self.pid:
            return f"ERROR: Could not find process name: {PROCESS_TARGET}"
        app = Application().connect(process=self.pid)
        return app

    def press_key(self, key: str):
        # with warnings.catch_warnings():
        #     warnings.simplefilter('ignore')

        warnings.filterwarnings("ignore", category=UserWarning)
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)