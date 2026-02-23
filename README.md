# Low-Light & Night-Time Object Detection System

This MVP project demonstrates a fast, lightweight AI pipeline to detect objects in low-light or night-time environments without requiring heavy custom model training. It uses classical computer vision for fast image enhancement, followed by a state-of-the-art pre-trained deep learning detector.

## Architecture Pipeline

1. **Input**: Accepts image files, video files, or a live webcam (`0`).
2. **Low-Light Enhancement**: Applies a fast combination of noise reduction, Gamma Correction, and Contrast Limited Adaptive Histogram Equalization (CLAHE) using OpenCV to illuminate dark regions.
3. **Detection**: Passes the enhanced image to Ultralytics YOLOv8 (Nano version) for fast and accurate object bounding-box detection.
4. **Output**: Displays the Original, Enhanced, and Detected images side-by-side in real-time, and saves the output locally.

## Project Structure

```text
nightLight-Detection/
├── main.py             # CLI Entry point and main processing logic
├── enhancement.py      # Gamma and CLAHE enhancement functions
├── detector.py         # YOLOv8 Object detection wrapper
├── utils.py            # Helper functions for display and saving
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── sample_inputs/      # Directory to place your test images/videos
└── outputs/            # Directory where results are saved
```

## Setup Instructions

1. **Install Dependencies**
   Ensure you have Python 3.8+ installed. From the `nightLight-Detection` directory, run:
   ```bash
   pip install -r requirements.txt
   ```
   _(Note: This might take a minute to download PyTorch and Ultralytics YOLO and its dependencies)_

## Usage

### Image Detection

Run the pipeline on a single image. The result window will wait for you to press any key to close.

```bash
python main.py --image path/to/dark_image.jpg
```

### Video Detection

Run the pipeline on a video file.

```bash
python main.py --video path/to/dark_video.mp4
```

### Live Webcam Detection

Run the pipeline on your live webcam (if you have one connected). Press `q` to quit the live feed.

```bash
python main.py --video 0
```

### Additional Options

- Add `--no-show` to quickly process files in the background without opening UI windows:
  ```bash
  python main.py --image dark_image.jpg --no-show
  ```
- Change the output directory (default is `outputs/`):
  ```bash
  python main.py --image dark_image.jpg --output-dir my_custom_results
  ```
