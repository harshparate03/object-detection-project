# USAGE
# python yolo.py --image images/baggage_claim.jpg
# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
from ultralytics import YOLO
import torch
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description='Advanced YOLO Object Detection')
    parser.add_argument('-i', '--input', required=True,
                        help='path to input image or directory')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                        help='minimum probability to filter weak detections')
    parser.add_argument('-m', '--model', default='yolov8n.pt',
                        help='path to YOLO model (yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt)')
    parser.add_argument('-s', '--size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('-o', '--output', default='outputs',
                        help='output folder')
    return parser.parse_args()

def create_output_folder(output_path):
    """Create output folder if it doesn't exist"""
    os.makedirs(output_path, exist_ok=True)
    return output_path

def load_model(model_path, device):
    """Load YOLO model"""
    try:
        print(f"Loading YOLO model: {model_path}")
        model = YOLO(model_path)
        model.to(device)
        return model
    except Exception as e:
        raise Exception(f"Error loading model: {e}")

def process_image(image_path, model, conf_threshold, size, output_folder):
    """Process a single image"""
    try:
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            raise Exception(f"Could not read image: {image_path}")

        # Get original image dimensions
        original_height, original_width = image.shape[:2]

        # Perform detection
        start_time = time.time()
        results = model(image,
                       conf=conf_threshold,    # Confidence threshold
                       iou=0.5,               # NMS IOU threshold
                       max_det=100,           # Maximum detections
                       imgsz=size)            # Inference size
        
        inference_time = time.time() - start_time

        # Process results
        detected_objects = {}
        annotated_image = image.copy()
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Get class and confidence
                conf = float(box.conf)
                cls = int(box.cls)
                class_name = model.names[cls]
                
                # Count objects
                detected_objects[class_name] = detected_objects.get(class_name, 0) + 1
                
                # Generate random color for this class
                color = (
                    hash(class_name) % 256,
                    hash(class_name * 2) % 256,
                    hash(class_name * 3) % 256
                )
                
                # Draw box
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                
                # Add label with confidence
                label = f'{class_name} {conf:.2f}'
                (label_width, label_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                
                # Draw label background
                cv2.rectangle(annotated_image, 
                            (x1, y1 - label_height - 10),
                            (x1 + label_width, y1),
                            color, -1)
                
                # Draw label text
                cv2.putText(annotated_image, label,
                           (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (255, 255, 255), 2)

        # Save result
        output_filename = f"{Path(image_path).stem}_detected{Path(image_path).suffix}"
        output_path = os.path.join(output_folder, output_filename)
        cv2.imwrite(output_path, annotated_image)

        # Return detection info
        return {
            'path': str(image_path),
            'objects': detected_objects,
            'inference_time': inference_time,
            'output_path': output_path
        }

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def detect_objects(input_path, model_path, conf_threshold, size, output_folder):
    """Main detection function"""
    try:
        # Check GPU availability
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {device}")

        # Create output folder
        output_folder = create_output_folder(output_folder)

        # Load model
        model = load_model(model_path, device)

        # Process input (file or directory)
        input_path = Path(input_path)
        results = []

        if input_path.is_file():
            # Single image
            result = process_image(input_path, model, conf_threshold, size, output_folder)
            if result:
                results.append(result)
        elif input_path.is_dir():
            # Directory of images
            image_files = [f for f in input_path.glob('*') 
                         if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
            
            for image_file in image_files:
                result = process_image(image_file, model, conf_threshold, size, output_folder)
                if result:
                    results.append(result)
        else:
            raise Exception(f"Invalid input path: {input_path}")

        # Print summary
        print("\nDetection Summary:")
        print("-" * 50)
        for result in results:
            print(f"\nImage: {result['path']}")
            print(f"Inference time: {result['inference_time']:.2f} seconds")
            print("Detected objects:")
            for obj, count in result['objects'].items():
                print(f"  - {obj}: {count}")
            print(f"Output saved: {result['output_path']}")

        return results

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    args = parse_arguments()
    
    try:
        # Ensure ultralytics is installed
        try:
            import ultralytics
        except ImportError:
            print("Installing ultralytics...")
            import subprocess
            subprocess.check_call(["pip", "install", "ultralytics"])
            print("Installation successful!")

        # Run detection
        detect_objects(
            args.input,
            args.model,
            args.confidence,
            args.size,
            args.output
        )

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()