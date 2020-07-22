import sys
from pathlib import Path

if __name__ == "__main__":
    config = open(str(Path.home() / 'data' / 'config.json'), 'r').readlines()
    config[1] = f'    "box_id": "{sys.argv[1]}",\n'
    open(str(Path.home() / 'data' / 'config.json'), 'w').writelines(config)
    print(f"New tunnel id is: {sys.argv[1]}")


