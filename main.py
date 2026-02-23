import argparse
import cv2
import os
from enhancement import enhance_low_light_image
from detector import ObjectDetector
from utils import display_side_by_side, save_output

def process_image(image_path, output_dir, detector, show=True):
    print(f"Processing image: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return

    # 1. Enhance low-light image
    enhanced_image = enhance_low_light_image(image, use_gamma=True, use_clahe=True, gamma_val=0.5)

    # 2. Detect objects on enhanced image
    detected_image, _ = detector.detect(enhanced_image)

    # 3. Handle Output
    # Create combined image
    combined_img = display_side_by_side(image, enhanced_image, detected_image)
    
    if show:
        print("Press any key in the window to close and save...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Save output
    filename = os.path.basename(image_path)
    out_path = os.path.join(output_dir, f"result_{filename}")
    save_output(combined_img, out_path)

def process_video(video_path, output_dir, detector, show=True):
    print(f"Processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_path}")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps: # Handle webcam FPS
        fps = 30.0
    
    # Prepare VideoWriter for combined output (3x width since side-by-side)
    filename = os.path.basename(str(video_path))
    if str(video_path) == "0":
        filename = "webcam.mp4"
    out_path = os.path.join(output_dir, f"result_{filename}")
    os.makedirs(output_dir, exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width * 3, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % 10 == 0:
            print(f"Processing frame {frame_count}...")

        # 1. Enhance
        enhanced_frame = enhance_low_light_image(frame, use_gamma=True, use_clahe=True, gamma_val=0.5)
        
        # 2. Detect
        detected_frame, _ = detector.detect(enhanced_frame)
        
        # 3. Create combined frame
        combined = cv2.hconcat([frame, enhanced_frame, detected_frame])
        out.write(combined)
        
        if show:
            # Scale down for display on smaller screens
            scale = 0.5
            display_img = cv2.resize(combined, (int(combined.shape[1] * scale), int(combined.shape[0] * scale)))
            cv2.imshow("Low-Light Detection Pipeline (Press 'q' to quit)", display_img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Interrupted by user")
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video processing complete. Output saved to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Low-Light Object Detection System")
    parser.add_argument("--image", type=str, help="Path to input image")
    parser.add_argument("--video", type=str, help="Path to input video (or '0' for webcam)")
    parser.add_argument("--no-show", action="store_true", help="Don't show the output window")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory to save outputs")
    
    args = parser.parse_args()
    
    if not args.image and not args.video:
        print("Please provide either --image or --video argument.")
        parser.print_help()
        return
        
    # Initialize Detector
    detector = ObjectDetector()
    
    show_output = not args.no_show
    
    if args.image:
        process_image(args.image, args.output_dir, detector, show=show_output)
        
    if args.video:
        video_source = 0 if args.video == "0" else args.video
        process_video(video_source, args.output_dir, detector, show=show_output)

if __name__ == "__main__":
    main()
