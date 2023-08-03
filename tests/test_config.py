import yaml
from settings import S

config = yaml.safe_load(open(S.ROOT/"config.yml"))
print(config["videopath"]) # ./cv/test_input_video/white_tshirt.MOV