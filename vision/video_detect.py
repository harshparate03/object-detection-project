# import numpy as np
# import argparse
# import time
# import cv2
# import os
# from ultralytics import YOLO
# import torch
# from pathlib import Path

# def parse_arguments():
#     parser = argparse.ArgumentParser(description='Advanced YOLO Object Detection for Images and Videos')
#     parser.add_argument('-i', '--input', required=True,
#                       help='path to input image/video file or camera index (0 for webcam)')
#     parser.add_argument('-c', '--confidence', type=float, default=0.3,
#                       help='minimum probability to filter weak detections')
#     parser.add_argument('-m', '--model', default='yolov8n.pt',
#                       help='path to YOLO model')
#     parser.add_argument('-s', '--size', type=int, default=640,
#                       help='inference size (pixels)')
#     parser.add_argument('-o', '--output', default='outputs',
#                       help='output folder')
#     parser.add_argument('--source-type', choices=['image', 'video', 'camera'],
#                       help='specify input source type (will auto-detect if not specified)')
#     return parser.parse_args()

# def create_output_folder(output_path):
#     """Create output folder if it doesn't exist"""
#     os.makedirs(output_path, exist_ok=True)
#     return output_path

# def load_model(model_path, device):
#     """Load YOLO model"""
#     try:
#         print(f"Loading YOLO model: {model_path}")
#         model = YOLO(model_path)
#         model.to(device)
#         return model
#     except Exception as e:
#         raise Exception(f"Error loading model: {e}")

# def process_image(image_path, model, conf_threshold, size, output_folder):
#     """Process a single image"""
#     try:
#         # Read image
#         image = cv2.imread(str(image_path))
#         if image is None:
#             raise Exception(f"Could not read image: {image_path}")

#         # Get original image dimensions
#         original_height, original_width = image.shape[:2]

#         # Perform detection
#         start_time = time.time()
#         annotated_image, detected_objects = process_frame(image, model, conf_threshold, size)
#         inference_time = time.time() - start_time

#         # Save result
#         output_filename = f"{Path(image_path).stem}_detected{Path(image_path).suffix}"
#         output_path = os.path.join(output_folder, output_filename)
#         cv2.imwrite(output_path, annotated_image)

#         # Return detection info
#         return {
#             'path': str(image_path),
#             'objects': detected_objects,
#             'inference_time': inference_time,
#             'output_path': output_path
#         }

#     except Exception as e:
#         print(f"Error processing {image_path}: {e}")
#         return None

# def process_frame(frame, model, conf_threshold, size):
#     """Process a single frame and return annotated frame and detections"""
#     try:
#         # Perform detection
#         results = model(frame,
#                        conf=conf_threshold,    # Confidence threshold
#                        iou=0.5,               # NMS IOU threshold
#                        max_det=100,           # Maximum detections
#                        imgsz=size)            # Inference size
        
#         # Process results
#         detected_objects = {}
#         annotated_frame = frame.copy()
        
#         for r in results:
#             boxes = r.boxes
#             for box in boxes:
#                 # Get box coordinates
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
                
#                 # Get class and confidence
#                 conf = float(box.conf)
#                 cls = int(box.cls)
#                 class_name = model.names[cls]
                
#                 # Count objects
#                 detected_objects[class_name] = detected_objects.get(class_name, 0) + 1
                
#                 # Generate random color for this class
#                 color = (
#                     hash(class_name) % 256,
#                     hash(class_name * 2) % 256,
#                     hash(class_name * 3) % 256
#                 )
                
#                 # Draw box
#                 cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
#                 # Add label with confidence
#                 label = f'{class_name} {conf:.2f}'
#                 (label_width, label_height), _ = cv2.getTextSize(
#                     label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                
#                 # Draw label background
#                 cv2.rectangle(annotated_frame, 
#                             (x1, y1 - label_height - 10),
#                             (x1 + label_width, y1),
#                             color, -1)
                
#                 # Draw label text
#                 cv2.putText(annotated_frame, label,
#                            (x1, y1 - 5),
#                            cv2.FONT_HERSHEY_SIMPLEX,
#                            0.5, (255, 255, 255), 2)

#         return annotated_frame, detected_objects

#     except Exception as e:
#         print(f"Error processing frame: {e}")
#         return frame, {}

# def process_video(source, model, conf_threshold, size, output_path):
#     """Process video file or camera stream"""
#     try:
#         # Open video source
#         if isinstance(source, str) and source.isdigit():
#             cap = cv2.VideoCapture(int(source))  # Camera
#         else:
#             cap = cv2.VideoCapture(str(source))  # Video file
            
#         if not cap.isOpened():
#             raise Exception("Error opening video source")

