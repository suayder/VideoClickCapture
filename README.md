# ClickCapture [Under Construction]


This repo contains a python script to run a given video and capture where the user is clicking. Also, it includes a jupyter notebook example to use the data load and display the clicked points.

## DEMO

[![](assets/first_page.png)](https://drive.google.com/file/d/1fe7JgEsmDxfiSc1JlJBSFe1ezeB4KgNb/view?usp=drive_link)

# Quick start

In this tool we use `python = 3.12.9`

install the necessary packages with `pip install -r requirements.txt`

Run with `python main.py --video {path_to_the_video_file}`, example `python main.py --video data/sideseeing-hospitals/data/Jundiai_HSV/Route01-2024-02-28-14-15-07-770/video.mp4`

After run the above cell you will be asked to click on the frames
> the output is saved at `./runs/{video_folder_name}`, like this `./runs/Route01-2024-02-28-14-15-07-770/*.txt`

## Features for click capture:

- every time the user click with the mouse a txt file will be saved with a x,y position.
- it allows only one click per frame
- The name of the file corresponds to the frame number
- The files will be saved at `/runs/{video_folder_name}`
- By default, every 30 frames the app asks for a click. This can be changed by passing the `--force-click` parameter.
- The user can choose the fps ratio to pass the video


**Commands**: 

```
space bar: pause and resume the video
q: quit from the annotation
,: go back one frame
f: to go forward one frame
h: to forward 100 frames
m: to backward 100 frames
l: to forward 250 frames
k: to backward 250 frames
```
