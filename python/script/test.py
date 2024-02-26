import os
from pathlib import Path

print(os.listdir(Path(__file__).parent))

print(sorted(['001', '1235', '66', '789'], key=lambda x: int(x)))
