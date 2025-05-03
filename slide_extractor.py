import os                    # For creating directories and handling file paths
import cv2                   # OpenCV for reading and writing video frames
import imagehash             # For perceptual image hashing (detecting changes)
from PIL import Image        # PIL (Pillow) for image processing
from pytube import YouTube   # pytube for download videos from YouTube
import time                  # For adding delay
import re                    # For sanitizing filenames
from datetime import datetime  # For fallback timestamp naming
import subprocess
import tempfile

# Removing invalid filename characters from a string (Windows-safe)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Extracting slide images by comparing each frame using image hashing
def extract_unique_slides(video_path, video_title, output_base='slides', interval=15, hash_diff_threshold=5):
    # Opening the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[ERROR] Failed to open video file.")
        return

    # Getting frames per second and total frames
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval)  # How many frames between checks

    print(f"[INFO] Starting slide extraction...")

    last_hash = None
    slide_images = []

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        if frame_id % frame_interval == 0:
            # Saving temporary frame image
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                temp_path = tmp_file.name
                cv2.imwrite(temp_path, frame)

            # Computing perceptual hash
            current_hash = imagehash.phash(Image.open(temp_path))

            # If it's different from the previous, saving it
            if last_hash is None or abs(current_hash - last_hash) > hash_diff_threshold:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image).convert("RGB")
                slide_images.append(pil_image)
                last_hash = current_hash

            os.remove(temp_path)

        frame_id += 1

    cap.release()

    # Saving slides to PDF only if any slides were captured
    if slide_images:
        output_dir = "slides"
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_path = os.path.join(output_dir, f"{video_title}_slides.pdf")
        slide_images[0].save(output_pdf_path, save_all=True, append_images=slide_images[1:])
        print(f"[SUCCESS] Slide extraction complete. PDF saved to: {output_pdf_path}")
    else:
        print("[INFO] No distinct slides found.")

# Downloading a YouTube video and saves it locally
def download_video_yt_dlp(url, output_dir='downloads'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Getting the video title
        result = subprocess.run(
            ['yt-dlp', '--get-title', url],
            capture_output=True, text=True, check=True
        )

        title = sanitize_filename(result.stdout.strip())

    except subprocess.CalledProcessError:
        print("[WARNING] Failed to fetch title. Using timestamp instead.")
        title = datetime.now().strftime("video_%Y%m%d_%H%M%S")

    output_path = os.path.join(output_dir, f"{title}.mp4")

    # Downloading the video
    print(f"[INFO] Downloading video '{title}'...")
    subprocess.run([
        'yt-dlp', '-f', 'best[ext=mp4]', '-o', output_path, url
    ], check=True)

    print(f"[INFO] Download complete: {output_path}")
    return output_path, title

# Main program entry point
if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ").strip()  # Getting user input 
    video_path, video_title = download_video_yt_dlp(youtube_url)     # Downloading video
    extract_unique_slides(video_path, video_title)            # Extracting slides
