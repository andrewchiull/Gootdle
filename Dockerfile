# [python - Official Image | Docker Hub](https://hub.docker.com/_/python/)
# [打造最小 Python Docker 容器 - 小惡魔 - AppleBOY](https://blog.wu-boy.com/2021/07/building-minimal-docker-containers-for-python-applications/)

# Use slim instead of alpine to avoid some opencv installation problems 
FROM python:3.9.2-slim as base
FROM base as builder

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt

RUN export PIP_DEFAULT_TIMEOUT=100
RUN pip install --user -r /requirements.txt

# [docker环境里安装opencv ImportError: libGL.so.1: cannot open shared object file: No such file or directory\_docker qt libgl.so.1\_Max\_ZhangJF的博客-CSDN博客](https://blog.csdn.net/Max_ZhangJF/article/details/108920050)
RUN pip install --user opencv-python-headless==4.5.5.64

FROM base
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local

COPY cv .

CMD [ "python3", "./cv/camera.py" ]