#         # Get video properties
#         frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = int(cap.get(cv2.CAP_PROP_FPS))

#         # Create video writer if source is not camera
#         if not (isinstance(source, str) and source.isdigit()):
#             output_filename = f"{Path(source).stem}_detected.mp4"
#             output_file = os.path.join(output_path, output_filename)
#             writer = cv2.VideoWriter(output_file,
#                                    cv2.VideoWriter_fourcc(*'mp4v'),
#                                    fps, (frame_width, frame_height))

#         print("Processing video... Press 'q' to quit.")
#         frame_count = 0
#         total_time = 0
        
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame_count += 1
#             start_time = time.time()

#             # Process frame
#             annotated_frame, detections = process_frame(frame, model, conf_threshold, size)
            
#             # Calculate and display FPS
#             process_time = time.time() - start_time
#             total_time += process_time
#             fps_current = 1 / process_time if process_time > 0 else 0
            
#             # Add FPS counter to frame
#             cv2.putText(annotated_frame, f"FPS: {fps_current:.1f}",
#                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#             # Display frame
#             cv2.imshow('YOLO Detection', annotated_frame)

#             # Save frame if processing video file
#             if not (isinstance(source, str) and source.isdigit()):
#                 writer.write(annotated_frame)

#             # Break if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Cleanup
#         cap.release()
#         if not (isinstance(source, str) and source.isdigit()):
#             writer.release()
#         cv2.destroyAllWindows()

#         # Print summary
#         avg_fps = frame_count / total_time if total_time > 0 else 0
#         print(f"\nVideo Processing Summary:")
#         print(f"Processed {frame_count} frames")
#         print(f"Average FPS: {avg_fps:.2f}")
#         if not (isinstance(source, str) and source.isdigit()):
#             print(f"Output saved: {output_file}")

#     except Exception as e:
#         print(f"Error processing video: {e}")

# def detect_objects(input_path, model_path, conf_threshold, size, output_folder, source_type=None):
#     """Main detection function"""
#     try:
#         # Check GPU availability
#         device = 'cuda' if torch.cuda.is_available() else 'cpu'
#         print(f"Using device: {device}")

#         # Create output folder
#         output_folder = create_output_folder(output_folder)

#         # Load model
#         model = load_model(model_path, device)

#         # Determine source type if not specified
#         if source_type is None:
#             if input_path.isdigit():
#                 source_type = 'camera'
#             elif Path(input_path).is_file():
#                 ext = Path(input_path).suffix.lower()
#                 if ext in ['.mp4', '.avi', '.mov', '.mkv']:
#                     source_type = 'video'
#                 elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
#                     source_type = 'image'
#             elif Path(input_path).is_dir():
#                 source_type = 'image'  # Directory of images

#         # Process based on source type
#         if source_type in ['video', 'camera']:
#             process_video(input_path, model, conf_threshold, size, output_folder)
#         else:
#             # Use existing image processing code
#             if Path(input_path).is_file():
#                 result = process_image(input_path, model, conf_threshold, size, output_folder)
#                 if result:
#                     print_image_results([result])
#             elif Path(input_path).is_dir():
#                 image_files = [f for f in Path(input_path).glob('*') 
#                              if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
#                 results = []
#                 for image_file in image_files:
#                     result = process_image(image_file, model, conf_threshold, size, output_folder)
#                     if result:
#                         results.append(result)
#                 print_image_results(results)

#     except Exception as e:
#         print(f"Error: {e}")

# def print_image_results(results):
#     """Print summary for image detection results"""
#     print("\nDetection Summary:")
#     print("-" * 50)
#     for result in results:
#         print(f"\nImage: {result['path']}")
#         print(f"Inference time: {result['inference_time']:.2f} seconds")
#         print("Detected objects:")
#         for obj, count in result['objects'].items():
#             print(f"  - {obj}: {count}")
#         print(f"Output saved: {result['output_path']}")

# def main():
#     args = parse_arguments()
    
#     try:
#         # Ensure ultralytics is installed
#         try:
#             import ultralytics
#         except ImportError:
#             print("Installing ultralytics...")
#             import subprocess
#             subprocess.check_call(["pip", "install", "ultralytics"])
#             print("Installation successful!")

#         # Run detection
#         detect_objects(
#             args.input,
#             args.model,
#             args.confidence,
#             args.size,
#             args.output,
#             args.source_type
#         )

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()




import argparse
import logging
import os
import time
from pathlib import Path
from typing import Dict, Tuple, Optional, Union
from django.conf import settings
import cv2
import numpy as np

