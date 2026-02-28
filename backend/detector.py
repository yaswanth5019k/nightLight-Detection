import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_name="yolov8n.pt"):
        """
        Initialize the YOLOv8 object detector.
        Uses yolov8n.pt (Nano version) by default for faster CPU inference.
        """
        print(f"Loading YOLO model: {model_name}...")
        self.model = YOLO(model_name)
        print("Model loaded successfully.")
        
    def detect(self, image, conf_threshold=0.5):
        """
        Run inference on a single image.
        Returns the annotated image and the list of detections.
        """
        # Run inference
        results = self.model(image, conf=conf_threshold, verbose=False)
        
        # results[0] contains the predictions for the first image
        annotated_image = results[0].plot()
        
        return annotated_image, results[0].boxes
