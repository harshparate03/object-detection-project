content = open('vision/templates/dashboard.html', encoding='utf-8').read()

# Replace webcam video + feed elements with a single canvas-based display
# Current: has both webcam-video and webcam-feed (img) elements
# Fix: use webcam-video for live feed, overlay canvas on top for detection boxes

# 1. Fix the webcam container HTML - add canvas overlay
old1 = """                    <div align="center">
                        <video id="webcam-video" width="640" height="480" autoplay
                            style="display: none; border: 1px solid black; margin-top: 20px; transform: scaleX(-1);"></video>
                    </div>

                    <div id="webcam-buttons" style="text-align: center; width: 100%; display: none;">
                        <button class="btn-default btn-large" onclick="takeScreenshot()">Take Screenshot</button>
                        <button class="btn-default btn-large" id="start-detection-btn" onclick="startDetection()">Start
                            Detection</button>
                        <button class="btn-default btn-large" onclick="stopWebcam()" id="stop-webcam-btn">Stop
                            Webcam</button>
                    </div>

                    <img id="webcam-feed" src="" style="width: 100%; display: block;">
                    <canvas id="screenshot-canvas" style="display: none;"></canvas>"""

new1 = """                    <div id="webcam-container" style="display:none; text-align:center; margin-top:20px; position:relative; display:none;">
                        <div style="position:relative; display:inline-block;">
                            <video id="webcam-video" width="640" height="480" autoplay muted
                                style="border: 2px solid white; border-radius: 10px; display:block;"></video>
                            <canvas id="detection-overlay" width="640" height="480"
                                style="position:absolute; top:0; left:0; pointer-events:none;"></canvas>
                        </div>
                        <div id="webcam-buttons" style="text-align: center; width: 100%; margin-top:10px;">
                            <button class="btn-default btn-large" onclick="takeScreenshot()">Take Screenshot</button>
                            <button class="btn-default btn-large" id="start-detection-btn" onclick="startDetection()">Start Detection</button>
                            <button class="btn-default btn-large" onclick="stopWebcam()" id="stop-webcam-btn">Stop Webcam</button>
                        </div>
                    </div>
                    <canvas id="screenshot-canvas" style="display: none;"></canvas>
                    <img id="webcam-feed" src="" style="display:none;">"""

if old1 in content:
    content = content.replace(old1, new1)
    print("FIX 1: webcam HTML restructured")
else:
    print("FIX 1 FAILED")

# 2. Fix openWebcam to show webcam-container
old2 = """                        var webcamStream = null;

                        function openWebcam() {
                            clearAllPanels();
                            // Use browser getUserMedia API - works locally and on Render
                            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                                navigator.mediaDevices.getUserMedia({ video: true })
                                .then(function(stream) {
                                    webcamStream = stream;
                                    var webcamVideo = document.getElementById("webcam-video");
                                    webcamVideo.srcObject = stream;
                                    webcamVideo.style.display = "block";
                                    document.getElementById("webcam-buttons").style.display = "inline-block";
                                })
                                .catch(function(err) {
                                    alert("Cannot access webcam: " + err.message);
                                });
                            } else {
                                alert("Webcam not supported in this browser.");
                            }
                        }"""

new2 = """                        var webcamStream = null;

                        function openWebcam() {
                            clearAllPanels();
                            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                                navigator.mediaDevices.getUserMedia({ video: true })
                                .then(function(stream) {
                                    webcamStream = stream;
                                    var webcamVideo = document.getElementById("webcam-video");
                                    webcamVideo.srcObject = stream;
                                    document.getElementById("webcam-container").style.display = "block";
                                })
                                .catch(function(err) {
                                    alert("Cannot access webcam: " + err.message);
                                });
                            } else {
                                alert("Webcam not supported in this browser.");
                            }
                        }"""

if old2 in content:
    content = content.replace(old2, new2)
    print("FIX 2: openWebcam updated")
