FROM francoisgervais/opencv-python
COPY ./cv/ ./cv/
CMD [ "python3", "./cv/camera.py" ]
