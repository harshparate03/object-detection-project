f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# Find and replace the entire webcam JS block
i_start = c.find('                        var webcamStream = null;')
i_end = c.find('                    </script>', i_start) + len('                    </script>')

old_block = c[i_start:i_end]
print("Found block length:", len(old_block))

new_block = """                        var webcamStream = null;
                        var detectionActive = false;
                        var detectionTimer = null;

                        function getCsrfToken() {
                            var name = 'csrftoken';
                            var cookies = document.cookie.split(';');
                            for (var i = 0; i < cookies.length; i++) {
                                var c = cookies[i].trim();
                                if (c.startsWith(name + '=')) return decodeURIComponent(c.substring(name.length + 1));
                            }
                            var el = document.querySelector('[name=csrfmiddlewaretoken]');
                            return el ? el.value : '';
                        }

                        function openWebcam() {
                            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                                alert('Webcam not supported in this browser.');
                                return;
                            }
                            navigator.mediaDevices.getUserMedia({ video: true })
                            .then(function(stream) {
                                webcamStream = stream;
                                var video = document.getElementById('webcam-video');
                                video.srcObject = stream;
                                video.style.display = 'block';
                                // Keep overlay hidden until detection starts
                                document.getElementById('detection-overlay').style.display = 'none';
                                document.getElementById('webcam-buttons').style.display = 'inline-block';
                            })
                            .catch(function(err) {
                                alert('Cannot access webcam: ' + err.message);
                            });
                        }

                        function stopWebcam() {
                            // Stop detection first
                            stopDetection();
                            // Stop camera stream
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(function(t) { t.stop(); });
                                webcamStream = null;
                            }
                            var video = document.getElementById('webcam-video');
                            video.srcObject = null;
                            video.style.display = 'none';
                            document.getElementById('webcam-buttons').style.display = 'none';
                            document.getElementById('webcam-feed').src = '';
                        }

                        function startDetection() {
                            var video = document.getElementById('webcam-video');
                            if (!video || !video.srcObject) {
                                alert('Please open webcam first.');
                                return;
                            }
                            if (detectionActive) return;
                            detectionActive = true;

                            // Show overlay canvas on top of webcam
                            var overlay = document.getElementById('detection-overlay');
                            overlay.width = video.videoWidth || 640;
                            overlay.height = video.videoHeight || 480;
                            overlay.style.display = 'block';

                            // Update button
                            var btn = document.getElementById('start-detection-btn');
                            btn.innerText = 'Stop Detection';
                            btn.setAttribute('onclick', 'stopDetection()');

                            // Start detection loop
                            runDetection(video);
                        }

                        function stopDetection() {
                            detectionActive = false;

                            // Cancel any pending timer
                            if (detectionTimer) {
                                clearTimeout(detectionTimer);
                                detectionTimer = null;
                            }

                            // Hide overlay completely
                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) {
                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                                overlay.style.display = 'none';
                            }

                            // Hide detection results
                            var wr = document.getElementById('webcam-detection-results');
                            if (wr) wr.style.display = 'none';

                            // Reset button
                            var btn = document.getElementById('start-detection-btn');
                            if (btn) {
                                btn.innerText = 'Start Detection';
                                btn.setAttribute('onclick', 'startDetection()');
                            }
                        }

                        function runDetection(video) {
                            if (!detectionActive) return;

                            var canvas = document.createElement('canvas');
                            canvas.width = video.videoWidth || 640;
                            canvas.height = video.videoHeight || 480;
                            canvas.getContext('2d').drawImage(video, 0, 0);

                            canvas.toBlob(function(blob) {
                                if (!detectionActive) return; // check again after async
                                var formData = new FormData();
                                formData.append('image', blob, 'frame.jpg');
                                fetch("{% url 'upload_image' %}", {
                                    method: 'POST',
                                    headers: { 'X-CSRFToken': getCsrfToken() },
                                    body: formData
                                })
                                .then(function(r) { return r.json(); })
                                .then(function(data) {
                                    if (!detectionActive) return;
                                    if (data.status === 'success') {
                                        // Draw annotated frame on overlay
                                        var overlay = document.getElementById('detection-overlay');
                                        var img = new Image();
                                        img.onload = function() {
                                            if (detectionActive && overlay) {
                                                overlay.getContext('2d').drawImage(img, 0, 0, overlay.width, overlay.height);
                                            }
                                        };
                                        img.src = data.annotated_image_url;

                                        // Show detected objects below webcam
                                        var list = document.getElementById('webcam-detection-list');
                                        list.innerHTML = '';
                                        data.detected_objects.forEach(function(obj) {
                                            var li = document.createElement('li');
                                            li.textContent = obj.label + ': ' + obj.count;
                                            list.appendChild(li);
                                        });
                                        document.getElementById('webcam-detection-results').style.display = 'block';
                                    }
                                    // Schedule next detection
                                    if (detectionActive) {
                                        detectionTimer = setTimeout(function() { runDetection(video); }, 2000);
                                    }
                                })
                                .catch(function() {
                                    if (detectionActive) {
                                        detectionTimer = setTimeout(function() { runDetection(video); }, 2000);
                                    }
                                });
                            }, 'image/jpeg', 0.8);
                        }

                        function takeScreenshot() {
                            var video = document.getElementById('webcam-video');
                            if (!video || !video.srcObject) {
                                alert('Please open webcam first.');
                                return;
                            }
                            var canvas = document.getElementById('screenshot-canvas');
                            canvas.width = video.videoWidth || 640;
                            canvas.height = video.videoHeight || 480;
                            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                            canvas.toBlob(function(blob) {
                                var link = document.createElement('a');
                                link.href = URL.createObjectURL(blob);
                                link.download = 'screenshot.jpg';
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                            }, 'image/jpeg', 0.95);
                        }

                    </script>"""

c = c[:i_start] + new_block + c[i_end:]
open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("Complete webcam JS rewritten successfully")