else:
    print("FIX 2 FAILED")

# 3. Fix stopWebcam to hide webcam-container
old3 = """                        function stopWebcam() {
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(track => track.stop());
                                webcamStream = null;
                            }
                            var webcamVideo = document.getElementById("webcam-video");
                            webcamVideo.srcObject = null;
                            webcamVideo.style.display = "none";
                            document.getElementById("webcam-feed").src = "";
                            document.getElementById("webcam-buttons").style.display = "none";
                        }"""

new3 = """                        function stopWebcam() {
                            stopDetection();
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(track => track.stop());
                                webcamStream = null;
                            }
                            var webcamVideo = document.getElementById("webcam-video");
                            webcamVideo.srcObject = null;
                            document.getElementById("webcam-container").style.display = "none";
                            // clear detection overlay
                            var overlay = document.getElementById("detection-overlay");
                            overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                        }"""

if old3 in content:
    content = content.replace(old3, new3)
    print("FIX 3: stopWebcam updated")
else:
    print("FIX 3 FAILED")

# 4. Fix startDetection to draw boxes on overlay canvas instead of separate image
old4 = """                        var detectionInterval = null;

                        function startDetection() {
                            var video = document.getElementById("webcam-video");
                            if (!video || !video.srcObject) {
                                alert("Please open webcam first.");
                                return;
                            }
                            var btn = document.getElementById("start-detection-btn");
                            btn.innerText = "Stop Detection";
                            btn.setAttribute("onclick", "stopDetection()");

                            function detectFrame() {
                                if (!detectionInterval) return;
                                var canvas = document.createElement('canvas');
                                canvas.width = video.videoWidth || 640;
                                canvas.height = video.videoHeight || 480;
                                canvas.getContext('2d').drawImage(video, 0, 0);

                                canvas.toBlob(function(blob) {
                                    var formData = new FormData();
                                    formData.append('image', blob, 'webcam_frame.jpg');
                                    fetch("{% url 'upload_image' %}", {
                                        method: 'POST',
                                        headers: {
                                            'X-CSRFToken': document.querySelector('#image-upload-form [name=csrfmiddlewaretoken]').value
                                        },
                                        body: formData
                                    })
                                    .then(r => r.json())
                                    .then(data => {
                                        if (data.status === 'success') {
                                            document.getElementById('annotated-image').src = data.annotated_image_url;
                                            document.getElementById('annotated-image-container').style.display = 'block';
                                            var list = document.getElementById('detection-list');
                                            list.innerHTML = '';
                                            data.detected_objects.forEach(obj => {
                                                var li = document.createElement('li');
                                                li.textContent = obj.label + ': ' + obj.count;
                                                list.appendChild(li);
                                            });
                                            document.getElementById('detection-results').style.display = 'block';
                                        }
                                        // schedule next frame after response
                                        if (detectionInterval) setTimeout(detectFrame, 2000);
                                    })
                                    .catch(e => {
                                        console.error('Detection error:', e);
                                        if (detectionInterval) setTimeout(detectFrame, 2000);
                                    });
                                }, 'image/jpeg', 0.8);
                            }

                            detectionInterval = true;
                            detectFrame();
                        }

                        function stopDetection() {
                            detectionInterval = null;
                            var btn = document.getElementById("start-detection-btn");
                            btn.innerText = "Start Detection";
                            btn.setAttribute("onclick", "startDetection()");
                        }"""

