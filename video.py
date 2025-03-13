"""
Open and display a video by an iterator.
Also, capture and saves the position of a click in the video.

tip: use space bar to play and pause the video.
"""
import collections
import time
import os

import cv2
import numpy as np


global paused, clicked
paused = False
clicked = False


class ClickCapture:
    """
    Helper class for OpenCV VideoCapture. Can be used as an iterator.
    """

    clicked_frames = collections.deque([0])

    def __init__(self, video_path, video_name=None, fps=30):
        self.__name = video_name or os.path.dirname(video_path).split('/')[-1]
        self.__capture = cv2.VideoCapture(video_path)
        self.__window_config()

        self.prev_frame_time = 0
        self.new_frame_time = 0

        self.__fps = fps

        self.fps_deque = collections.deque(maxlen=fps)


    def __window_config(self):
        cv2.namedWindow(self.__name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.__name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback(self.__name, mouse_callback, param=[self])
        # cv2.setMouseCallback(self.__name, continuous_click, param=[self])
    
    def __iter__(self):
        if not self.__capture.isOpened():
            raise StopIteration
        return self

    def __next__(self):
        global paused
        ret, frame = self.__capture.read()

        if not ret:
            raise StopIteration

        key = cv2.waitKey(max(2, 1000 // self.__fps))

        # q to quit the video
        if key & 0xFF == ord('q'):
            raise StopIteration

        # space to pause the video
        elif key & 0xFF == ord(' '):
            paused = not paused
            if paused:
                while True:
                    kaux = cv2.waitKey(30) & 0xFF
                    if kaux == ord(' '):
                        paused = False
                        break

                    # b to go back one frame
                    elif kaux == ord(','):
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame - 2)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

                    # f to go forward one frame
                    elif kaux == ord('.'):
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

                    # Avançar 100 quadros
                    elif kaux == ord('h') and paused:
                        self.current_frame += 100
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

                    # Recuar 100 frames
                    elif kaux == ord('m') and paused:
                        self.current_frame -= 100
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame - 2)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

                    # Avançar 250 quadros
                    elif kaux == ord('l') and paused:
                        self.current_frame += 250
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

                    # Recuar 250 frames
                    elif kaux == ord('k') and paused:
                        self.current_frame -= 250
                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame - 2)
                        ret, frame = self.__capture.read()
                        cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow(self.__name, frame)
                        cv2.waitKey(30)

        return frame

    def __del__(self):
        self.__capture.release()
        cv2.destroyAllWindows()

    @property
    def current_frame(self):
        return int(self.__capture.get(cv2.CAP_PROP_POS_FRAMES))
    
    @current_frame.setter
    def current_frame(self, value):
        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, value)
    
    @property
    def win_name(self):
        return self.__name

    def show(self, frame, only_print=False):
        global clicked
        self.new_frame_time = time.time()
        self.fps_deque.append(1 / (self.new_frame_time - self.prev_frame_time))
        self.prev_frame_time = self.new_frame_time

        if only_print:
            print(f'{self.__name} - FPS: {np.mean(self.fps_deque):5.2f}')
        else:
            cv2.putText(frame, f'Frame: {self.current_frame}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # cv2.putText(frame, f'Click: {clicked}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow(self.__name, frame)
            cv2.setWindowTitle(self.__name, f'{self.__name} - FPS: {np.mean(self.fps_deque):5.2f}')
            
            total_frames = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
            if self.current_frame%len(self.fps_deque):
                print(f'{self.__name} ({(self.current_frame/total_frames)*100:.2f}%) - FPS: {np.mean(self.fps_deque):5.2f}')


def mouse_callback(event, x, y, flags, params):
    path = os.path.join('./runs', params[0].win_name)
    os.makedirs(path, exist_ok=True)

    if event == cv2.EVENT_LBUTTONDOWN:
        global clicked
        clicked = True

        current_frame = params[0].current_frame
        save_at = os.path.join(path, str(current_frame) + '.txt')
        with open(save_at, 'a') as frame_file:
            frame_file.write(f'{x}, {y}\n')

        ClickCapture.clicked_frames.append(current_frame)

def continuous_click(event, x, y, flags, params):
    """continousily capture the mouse click at each frame"""
    global clicked

    path = os.path.join('./runs_cont', params[0].win_name)
    os.makedirs(path, exist_ok=True)

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = not clicked
    elif clicked:
        current_frame = params[0].current_frame
        save_at = os.path.join(path, str(current_frame) + '.txt')
        with open(save_at, 'w') as frame_file:
            frame_file.write(f'{x}, {y}\n')

        ClickCapture.clicked_frames.append(current_frame)


def wait_for_click(cap: ClickCapture):
    global clicked
    clicked = False

    while True:
        cv2.waitKey(1)
        if clicked:
            break
