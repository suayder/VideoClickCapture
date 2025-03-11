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

from helpers import Logger, get_username

global paused, clicked, drawing
paused = False
clicked = False
drawing = False

logger = Logger().get_logger('video')

def mouse_callback(event, x, y, flags, params):
    global clicked, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        drawing = True

        current_frame_number = params[0].current_frame_number
        save_at = os.path.join(params[0].save_dir, str(current_frame_number)+'.txt')

        cv2.circle(params[0].current_frame_image,(x,y),15,(0,0,255),-1)
        params[0].show()

        with open(save_at, 'w') as frame_file:
            frame_file.write(f'{x}, {y}')

        ClickCapture.clicked_frames.append(current_frame_number)
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing:
            cv2.circle(params[0].current_frame_image,(x,y),15,(0,0,255),-1)
            params[0].show()
            drawing = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        clicked = True
        ClickCapture.rclicks_frames.append(params[0].current_frame_number)

class ClickCapture:
    """
    Helper class for OpenCV VideoCapture. Can be used as an iterator.
    """

    clicked_frames = collections.deque([0])
    rclicks_frames = collections.deque([0])

    def __init__(self, video_path, save_dir=None, fps=30):

        video_path = os.path.abspath(video_path)
        self.__name = os.path.dirname(video_path).split('/')[-1] # video name without extension
        self.__capture = cv2.VideoCapture(video_path)
        self.__current_frame_image = None

        self.prev_frame_time = 0
        self.new_frame_time = 0

        self.__fps = fps

        self.fps_deque = collections.deque(maxlen=fps)

        # config save_dir
        self.save_dir = os.path.abspath(save_dir) if save_dir else os.path.join(os.path.dirname(video_path), 'clicks')
        i = 0
        save_find_dir = self.save_dir
        while os.path.exists(save_find_dir):
            i += 1
            save_find_dir = f'{self.save_dir}_{i}'
            logger.warning(f'The folder "{self.save_dir}" already exists to save files. Checking for {save_find_dir}.')
        else:
            self.save_dir = save_find_dir
            os.makedirs(self.save_dir, exist_ok=True)
            logger.info(f'created directory {self.save_dir}')

    def __window_config(self):

        width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cv2.namedWindow(self.__name)
        cv2.resizeWindow(self.__name, width, height)
        # cv2.setWindowProperty(self.__name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback(self.__name, mouse_callback, param=[self])

    def __iter__(self):
        if not self.__capture.isOpened():
            raise StopIteration
        self.__current_frame_number = 0
        return self

    def __next__(self):
        ret, frame = self.__capture.read()
        self.__current_frame_number += 1
        global paused

        if not ret:
            raise StopIteration

        key = cv2.waitKey(max(10, 1000//self.__fps))
        
        # q to quit the video
        if key & 0xFF == ord('q'):
            raise StopIteration

        # space to pause the video
        elif key & 0xFF == ord(' '):
            paused = not paused
            while paused:
                kaux = cv2.waitKey(30) & 0xFF
                if kaux == ord(' '):
                    paused = False
                    break
        self.__current_frame_image = frame
        return frame

    def __del__(self):
        self.__capture.release()
        cv2.destroyAllWindows()

    @property
    def current_frame_number(self):
        return self.__current_frame_number
        # return int(self.__capture.get(cv2.CAP_PROP_POS_FRAMES))
    
    @property
    def current_frame_image(self):
        return self.__current_frame_image
    @property
    def win_name(self):
        return self.__name

    def show(self, frame=None, only_print=False):
        self.new_frame_time = time.time()
        self.fps_deque.append(1 / (self.new_frame_time - self.prev_frame_time))
        self.prev_frame_time = self.new_frame_time

        if only_print:
            print(f'{self.__name} - FPS: {np.mean(self.fps_deque):5.2f}')
        else:
            self.__window_config()
            cv2.setWindowTitle(self.__name, f'{self.__name} - FPS: {np.mean(self.fps_deque):5.2f}')
            if frame is None:
                cv2.imshow(self.__name, self.current_frame_image)
            else:
                cv2.imshow(self.__name, frame)

            # total_frames = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
            # if self.__current_frame_number%len(self.fps_deque):
            #     print(f'{self.__name} ({(self.__current_frame_number/total_frames)*100:.2f}%) - FPS: {np.mean(self.fps_deque):5.2f}')


def wait_for_click(cap: ClickCapture, frame):

    global clicked
    clicked = False
    
    cap.show()
    while not clicked:
        cv2.waitKey(30)