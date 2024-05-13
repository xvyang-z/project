import os
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = ROOT_DIR / 'gui/ui'


MODEL_PATH = r'D:\tmp\yolov8\runs\detect\train4\weights\best.pt'
GAME_HANDLE_NAME = '守望先锋'
# GAME_HANDLE_NAME = '录制_2024_05_13_11_49_44_276.mp4 - PotPlayer'  # fixme for test
