# ClickCapture [Under Construction]


This repo contains a python script to run a given video and capture where is the user clicking.

#### Features:

- every time the user click with the mouse a txt file will be saved with a x,y position.
- The name of the file corresponds to the frame number
- The files will be saved at `{video_folder}/{video_name}/*.txt` or at `save_dir` argument
- By default, every 30 frames the app asks for a click. This can be changed as explained further in this readme.
- The user can choose the fps ratio to pass the video

#### How to use it

> Install the requirements in `requirements.txt`

> just type `python main.py --video <path to the video>` or `python main.py -h` to see the arguments