import cv2
import color

class Camera:
    def run(self):

        # Ref: [Python-OpenCV — 讀取顯示及儲存影像、影片 | by 李謦伊 | 謦伊的閱讀筆記 | Medium](https://medium.com/ching-i/python-opencv-%E8%AE%80%E5%8F%96%E9%A1%AF%E7%A4%BA%E5%8F%8A%E5%84%B2%E5%AD%98%E5%BD%B1%E5%83%8F-%E5%BD%B1%E7%89%87-ee3701c454da)

        # current camera
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            # ESC
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        
        cd = color.ColorDetection(img=frame, detect=40, resize=50)
        cd.main()



def main():
    camera = Camera()
    camera.run()


if __name__ == "__main__":
    main()