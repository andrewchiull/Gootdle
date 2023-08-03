from datetime import datetime, timedelta
import threading


class Clock:
    def __init__(self) -> None:
        self.running = False

        self.start = datetime.now()
        self.prev = self.start


    def FPS(self, fps: float) -> bool:
        if self.curr - self.prev > timedelta(seconds=1/fps):
            self.prev = self.curr
            return True
        else:
            return False

    def run(self):
        self.running = True
        while self.running:
            self.curr = datetime.now()

    def stop(self):
        self.running = False

clock = Clock()

if __name__ == "__main__":
    thread = threading.Thread(target=clock.run)
    thread.start()

    while True:
        if clock.FPS(3):
            print(f"{clock.curr}")