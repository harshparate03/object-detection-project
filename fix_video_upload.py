with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def upload_video(request):

    if request.method == 'POST' and request.FILES.get('video'):

        try:

            video_file = request.FILES['video']

            # バ. Step 1: Save the uploaded video in /media/uploads/
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            safe_filename = video_file.name.replace(" ", "_")
            uploaded_video_path = os.path.join(upload_dir, safe_filename)

            with default_storage.open(uploaded_video_path, 'wb') as f:
                for chunk in video_file.chunks():

                    f.write(chunk)

            print("バ. Video uploaded successfully at:", uploaded_video_path)

            # バ. Step 2: Process the video
            processed_video_path = get_detector().process_video(uploaded_video_path)
            print("バ. Processed video path:", processed_video_path)

            # バ. Step 3: Ensure processed video exists
            if processed_video_path and os.path.exists(processed_video_path):
                # バ. Move processed video to media/output-videos/
                output_videos_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
                os.makedirs(output_videos_dir, exist_ok=True)

                final_processed_video_path = os.path.join(output_videos_dir, os.path.basename(processed_video_path))
                os.rename(processed_video_path, final_processed_video_path)  # Move the file


                # バ. Generate the correct video URL
                processed_video_url = request.build_absolute_uri(
                    settings.MEDIA_URL + 'output-videos/' + urllib.parse.quote(os.path.basename(final_processed_video_path))
                )


                print("バ. Processed Video URL:", processed_video_url)
                return JsonResponse({'status': 'success', 'processed_video_url': processed_video_url})

            else:
                print("❌ Error: Processed video path is None or does not exist")
                return JsonResponse({'status': 'error', 'message': 'Failed to process video'})

        except Exception as e:
            print("❌ Exception:", str(e))
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})'''

new = '''def upload_video(request):
    """
    Process video by sampling frames via Roboflow API (lightweight, no local YOLO).
    Annotates sampled frames and returns processed video as base64.
    """
    if request.method == 'POST' and request.FILES.get('video'):
        try:
            import base64
            import tempfile

            video_file = request.FILES['video']

            # Save uploaded video to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            cap = cv2.VideoCapture(tmp_path)
            if not cap.isOpened():
                os.unlink(tmp_path)
                return JsonResponse({'status': 'error', 'message': 'Could not read video file'})

            frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps          = int(cap.get(cv2.CAP_PROP_FPS) or 25)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Sample every Nth frame to stay within Render's timeout (300s)
            # Process max 60 frames to keep response time under 60s
            max_frames = 60
            step = max(1, total_frames // max_frames)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as out_tmp:
                out_path = out_tmp.name

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))

            frame_idx = 0
            last_annotated = None
            all_detections = {}

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % step == 0:
                    # Send frame to Roboflow
                    _, buf = cv2.imencode('.jpg', frame)
                    img_b64 = base64.b64encode(buf).decode('utf-8')
                    try:
                        resp = http_requests.post(
                            f"https://detect.roboflow.com/{ROBOFLOW_MODEL}",
                            params={"api_key": ROBOFLOW_API_KEY, "confidence": 40, "overlap": 30},
                            data=img_b64,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            timeout=10
                        )
                        preds = resp.json().get('predictions', [])
                        annotated = frame.copy()
                        for pred in preds:
                            label = pred['class']
                            conf  = pred['confidence']
                            x, y, w, h = int(pred['x']), int(pred['y']), int(pred['width']), int(pred['height'])
                            x1, y1 = max(0, x - w//2), max(0, y - h//2)
                            x2, y2 = min(frame_width, x + w//2), min(frame_height, y + h//2)
                            color = COLORS[hash(label) % len(COLORS)]
                            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
                            text = f"{label} {conf:.0%}"
                            cv2.putText(annotated, text, (x1+2, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                            all_detections[label] = all_detections.get(label, 0) + 1
                        last_annotated = annotated
                    except Exception:
                        last_annotated = frame
                else:
                    # Reuse last annotated frame for non-sampled frames
                    last_annotated = last_annotated if last_annotated is not None else frame

                writer.write(last_annotated)
                frame_idx += 1

            cap.release()
            writer.release()
            os.unlink(tmp_path)

            # Read processed video and return as base64 data URL
            with open(out_path, 'rb') as f:
                video_b64 = base64.b64encode(f.read()).decode('utf-8')
            os.unlink(out_path)

            detected_objects = [{"label": k, "count": v} for k, v in all_detections.items()]
            return JsonResponse({
                'status': 'success',
                'processed_video_url': f'data:video/mp4;base64,{video_b64}',
                'detected_objects': detected_objects
            })

        except Exception as e:
            logger.exception("Video processing error")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})'''

if 'def upload_video(request):' in content:
    # Find and replace the entire upload_video function
    start = content.find('def upload_video(request):')
    # Find the next top-level def after upload_video
    next_def = content.find('\ndef ', start + 10)
    content = content[:start] + new + '\n\n' + content[next_def+1:]
    print("upload_video replaced successfully")
else:
    print("ERROR: upload_video not found")

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
