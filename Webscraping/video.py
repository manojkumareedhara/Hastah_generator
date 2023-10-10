import cv2
import os
import pafy


import random

# Get video streaming URL using pafy
def get_streaming_url(youtube_url):
    video = pafy.new(youtube_url)
    best = video.getbest(preftype="mp4")
    return best.url

# Extract random frames from streaming video using OpenCV
def extract_random_frames(video_url, num_frames=5):
    cap = cv2.VideoCapture(video_url)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_ids = sorted(random.sample(range(0, total_frames), num_frames))
    frames = []

    for fid in frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frame = cap.read()
        frames.append(frame)

    cap.release()
    return frames

# Display frames using OpenCV
def display_frames(frames):
    for idx, frame in enumerate(frames):
        cv2.imshow(f'Frame {idx + 1}', frame)
        cv2.waitKey(0)  # Waits for a key press to show the next frame

    cv2.destroyAllWindows()  # Close all image windows

youtube_url = "https://www.youtube.com/watch?v=ABl8-quPXcw"  # Replace with your YouTube video URL
streaming_url = get_streaming_url(youtube_url)
frames = extract_random_frames(streaming_url)
display_frames(frames)
