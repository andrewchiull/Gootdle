# Dev Journal
- Max test
# Python

## Coding Style

### How to name a module?
```bash
# 2023-07-21 06:15:20
# [Structuring Your Project — The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
```

# Raspberry Pi
## 不知道 RPi 的 id，沒辦法 ssh

```bash
# 2023-07-21 19:42:24
# nmap 可以掃同網域內其他 ip
# [祕密基地: Mac 安裝 Nmap](http://secretbase2000.blogspot.com/2019/11/mac-nmap.html)
brew install nmap
```


# Opencv

## Installation

```bash
# 在實際安裝opencv之前，需要先安裝一些opencv相關支援套件。
sudo apt-get install –y libhdf5-dev
sudo apt-get install –y libatlas-base-dev
sudo apt-get install –y libjasper-dev


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

## Git/GitHub

### Tutorial

[連猴子都能懂的Git入門指南 | 貝格樂（Backlog）](https://backlog.com/git-tutorial/tw/)


## Docker

### Installation
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### If permission denied
[How to fix docker: Got permission denied issue - Stack Overflow](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue)
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### Dockerfile

[打造最小 Python Docker 容器 - 小惡魔 - AppleBOY](https://blog.wu-boy.com/2021/07/building-minimal-docker-containers-for-python-applications/)


[docker环境里安装opencv ImportError: libGL.so.1: cannot open shared object file: No such file or directory\_docker qt libgl.so.1\_Max\_ZhangJF的博客-CSDN博客](https://blog.csdn.net/Max_ZhangJF/article/details/108920050)

