import cv2
import numpy as np

# Function to extract frames from a video with skipping and resizing
#set resize_factor=1, frame_skip=5 for a balance of quality and performance
def extract_frames(video_path, resize_factor=1, frame_skip=5):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames to reduce processing
        if frame_count % frame_skip == 0:
            # Resize frame to reduce computational load
            frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_LINEAR)
            frames.append(frame)

        frame_count += 1

    cap.release()
    return frames

# Function to stitch frames together
def stitch_frames(frames):
    stitcher = cv2.createStitcher() if int(cv2.__version__.split('.')[0]) < 4 else cv2.Stitcher_create()
    
    status, panorama = stitcher.stitch(frames)
    
    if status == cv2.Stitcher_OK:
        return panorama
    else:
        print(f"Stitching failed with status {status}")
        return None

# Main function
def main(video_path, output_path):
    print("Extracting frames...")
    frames = extract_frames(video_path)

    if len(frames) < 2:
        print("Not enough frames to create a panorama.")
        return

    print("Stitching frames to create a panorama...")
    panorama = stitch_frames(frames)

    if panorama is not None:
        print("Saving panorama...")
        cv2.imwrite(output_path, panorama)
        print(f"Panorama saved to {output_path}")
    else:
        print("Failed to create a panorama.")

if __name__ == "__main__":
    video_path = "video.mp4"  # Replace with the path to your video file
    output_path = "panorama.jpg"    # Replace with the desired output file path

    main(video_path, output_path)