new4 = """                        var detectionInterval = null;

                        function startDetection() {
                            var video = document.getElementById("webcam-video");
                            if (!video || !video.srcObject) {
                                alert("Please open webcam first.");
                                return;
                            }
                            var btn = document.getElementById("start-detection-btn");
                            btn.innerText = "Stop Detection";
                            btn.setAttribute("onclick", "stopDetection()");

                            function detectFrame() {
                                if (!detectionInterval) return;
                                var canvas = document.createElement('canvas');
                                canvas.width = video.videoWidth || 640;
                                canvas.height = video.videoHeight || 480;
                                canvas.getContext('2d').drawImage(video, 0, 0);

                                canvas.toBlob(function(blob) {
                                    var formData = new FormData();
                                    formData.append('image', blob, 'webcam_frame.jpg');
                                    fetch("{% url 'upload_image' %}", {
                                        method: 'POST',
                                        headers: {
                                            'X-CSRFToken': document.querySelector('#image-upload-form [name=csrfmiddlewaretoken]').value
                                        },
                                        body: formData
                                    })
                                    .then(r => r.json())
                                    .then(data => {
                                        if (data.status === 'success') {
                                            // Draw annotated frame ON the overlay canvas (same window as webcam)
                                            var overlay = document.getElementById("detection-overlay");
                                            var ctx = overlay.getContext('2d');
                                            var img = new Image();
                                            img.onload = function() {
                                                overlay.width = video.videoWidth || 640;
                                                overlay.height = video.videoHeight || 480;
                                                ctx.drawImage(img, 0, 0, overlay.width, overlay.height);
                                            };
                                            img.src = data.annotated_image_url;

                                            // Update detection list
                                            var list = document.getElementById('detection-list');
                                            list.innerHTML = '';
                                            data.detected_objects.forEach(obj => {
                                                var li = document.createElement('li');
                                                li.textContent = obj.label + ': ' + obj.count;
                                                list.appendChild(li);
                                            });
                                            document.getElementById('detection-results').style.display = 'block';
                                        }
                                        if (detectionInterval) setTimeout(detectFrame, 2000);
                                    })
                                    .catch(e => {
                                        console.error('Detection error:', e);
                                        if (detectionInterval) setTimeout(detectFrame, 2000);
                                    });
                                }, 'image/jpeg', 0.8);
                            }

                            detectionInterval = true;
                            detectFrame();
                        }

                        function stopDetection() {
                            detectionInterval = null;
                            var btn = document.getElementById("start-detection-btn");
                            if (btn) {
                                btn.innerText = "Start Detection";
                                btn.setAttribute("onclick", "startDetection()");
                            }
                            // Clear overlay
                            var overlay = document.getElementById("detection-overlay");
                            if (overlay) overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                        }"""

if old4 in content:
    content = content.replace(old4, new4)
    print("FIX 4: startDetection draws on overlay canvas")
else:
    print("FIX 4 FAILED")

# 5. Fix clearAllPanels to hide webcam-container instead of webcam-buttons
old5 = "            // Hide webcam panel\n            document.getElementById('webcam-feed').src = '';\n            document.getElementById('webcam-buttons').style.display = 'none';"
new5 = "            // Hide webcam panel\n            document.getElementById('webcam-container').style.display = 'none';\n            document.getElementById('webcam-feed').src = '';"

if old5 in content:
    content = content.replace(old5, new5)
    print("FIX 5: clearAllPanels updated for webcam-container")
else:
    print("FIX 5 FAILED")

# 6. Fix takeScreenshot to use webcam-video
old6 = """                        function takeScreenshot() {
                            let videoElement = document.getElementById("webcam-video");
                            let canvas = document.getElementById("screenshot-canvas");
                            let context = canvas.getContext("2d");

                            if (!videoElement || !videoElement.srcObject) {
                                alert("Webcam not started.");
                                return;
                            }"""
new6 = """                        function takeScreenshot() {
                            let videoElement = document.getElementById("webcam-video");
                            let canvas = document.getElementById("screenshot-canvas");
                            let context = canvas.getContext("2d");

                            if (!videoElement || !videoElement.srcObject) {
                                alert("Please open webcam first.");
                                return;
                            }"""

if old6 in content:
    content = content.replace(old6, new6)
    print("FIX 6: takeScreenshot updated")
else:
    print("FIX 6 SKIPPED")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("\nAll fixes applied.")
