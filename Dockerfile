FROM francoisgervais/opencv-python
COPY ./cv/ ./cv/

# Show info
RUN pip list
RUN python3 -V
RUN python -c 'import cv2; print(cv2.__path__) ;print(cv2.__version__)'

CMD [ "python3", "./cv/camera.py" ]
