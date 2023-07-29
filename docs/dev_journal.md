# Dev Journal

- Authors
    - marshall
    - 黃沛婕
    - yushan
    - Max
    - Andrew

# Python

## Coding Style

### How to name a module?
```bash
# 2023-07-21 06:15:20
# [Structuring Your Project — The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
```

# [python - Importing modules from parent folder - Stack Overflow](https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder)

```python
# setup.py
from setuptools import setup, find_packages

setup(name='myproject', version='1.0', packages=find_packages())
```

```bash
pip install -e .
```

# Raspberry Pi


## ssh RPi 的 hostname 沒有用

要寫成 hostname.local

## 不知道 RPi 的 IP，沒辦法 ssh

```bash
# 2023-07-21 19:42:24
# nmap 可以掃同網域內其他 ip
# [祕密基地: Mac 安裝 Nmap](http://secretbase2000.blogspot.com/2019/11/mac-nmap.html)
brew install nmap

# 給一個 ip 範圍
nmap -sP "192.168.1.101-110"
# 或是全掃（會比較慢）
nmap -sP "192.168.1.*"
```


## 沒有網路的情況下連接 RPi (Mac)

[Connect to your Raspberry Pi from a Mac](https://www.dexterindustries.com/BrickPi/brickpi-tutorials-documentation/getting-started/using-the-pi/connect-to-your-raspberry-pi-from-a-mac/)

## 分享網路給 RPi (Mac)

[Direct ethernet connection | The Raspberry Pi Guide](https://raspberrypi-guide.github.io/networking/create-direct-ethernet-connection)


## 把 RPi 的 HDMI 訊號用 USB 輸入到電腦（反之亦然）

可以把電腦的螢幕畫面當成 Webcam 訊號給 RPi。

[VC01 USB3.0轉HDMI影像擷取卡 - PChome 24h購物](https://24h.pchome.com.tw/prod/DCAX3W-A900EQPPF-000)
[BENEVO 4K版 50cm HDMI2.0影音連接線(滿芯) - PChome 24h購物](https://24h.pchome.com.tw/prod/DCACXR-A900G6OTS-000)

## Sync with .gitignore

[explainshell.com - rsync -avhr \~/Google-HPS-2023-Team8 andrew@andrewrpi.local:\~ --include='\*\*.gitignore' --exclude='/.git' --filter=':- .gitignore' --delete-after](https://explainshell.com/explain?cmd=rsync+-avhr+%7E%2FGoogle-HPS-2023-Team8+andrew%40andrewrpi.local%3A%7E+--include%3D%27**.gitignore%27+--exclude%3D%27%2F.git%27+--filter%3D%27%3A-+.gitignore%27+--delete-after)

[git - rsync exclude according to .gitignore & .hgignore & svn:ignore like --filter=:C - Stack Overflow](https://stackoverflow.com/questions/13713101/rsync-exclude-according-to-gitignore-hgignore-svnignore-like-filter-c)

# Opencv

## Installation

```bash
# 需要先安裝一些 opencv 相關支援套件。
sudo apt-get install –y libhdf5-dev
sudo apt-get install –y libatlas-base-dev
sudo apt-get install –y libjasper-dev

pip install numpy==1.22.3
pip install opencv-python==4.5.5.64

# Optional
pip install matplotlib==3.3.4
```


## Opencv Tutorial

[Python-OpenCV — 讀取顯示及儲存影像、影片 | by 李謦伊 | 謦伊的閱讀筆記 | Medium](https://medium.com/ching-i/python-opencv-%E8%AE%80%E5%8F%96%E9%A1%AF%E7%A4%BA%E5%8F%8A%E5%84%B2%E5%AD%98%E5%BD%B1%E5%83%8F-%E5%BD%B1%E7%89%87-ee3701c454da)

## Add to PATH Permanently

```bash
# Open the .zshrc file using a text editor.
nano ~/.zshrc

# Go to the end of the file.
# Paste the export syntax at the end of the file. 
# export PATH="/Directory1:$PATH"
```

# Git/GitHub

## Tutorial

[連猴子都能懂的Git入門指南 | 貝格樂（Backlog）](https://backlog.com/git-tutorial/tw/)


# Docker

## Dev in docker

[(10) How to create a great dev environment with Docker - YouTube](https://www.youtube.com/watch?v=0H2miBK_gAk&ab_channel=PatrickLoeber)

## Installation
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## If permission denied
[How to fix docker: Got permission denied issue - Stack Overflow](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue)
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

## Dockerfile

[打造最小 Python Docker 容器 - 小惡魔 - AppleBOY](https://blog.wu-boy.com/2021/07/building-minimal-docker-containers-for-python-applications/)


[docker环境里安装opencv ImportError: libGL.so.1: cannot open shared object file: No such file or directory\_docker qt libgl.so.1\_Max\_ZhangJF的博客-CSDN博客](https://blog.csdn.net/Max_ZhangJF/article/details/108920050)


## opencv-python Installation

[francoisgervais/opencv-python - Docker Image | Docker Hub](https://hub.docker.com/r/francoisgervais/opencv-python/)

## Build and Run

```bash
docker build -t my-python-app .
docker run -it --rm --name my-running-app my-python-app
```

## docker-compose

```bash
# Installation on RPi
sudo curl -SL https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod 777 -R /usr/local/bin/docker-compose
sudo pip install docker-compose
```

```bash
# build
docker-compose up -d --build
docker ps
docker exec -it python-server sh -c "echo Hi"
docker exec -it python-server sh -c "python3 test_docker_volume.py"
```