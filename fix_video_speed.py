content = open('vision/views.py', encoding='utf-8').read()

old = """            # Process video frame by frame using Roboflow API
            cap = cv2.VideoCapture(uploaded_video_path)
            if not cap.isOpened():
                return JsonResponse({'status': 'error', 'message': 'Cannot open video file'})

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            output_videos_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
            os.makedirs(output_videos_dir, exist_ok=True)
            output_path = os.path.join(output_videos_dir, 'detected_' + safe_filename.replace('.mp4', '') + '.mp4')

            writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

            # Process every Nth frame to save time (process 1 in 5 frames)
            frame_skip = max(1, fps // 5)
            frame_count = 0
            last_annotated = None

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1

                if frame_count % frame_skip == 0:
                    # Send frame to Roboflow
                    _, buf = cv2.imencode('.jpg', frame)
                    import base64
                    b64 = base64.b64encode(buf).decode('utf-8')
                    try:
                        resp = http_requests.post(
                            f"https://detect.roboflow.com/{ROBOFLOW_MODEL}",
                            params={"api_key": ROBOFLOW_API_KEY, "confidence": 40},
                            data=b64,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            timeout=10
                        )
                        preds = resp.json().get('predictions', [])
                        annotated = frame.copy()
                        for pred in preds:
                            label = pred['class']
                            conf = pred['confidence']
                            x, y, w, h = int(pred['x']), int(pred['y']), int(pred['width']), int(pred['height'])
                            x1, y1 = max(0, x - w//2), max(0, y - h//2)
                            x2, y2 = min(frame_width, x + w//2), min(frame_height, y + h//2)
                            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(annotated, f"{label} {conf:.0%}", (x1, y1-5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        last_annotated = annotated
                    except Exception:
                        last_annotated = frame

                writer.write(last_annotated if last_annotated is not None else frame)

            cap.release()
            writer.release()"""

new = """            # Process video - detect once per second, reuse boxes for all frames
            cap = cv2.VideoCapture(uploaded_video_path)
            if not cap.isOpened():
                return JsonResponse({'status': 'error', 'message': 'Cannot open video file'})

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)

            # Resize to 640px wide for faster processing
            scale = min(1.0, 640 / frame_width)
            out_w = int(frame_width * scale)
            out_h = int(frame_height * scale)

            output_videos_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
            os.makedirs(output_videos_dir, exist_ok=True)
            output_path = os.path.join(output_videos_dir, 'detected_' + safe_filename.replace('.mp4', '') + '.mp4')

            writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (out_w, out_h))

            # Call Roboflow only once per second
            detect_every = max(1, fps)
            frame_count = 0
            last_preds = []
            import base64

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1

                # Resize frame
                if scale < 1.0:
                    frame = cv2.resize(frame, (out_w, out_h))

                if frame_count % detect_every == 1:
                    # Detect on this frame
                    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                    b64 = base64.b64encode(buf).decode('utf-8')
                    try:
                        resp = http_requests.post(
                            f"https://detect.roboflow.com/{ROBOFLOW_MODEL}",
                            params={"api_key": ROBOFLOW_API_KEY, "confidence": 40},
                            data=b64,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            timeout=8
                        )
                        last_preds = resp.json().get('predictions', [])
                    except Exception:
                        last_preds = []

                # Draw last known boxes on every frame
                annotated = frame.copy()
                for pred in last_preds:
                    label = pred['class']
                    conf = pred['confidence']
                    x, y, w, h = int(pred['x']*scale), int(pred['y']*scale), int(pred['width']*scale), int(pred['height']*scale)
                    x1, y1 = max(0, x - w//2), max(0, y - h//2)
                    x2, y2 = min(out_w, x + w//2), min(out_h, y + h//2)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated, f"{label} {conf:.0%}", (x1, max(0,y1-5)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                writer.write(annotated)

            cap.release()
            writer.release()"""

if old in content:
    content = content.replace(old, new)
    print("Video processing optimized")
else:
    print("FAILED")

open('vision/views.py', 'w', encoding='utf-8').write(content)
print("done")
