# ClickCapture [Under Construction]


This repo contains a python script to run a given video and capture where is the user clicking. Also, it includes a jupyter notebook example to use the data load and display the clicked points.

#### Features for click capture:

- every time the user click with the mouse a txt file will be saved with a x,y position.
- The name of the file corresponds to the frame number
- The files will be saved at `{video_folder}/{video_name}/{username}/*.txt` or at `save_dir` argument
- By default, every 30 frames the app asks for a click. This can be changed by passing the `--force-click` parameter.
- The user can choose the fps ratio to pass the video


- **Commands**: 
> space bar: pause and resume the video
> 
> q: quit from the annotation

#### How to use it

> Install the requirements in `requirements.txt`

> just type `python main.py --video <path to the video>` or `python main.py -h` to see the arguments.

> Use the `viewer.ipynb` to run a visualization of your annotation 