class ColorPalette:
    """Manage color generation for object detection"""
    def __init__(self, num_colors: int = 20):
        """Generate a diverse color palette"""
        np.random.seed(42)  # For reproducibility
        self.colors = np.random.randint(0, 255, size=(num_colors, 3)).tolist()

    def get_color(self, index: int) -> Tuple[int, int, int]:
        """Get a color for a specific index"""
        return self.colors[index % len(self.colors)]

class YOLODetector:
    """Advanced YOLO Object Detection Class"""
    def __init__(
        self, 
        model_path: str = 'yolov8n.pt', 
        confidence: float = 0.3, 
        img_size: int = 640,
        output_dir: str = 'outputs'
    ):
        """
        Initialize YOLO detector with configurable parameters
        
        Args:
            model_path: Path to YOLO model
            confidence: Confidence threshold
            img_size: Inference image size
            output_dir: Directory to save outputs
        """
        self.logger = self._setup_logger()
        
        # Create output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load model
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.logger.info(f"Loaded YOLO model: {model_path}")
        except Exception as e:
            self.logger.error(f"Model loading failed: {e}")
            raise
        
        self.confidence = confidence
        self.img_size = img_size
        self.color_palette = ColorPalette()

    def _setup_logger(self) -> logging.Logger:
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        return logging.getLogger(__name__)

    def process_frame(
        self, 
        frame: np.ndarray
    ) -> Tuple[np.ndarray, Dict[str, int]]:
        """
        Detect and annotate objects in a single frame
        
        Args:
            frame: Input image frame
        
        Returns:
            Annotated frame and detection counts
        """
        # Perform detection
        results = self.model(frame, imgsz=self.img_size, conf=self.confidence)
        
        # Initialize detection tracking
        detections: Dict[str, int] = {}
        
        # Process each detection
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]
                conf = float(box.conf[0])
                
                # Count detections
                detections[label] = detections.get(label, 0) + 1
                
                # Get color for this class
                color = self.color_palette.get_color(cls)
                
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Add label with confidence
                text = f"{label} {conf:.2f}"
                cv2.putText(
                    frame, text, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                )
        
        return frame, detections

    def process_image(self, image_path: str):
        """Process a single image"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not read image")
            
            # Detect objects
            annotated_image, detections = self.process_frame(image)
            
            # Save output
            output_filename = self.output_dir / f"{Path(image_path).stem}_detected.jpg"
            cv2.imwrite(str(output_filename), annotated_image)
            
            self.logger.info(f"Processed image: {output_filename}")
            self.logger.info(f"Detected objects: {detections}")
            
            # Optional: Display image
            cv2.imshow('Object Detection', annotated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        except Exception as e:
            self.logger.error(f"Image processing error: {e}")

    # def process_video(self, source: Union[str, int]):
    #     """
    #     Process video from file or camera
        
    #     Args:
    #         source: Video file path or camera index
    #     """
    #     try:
    #         # Open video capture
    #         cap = cv2.VideoCapture(source)
    #         if not cap.isOpened():
    #             raise ValueError("Could not open video source")
            
    #         # Video properties
    #         frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #         frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #         fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)
            
    #         # Output video writer (if not webcam)
    #         writer: Optional[cv2.VideoWriter] = None
    #         if not isinstance(source, int):
    #             output_file = self.output_dir / f"{Path(source).stem}_detected.mp4"
    #             writer = cv2.VideoWriter(
    #                 str(output_file), 
    #                 cv2.VideoWriter_fourcc(*'mp4v'), 
    #                 fps, 
    #                 (frame_width, frame_height)
    #             )
    #             self.logger.info(f"Output video: {output_file}")
            
    #         # Performance tracking
    #         frame_count, total_time = 0, 0
            
    #         while True:
    #             ret, frame = cap.read()
    #             if not ret:
    #                 break
                
    #             # Time the detection process
    #             start_time = time.time()
    #             annotated_frame, detections = self.process_frame(frame)
    #             process_time = time.time() - start_time
                
    #             # Update performance metrics
    #             frame_count += 1
    #             total_time += process_time
                
    #             # Add FPS to frame
    #             fps_current = 1 / (process_time or 1e-9)
    #             cv2.putText(
    #                 annotated_frame, 
    #                 f"FPS: {fps_current:.1f}", 
    #                 (10, 30), 
    #                 cv2.FONT_HERSHEY_SIMPLEX, 
    #                 1, (0, 255, 0), 2
    #             )
                
    #             # Display object counts
    #             y_offset = 70
    #             for obj, count in detections.items():
    #                 cv2.putText(
    #                     annotated_frame, 
    #                     f"{obj}: {count}", 
    #                     (10, y_offset), 
    #                     cv2.FONT_HERSHEY_SIMPLEX, 
    #                     0.6, (0, 255, 0), 2
    #                 )
    #                 y_offset += 25
                
    #             # Display and optionally write frame
    #             cv2.imshow('Object Detection', annotated_frame)
    #             if writer:
    #                 writer.write(annotated_frame)
                
    #             # Exit condition
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
            
    #         # Cleanup
    #         cap.release()
    #         if writer:
    #             writer.release()
    #         cv2.destroyAllWindows()
            
    #         # Performance summary
    #         avg_fps = frame_count / (total_time or 1e-9)
    #         self.logger.info(f"Processed {frame_count} frames")
    #         self.logger.info(f"Average FPS: {avg_fps:.2f}")
            
    #     except Exception as e:
    #         self.logger.error(f"Video processing error: {e}")

