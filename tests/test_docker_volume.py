import time
from settings import S
import attrs
from pprint import pprint

print("test_docker_volume.py begins...")

# s = 
pprint(attrs.asdict(S))

i = 0
while True:
    i += 1
    print(f"test_docker_volume.py {i}")
    time.sleep(1)