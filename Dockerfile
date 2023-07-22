# [python - Official Image | Docker Hub](https://hub.docker.com/_/python/)
FROM python:3.9.2


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# [docker环境里安装opencv ImportError: libGL.so.1: cannot open shared object file: No such file or directory\_docker qt libgl.so.1\_Max\_ZhangJF的博客-CSDN博客](https://blog.csdn.net/Max_ZhangJF/article/details/108920050)
RUN pip install opencv-python-headless==4.5.5.64

COPY . .

CMD [ "python3", "./cv/camera.py" ]
