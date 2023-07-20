import argparse
import numpy as np
import cv2


class ColorDetection():
    def __init__(self, img: np.ndarray, detect: int, resize: int, debugMode: bool =False):
        self.img = img

        self.debugMode = (debugMode == "y")
        self.CROP_PERCENTAGE = detect
        self.RESIZE_PERCENTAGE = resize

        # For HSV in OpenCV, hue range is [0,179], NOT [0,359]
        # [OpenCV: Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
        self.color2Hue = {"red":      0 / 2,
                          "yellow":  60 / 2,
                          "green":  120 / 2,
                          "blue":   180 / 2,
                          "blue":   240 / 2,
                          "purple": 300 / 2}

        width = int(self.img.shape[1] * self.RESIZE_PERCENTAGE / 100)
        height = int(self.img.shape[0] * self.RESIZE_PERCENTAGE / 100)
        dim = (width, height)

        # resize image
        self.img = cv2.resize(self.img, dim, interpolation=cv2.INTER_AREA)

        self.imgOriginal = self.img.copy()

    def enhance(self, img: np.ndarray, brightness=0, contrast=100):
        # [【OpenCV】8 - 運用 OpenCV 改變圖片的對比度 modify contrast (內含：網路上常見錯誤調整對比度方式的分析)](https://www.wongwonggoods.com/python/python_opencv/opencv-modify-contrast/)
        import math

        b = brightness / 255.0
        c = contrast / 255.0
        k = math.tan((45 + 44 * c) / 180 * math.pi)

        img = (img - 127.5 * (1 - b)) * k + 127.5 * (1 + b)

        # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
        img = np.clip(img, 0, 255).astype(np.uint8)

        return img

    def maskByColor(self, img: np.ndarray) -> np.ndarray:
        # [利用openCV+python进行HSV颜色识别，并结合滑动条动态改变目标颜色\_田土豆的博客-CSDN博客](https://blog.csdn.net/weixin_42216109/article/details/89520423)
        # [OpenCV: Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)

        window = 'Mask by Color'
        self.imgMask = img

        def calculateMask(_) -> np.ndarray:
            # Get the values from the bars
            levelH = cv2.getTrackbarPos('levelH', window)
            rangeH = cv2.getTrackbarPos('rangeH', window)
            levelS = cv2.getTrackbarPos('levelS', window)
            rangeS = cv2.getTrackbarPos('rangeS', window)
            levelV = cv2.getTrackbarPos('levelV', window)
            rangeV = cv2.getTrackbarPos('rangeV', window)
            # Set the lower and upper bounds
            lower = (max(0, levelH - rangeH),
                     max(0, levelS - rangeS),
                     max(0, levelV - rangeV))
            upper = (min(179, levelH + rangeH),
                     min(255, levelS + rangeS),
                     min(255, levelV + rangeV))

            imgHsv = cv2.cvtColor(self.imgMask, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(imgHsv, lower, upper)
            print(f"{lower}, {upper}\r", end="")

            imgTmp = cv2.bitwise_and(self.imgMask, self.imgMask, mask=mask)
            cv2.imshow(window, imgTmp)
            return mask

        cv2.namedWindow(window)
        cv2.createTrackbar('levelH', window, 0, 179, calculateMask)
        cv2.createTrackbar('rangeH', window, 20, 180, calculateMask)
        cv2.createTrackbar('levelS', window, 200, 255, calculateMask)
        cv2.createTrackbar('rangeS', window, 128, 255, calculateMask)
        cv2.createTrackbar('levelV', window, 200, 255, calculateMask)
        cv2.createTrackbar('rangeV', window, 128, 255, calculateMask)

        # Initialize mask
        calculateMask(None)

        # Confirm the masked result
        cv2.waitKey(0)
        mask = calculateMask(None)
        cv2.destroyWindow(window)
        print()  # Keep the finally printed lower and upper bounds

        # Mask the origin image
        return cv2.bitwise_and(self.imgMask, self.imgMask, mask=mask)

    def crop(self, img: np.ndarray, percent: int) -> np.ndarray:
        # Crop out the center area
        percent /= 100
        h = img.shape[0]
        w = img.shape[1]
        y0 = int(h * (1 - percent) / 2)
        y1 = h - y0
        x0 = int(w * (1 - percent) / 2)
        x1 = w - x0
        return img[y0:y1, x0:x1]

    def chooseArea(self, img: np.ndarray, percent: int) -> np.ndarray:
        # [python - Creating a Blank image based on the dimensions from another pictures - Stack Overflow](https://stackoverflow.com/questions/65928581/creating-a-blank-image-based-on-the-dimensions-from-another-pictures)
        blackBg: np.ndarray = np.zeros_like(img, dtype=np.uint8)

        # Crop out the center area
        percent /= 100
        h = img.shape[0]
        w = img.shape[1]
        y0 = int(h * (1 - percent) / 2)
        y1 = h - y0
        x0 = int(w * (1 - percent) / 2)
        x1 = w - x0

        # Add the area on the bg
        blackBg[y0:y1, x0:x1] = img[y0:y1, x0:x1]
        return blackBg

    def compareImage(self, show: bool = True, original=None, compare=None):
        if not self.debugMode:
            return

        window = "Compare"

        if show:
            if original is None:
                original = self.imgOriginal
            if compare is None:
                compare = self.img

            cv2.imshow(window, np.hstack([original, compare]))
            cv2.waitKey(0)
        else:
            cv2.destroyWindow(window)

    def colorQuantization(self, img: np.ndarray, k: int):
        # [How to find the average colour of an image in Python with OpenCV? - Stack Overflow](https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv?newreg=7550175d510343eba40bc392203da6fc)
        # [OpenCV: K-Means Clustering in OpenCV](https://docs.opencv.org/3.4/d1/d5c/tutorial_py_kmeans_opencv.html)

        pixels = np.float32(img.reshape(-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flag = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, flag)
        # labels: the pixel map of each color in centers
        # label: the index of centers

        # Map labels back into each color in centers
        """
        e.g.:
        >>> a = np.array([6,7])
        >>> b = np.array([0,0,0,1,1])
        >>> a[b]
        array([6, 6, 6, 7, 7])
        """
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        # Reshape to the original image
        res: np.ndarray = res.reshape((img.shape))

        # Get pixel amounts of each label (color)
        labels, counts = np.unique(labels, return_counts=True)

        # Sort labels by counts decreasingly
        labels = [l for _, l in sorted(zip(counts, labels), reverse=True)]
        # Map labels back into each color in centers
        dominants = centers[labels]
        self.compareImage(original=img, compare=res)
        return res, dominants

    def dominantColor(self, img: np.ndarray):
        res, dominants = self.colorQuantization(img, 3)
        dominantColor = dominants[0]

        dominantColorImg = img.copy()
        dominantColorImg[:] = dominants[0]

        self.compareImage(original=res, compare=dominantColorImg)

        BGR = np.uint8([[dominantColor]])
        HSV = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)
        colorHSV: np.ndarray = HSV[0][0]
        return colorHSV

    def colorName(self, img: np.ndarray) -> str:
        # [HSV](https://color.lukas-stratmann.com/color-systems/hsv.html)
        hue, saturation, value = self.dominantColor(img)
        if value < 64:
            return "black"
        elif saturation < 32:
            if value > 256-32:
                return "white"
            else:
                return "gray"

        def hueDiffence(colorHuePair: tuple) -> int:
            diff = abs(hue - colorHuePair[1])
            return diff if diff < 90 else 180 - diff

        color, _ = min(self.color2Hue.items(), key=hueDiffence)
        return color

    def main(self):

        # Blur
        self.img: np.ndarray = cv2.GaussianBlur(self.img, (15, 15), 0)
        self.compareImage()

        # Enhance
        self.img = self.enhance(self.img, 0, 200)
        self.compareImage()

        # Choose detection area
        self.img = self.chooseArea(self.img, percent=self.CROP_PERCENTAGE)
        self.imgCropped = self.crop(self.img, percent=self.CROP_PERCENTAGE)
        self.compareImage()

        color = self.colorName(self.imgCropped)
        print(f"The dominant color is {color}.")
        cv2.destroyAllWindows()

        if color == "red":
            print("The complementary color of red is GREEN!")
        elif color == "blue":
            print("The complementary color of blue is YELLOW!")


def main():
    # [OpenCV and Python Color Detection - PyImageSearch](https://pyimagesearch.com/2014/08/04/opencv-python-color-detection/)

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", help="path to the image")
    ap.add_argument("--debug", help="'y' if you want to turn on the debug mode")
    ap.add_argument("--detect", help="detect the image from how many percent of the center (40 by default)")
    ap.add_argument("--resize", help="resize the image to how many percent (60 by default)")
    args = vars(ap.parse_args())

    # load the image
    imageFilename = args["image"]
    debugMode = args["debug"]
    detect = int(args["detect"]) if args["detect"] is not None else 40
    resize = int(args["resize"]) if args["resize"] is not None else 60
    # imageFilename = "/Users/andrewchiu/Downloads/IMG_2556.PNG"
    img = cv2.imread(imageFilename)
    c = ColorDetection(img, detect, resize, debugMode)
    c.main()


if __name__ == "__main__":
    main()
