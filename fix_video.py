content = open('vision/views.py', encoding='utf-8').read()

old = """def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        try:
            video_file = request.FILES['video']

            # \u2705 Step 1: Save the uploaded video in /media/uploads/
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            safe_filename = video_file.name.replace(" ", "_")
            uploaded_video_path = os.path.join(upload_dir, safe_filename)

            with default_storage.open(uploaded_video_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            print("\u2705 Video uploaded successfully at:", uploaded_video_path)

            # \u2705 Step 2: Process the video
            processed_video_path = get_detector().process_video(uploaded_video_path)
            print("\u2705 Processed video path:", processed_video_path)

            # \u2705 Step 3: Ensure processed video exists
            if processed_video_path and os.path.exists(processed_video_path):
                # \u2705 Move processed video to media/output-videos/
                output_videos_dir = os.path.join(settings.MEDIA_ROOT, 'output-videos')
                os.makedirs(output_videos_dir, exist_ok=True)

                final_processed_video_path = os.path.join(output_videos_dir, os.path.basename(processed_video_path))
                os.rename(processed_video_path, final_processed_video_path)  # Move the file

                # \u2705 Generate the correct video URL
                processed_video_url = request.build_absolute_uri(
                    settings.MEDIA_URL + 'output-videos/' + urllib.parse.quote(os.path.basename(final_processed_video_path))
                )

                print("\u2705 Processed Video URL:", processed_video_url)
                return JsonResponse({'status': 'success', 'processed_video_url': processed_video_url})

            else:
                print("\u274c Error: Processed video path is None or does not exist")
                return JsonResponse({'status': 'error', 'message': 'Failed to process video'})

        except Exception as e:
            print("\u274c Exception:", str(e))
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})"""

new = """def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        try:
            video_file = request.FILES['video']

            # Save uploaded video
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            safe_filename = video_file.name.replace(" ", "_")
            uploaded_video_path = os.path.join(upload_dir, safe_filename)
            with open(uploaded_video_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # Process video frame by frame using Roboflow API
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
            writer.release()

            if os.path.exists(output_path):
                processed_video_url = request.build_absolute_uri(
                    settings.MEDIA_URL + 'output-videos/' + urllib.parse.quote(os.path.basename(output_path))
                )
                return JsonResponse({'status': 'success', 'processed_video_url': processed_video_url})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to save processed video'})

        except Exception as e:
            import traceback
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}', 'detail': traceback.format_exc()})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})"""

if old in content:
    content = content.replace(old, new)
    print("upload_video fixed")
else:
    print("FAILED - pattern not found")
    idx = content.find('def upload_video')
    print("upload_video at:", idx)

open('vision/views.py', 'w', encoding='utf-8').write(content)
print("done")
