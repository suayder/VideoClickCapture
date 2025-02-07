# ClickCapture [Under Construction]


This repo contains a python script to run a given video and capture where is the user clicking.

#### Features:
- every time the user click with the mouse a txt file will be saved with a x,y position.
- The name of the file corresponds to the frame number
- The file will be saved at `./runs/{video_folder_name}`
- By default, every 30 frames the app asks for a click. This can be changed as explained further in this readme.
- The user can choose the fps ratio to pass the video

##### Files in this repo:

- `file_loader.py` contains a function that you can load every text file in a single dataframe

#### How to use it

> in a virtual environment type `python -m pip install -r requirements.txt`

> just type `python main.py` or `python main.py -h` to see the arguments