# -----------------------
    # def process_video(self, source: str):
    #     """
    #     Process video from file and save it to media/output-videos/
    #     """
    #     try:
    #         cap = cv2.VideoCapture(source)
    #         if not cap.isOpened():
    #             raise ValueError("❌ Could not open video source")

    #         frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #         frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #         fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)  # Ensure FPS is never 0

    #         # ✅ Ensure output directory is in MEDIA_ROOT
    #         output_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
    #         os.makedirs(output_dir, exist_ok=True)

    #         # ✅ Define processed video path
    #         output_file = os.path.join(output_dir, f"processed_{os.path.basename(source)}")

    #         self.logger.info(f"🔍 Saving Processed Video to: {output_file}")

    #         writer = cv2.VideoWriter(
    #             output_file,
    #             cv2.VideoWriter_fourcc(*'mp4v'),
    #             fps,
    #             (frame_width, frame_height)
    #         )

    #         if not writer.isOpened():
    #             self.logger.error(f"❌ Failed to open VideoWriter for: {output_file}")
    #             return None

    #         frame_count, total_time = 0, 0

    #         while True:
    #             ret, frame = cap.read()
    #             if not ret:
    #                 break

    #             start_time = time.time()
    #             annotated_frame, detections = self.process_frame(frame)
    #             process_time = time.time() - start_time

    #             frame_count += 1
    #             total_time += process_time

    #             fps_current = 1 / (process_time or 1e-9)
    #             cv2.putText(
    #                 annotated_frame,
    #                 f"FPS: {fps_current:.1f}",
    #                 (10, 30),
    #                 cv2.FONT_HERSHEY_SIMPLEX,
    #                 1, (0, 255, 0), 2
    #             )

    #             writer.write(annotated_frame)  # Save frame to output video

    #         cap.release()
    #         writer.release()

    #         if os.path.exists(output_file):
    #             self.logger.info(f"✅ Processed video saved at: {output_file}")
    #             return output_file
    #         else:
    #             self.logger.error(f"❌ Processed video NOT saved! Check VideoWriter settings.")
    #             return None

    #     except Exception as e:
    #         self.logger.error(f"❌ Video processing error: {e}")
    #         return None


    def process_video(self, source: str):
        """
        Process video from file, return output path using mp4v codec.
        """
        try:
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                raise ValueError("Could not open video source")

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)

            output_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
            os.makedirs(output_dir, exist_ok=True)

            base_name = os.path.splitext(os.path.basename(source))[0]
            output_file = os.path.join(output_dir, f"processed_{base_name}.mp4")

            # Use mp4v — universally available on all platforms
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

            if not writer.isOpened():
                raise ValueError("VideoWriter failed to open")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                annotated_frame, _ = self.process_frame(frame)
                writer.write(annotated_frame)

            cap.release()
            writer.release()

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                self.logger.info(f"Processed video saved: {output_file}")
                return output_file
            else:
                self.logger.error("Processed video not saved")
                return None

        except Exception as e:
            self.logger.error(f"Video processing error: {e}")
            return None



def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Advanced YOLO Object Detection')
    parser.add_argument(
        '-i', '--input', 
        required=True, 
        help='Path to input image/video or camera index'
    )
    parser.add_argument(
        '-c', '--confidence', 
        type=float, 
        default=0.3, 
        help='Minimum confidence threshold'
    )
    parser.add_argument(
        '-m', '--model', 
        default='yolov8n.pt', 
        help='YOLO model path'
    )
    parser.add_argument(
        '-s', '--size', 
        type=int, 
        default=640, 
        help='Inference image size'
    )
    parser.add_argument(
        '-o', '--output', 
        default='outputs', 
        help='Output directory'
    )
    return parser.parse_args()

def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Initialize detector
    detector = YOLODetector(
        model_path=args.model,
        confidence=args.confidence,
        img_size=args.size,
        output_dir=args.output
    )
    
    # Determine input type
    input_path = args.input
    if input_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        detector.process_image(input_path)
    else:
        detector.process_video(input_path)

if __name__ == "__main__":
    main()

