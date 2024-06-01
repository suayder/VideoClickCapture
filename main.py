import json
from os.path import join, dirname
from argparse import ArgumentParser
from video import ClickCapture, wait_for_click 
from helpers.helpers import get_username

global EXEC_PARAMS
EXEC_PARAMS = {}  # is used to store execution parameters

def main(path, fps, force_click, save_dir):

    video_iter = ClickCapture(path, save_dir=save_dir, fps=fps)

    EXEC_PARAMS['video_path'] = path
    EXEC_PARAMS['force_click'] = force_click

    for frame in video_iter:
        video_iter.show(frame)
        if (video_iter.current_frame - ClickCapture.clicked_frames[-1]) > force_click:
            wait_for_click(video_iter)

    print('All clicked frames:', ClickCapture.clicked_frames)
    print(f'You clicked on {len(ClickCapture.clicked_frames)} frames')

    EXEC_PARAMS['save_dir'] = video_iter.save_dir
    EXEC_PARAMS['total_clicked_frames'] = len(ClickCapture.clicked_frames)
    EXEC_PARAMS['clicked_frames'] = list(ClickCapture.clicked_frames)

    with open(join(dirname(video_iter.save_dir),
                   f'params_{get_username()}.json'), 'w') as fp:
        json.dump(EXEC_PARAMS, fp, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--video', required=True, help="path of the video to be watched")
    parser.add_argument('--fps', default=30, type=int, help="fps ratio to show the video")
    parser.add_argument('--force-click', type=int, default=30, help="maximum frames that can elapse without require user click")
    parser.add_argument('--save_dir', default=None, help="directory to save the click text files")

    args = parser.parse_args()

    main(args.video, args.fps, args.force_click, args.save_dir)
