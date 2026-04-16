with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def upload_video(request):
    """
    Process video: sample 20 frames via Roboflow, annotate, save to disk, return URL.
    Keeps processing fast and avoids base64 bloat.
    """
    if request.method == 'POST' and request.FILES.get('video'):
        try:
            import base64 as _b64
            import tempfile
            import uuid

            video_file = request.FILES['video']

            # Reject files > 20MB
            if video_file.size > 20 * 1024 * 1024:
                return JsonResponse({'status': 'error', 'message': 'Video too large. Max 20MB.'})

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
            fps          = max(1, int(cap.get(cv2.CAP_PROP_FPS) or 25))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Only annotate 20 frames max — fast & avoids timeout
            max_api_calls = 20
            step = max(1, total_frames // max_api_calls)

            # Output to media/output-videos/
            out_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
            os.makedirs(out_dir, exist_ok=True)
            out_filename = f"processed_{uuid.uuid4().hex[:8]}.mp4"
            out_path = os.path.join(out_dir, out_filename)

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
                    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                    img_b64 = _b64.b64encode(buf).decode('utf-8')
                    try:
                        resp = http_requests.post(
                            f"https://detect.roboflow.com/{ROBOFLOW_MODEL}",
                            params={"api_key": ROBOFLOW_API_KEY, "confidence": 40, "overlap": 30},
                            data=img_b64,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            timeout=8
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
                    last_annotated = last_annotated if last_annotated is not None else frame

                writer.write(last_annotated)
                frame_idx += 1

            cap.release()
            writer.release()
            os.unlink(tmp_path)

            if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                return JsonResponse({'status': 'error', 'message': 'Failed to write output video'})

            video_url = request.build_absolute_uri(
                settings.MEDIA_URL + 'output-videos/' + out_filename
            )
            detected_objects = [{"label": k, "count": v} for k, v in all_detections.items()]
            return JsonResponse({
                'status': 'success',
                'processed_video_url': video_url,
                'detected_objects': detected_objects
            })

        except Exception as e:
            logger.exception("Video processing error")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})'''

new = '''def upload_video(request):
    """
    Process video: sample 20 frames via Roboflow, return annotated frames as
    a GIF-style slideshow encoded as base64 JPEG frames in JSON.
    Avoids disk storage entirely — works on Render ephemeral filesystem.
    """
    if request.method == 'POST' and request.FILES.get('video'):
        try:
            import base64 as _b64
            import tempfile

            video_file = request.FILES['video']

            if video_file.size > 50 * 1024 * 1024:
                return JsonResponse({'status': 'error', 'message': 'Video too large. Max 50MB.'})

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                for chunk in video_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            cap = cv2.VideoCapture(tmp_path)
            if not cap.isOpened():
                os.unlink(tmp_path)
                return JsonResponse({'status': 'error', 'message': 'Could not read video file'})

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps          = max(1, int(cap.get(cv2.CAP_PROP_FPS) or 25))

            # Sample exactly 20 evenly-spaced frames
            max_frames = 20
            step = max(1, total_frames // max_frames)

            annotated_frames = []
            all_detections = {}
            frame_idx = 0

            while len(annotated_frames) < max_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if not ret:
                    break

                # Resize to max 640px wide for speed
                h, w = frame.shape[:2]
                if w > 640:
                    scale = 640 / w
                    frame = cv2.resize(frame, (640, int(h * scale)))
                    frame_width, frame_height = 640, int(h * scale)

                _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
                img_b64 = _b64.b64encode(buf).decode('utf-8')

                try:
                    resp = http_requests.post(
                        f"https://detect.roboflow.com/{ROBOFLOW_MODEL}",
                        params={"api_key": ROBOFLOW_API_KEY, "confidence": 40, "overlap": 30},
                        data=img_b64,
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        timeout=8
                    )
                    preds = resp.json().get('predictions', [])
                    annotated = frame.copy()
                    for pred in preds:
                        label = pred['class']
                        conf  = pred['confidence']
                        x, y, w2, h2 = int(pred['x']), int(pred['y']), int(pred['width']), int(pred['height'])
                        x1, y1 = max(0, x - w2//2), max(0, y - h2//2)
                        x2, y2 = min(frame_width, x + w2//2), min(frame_height, y + h2//2)
                        color = COLORS[hash(label) % len(COLORS)]
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
                        text = f"{label} {conf:.0%}"
                        cv2.putText(annotated, text, (x1+2, max(y1-4,10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                        all_detections[label] = all_detections.get(label, 0) + 1
                except Exception:
                    annotated = frame

                _, out_buf = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
                annotated_frames.append('data:image/jpeg;base64,' + _b64.b64encode(out_buf).decode('utf-8'))

                frame_idx += step

            cap.release()
            os.unlink(tmp_path)

            detected_objects = [{"label": k, "count": v} for k, v in all_detections.items()]
            return JsonResponse({
                'status': 'success',
                'frames': annotated_frames,
                'fps': min(fps, 10),
                'detected_objects': detected_objects
            })

        except Exception as e:
            logger.exception("Video processing error")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})'''

if old in content:
    content = content.replace(old, new)
    print("Replaced successfully")
else:
    # fallback: find and replace by function boundary
    start = content.find('def upload_video(request):')
    next_def = content.find('\ndef ', start + 10)
    content = content[:start] + new + '\n\n' + content[next_def+1:]
    print("Replaced via boundary")

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
