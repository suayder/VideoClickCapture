from argparse import ArgumentParser
from video import ClickCapture, wait_for_click


def main(path, fps, force_click, mode, video_name):
    video_iter = ClickCapture(path, fps=fps, video_name=video_name)

    if mode == 'click':
        for frame in video_iter:
            video_iter.show(frame)
            if (video_iter.current_frame - ClickCapture.clicked_frames[-1]) > force_click:
                wait_for_click(video_iter)
    elif mode == 'continuous':
        for frame in video_iter:
            video_iter.show(frame)
        
    print('All clicked frames:', ClickCapture.clicked_frames)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--video', required=True, help="path of the video to be watched")
    parser.add_argument('--mode', default='click', choices=['click', 'continuous'], help="mode of the program")
    parser.add_argument('--video-name', help="name of the video")
    parser.add_argument('--fps', default=30, type=int, help="fps ratio to show the video")
    parser.add_argument('--force-click', type=int, default=30, help="maximum frames that can elapse without require user click")

    args = parser.parse_args()

    main(args.video, args.fps, args.force_click, args.mode, args.video_name)
