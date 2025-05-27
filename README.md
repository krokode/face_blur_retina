# Face Blurring from Video

This project provides a set of Python scripts to extract frames from a video, detect faces in each frame using RetinaFace, apply a blur effect to the detected faces, and then reconstruct a new video from the blurred frames.

---

## 📦 Setup and Dependencies

### 🧰 Requirements

- **ffmpeg** – Used for video frame extraction and rebuilding.
- **RetinaFace (via DeepFace)** – For accurate face detection.

---

### 🧪 ffmpeg Installation

Make sure `ffmpeg` is installed on your system:

- **Ubuntu**:
  ```bash
  sudo apt-get install ffmpeg

- **macOS**:
   ```bash
   brew install ffmpeg

### 🐍 Python Dependencies

Install required packages:

   ```bash
   pip install -r requirements.txt

Note: On first run, deepface will automatically download the retinaface.h5 model and store it at:
~/.deepface/weights/retinaface.h5


### ⚡️ GPU Acceleration (Optional)

If you’re using PyTorch and have a CUDA-enabled GPU, you can enable GPU acceleration for face detection.

For PyTorch users:
Add this to the top of face_coords.py:
Python: import torch
        torch.set_default_tensor_type('torch.cuda.FloatTensor')

For retinaface-torch users:
Pass the parameter device='cuda' when initializing the detector.

### 🗂 Project Structure
.
├── blur_faces.py           # Main script to run the full pipeline
├── face_coords.py          # Face detection using RetinaFace
├── video_to_frames.py      # Frame extraction from video
├── requirements.txt        # Python dependencies
└── README.md               # This file

### 🔍 Function Details

#### blur_faces.py
map_face(input_video, output_directory, bboxes_file, blured_frame_dir)
Extracts frames, detects faces, saves coordinates to a JSON file, and applies blur.

apply_blur_to_image(frame_path, BLURRED_FRAMES_DIR, file, coordinates)
Applies Gaussian blur to face regions in an image.

blur_from_bboxes(bboxes_file, output_dir, BLURRED_FRAMES_DIR)
Reads bounding boxes from JSON and blurs corresponding faces.

open_bboxes_file_per_frame(bboxes_file)
Generator that yields face coordinates per frame.

rebuild_video_from_blurred_frames(BLURRED_FRAMES_DIR, output_video, FPS=30)
Rebuilds video from blurred image frames using ffmpeg.

remove_directory(directory)
Deletes a directory and all its contents.

#### face_coords.py
get_face_coordinates(image_path)
Detects faces in an image and returns a list of dictionaries with bounding box coordinates: x1, y1, x2, y2.

#### video_to_frames.py
extract_frames(input_video, output_directory)
Uses ffmpeg to extract frames from a video and saves them as JPEGs.

## 🧠 Credits
DeepFace

RetinaFace

FFmpeg

## 📜 License
MIT License