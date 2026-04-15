content = open('vision/templates/dashboard.html', encoding='utf-8').read()

old = """                        var detectionInterval = null;

                        function startDetection() {
                            var btn = document.getElementById("start-detection-btn");
                            btn.innerText = "Stop Detection";
                            btn.setAttribute("onclick", "stopDetection()");

                            detectionInterval = setInterval(function() {
                                var video = document.getElementById("webcam-video");
                                if (!video || !video.srcObject) return;

                                var canvas = document.createElement('canvas');
                                canvas.width = video.videoWidth || 640;
                                canvas.height = video.videoHeight || 480;
                                canvas.getContext('2d').drawImage(video, 0, 0);

                                canvas.toBlob(function(blob) {
                                    var reader = new FileReader();
                                    reader.onloadend = function() {
                                        var base64 = reader.result.split(',')[1];
                                        fetch("{% url 'upload_image' %}", {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/x-www-form-urlencoded',
                                                'X-CSRFToken': document.querySelector('#image-upload-form [name=csrfmiddlewaretoken]').value
                                            },
                                            body: new URLSearchParams({ webcam_base64: base64 })
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
                                        })
                                        .catch(e => console.error('Detection error:', e));
                                    };
                                    reader.readAsDataURL(blob);
                                }, 'image/jpeg', 0.8);
                            }, 3000); // detect every 3 seconds
                        }

                        function stopDetection() {
                            if (detectionInterval) {
                                clearInterval(detectionInterval);
                                detectionInterval = null;
                            }
                            var btn = document.getElementById("start-detection-btn");
                            btn.innerText = "Start Detection";
                            btn.setAttribute("onclick", "startDetection()");
                        }"""

new = """                        var detectionInterval = null;

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

if old in content:
    content = content.replace(old, new)
    print("Detection fixed - now sends frame as FormData file")
else:
    print("FAILED - pattern not found")
    # debug
    idx = content.find('detectionInterval = null')
    print("detectionInterval found at:", idx)

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("done")
