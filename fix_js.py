f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# Find the broken script block and replace entirely
old = c[c.find('                    <script>\r\n                        // Function to handle video upload'):c.find('                    </script>\r\n\r\n\r\n                </div>\r\n            </div>')+len('                    </script>')]

new = """                    <script>
                        var webcamStream = null;

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
                                var webcamVideo = document.getElementById('webcam-video');
                                webcamVideo.srcObject = stream;
                                webcamVideo.style.display = 'block';
                                document.getElementById('webcam-buttons').style.display = 'inline-block';
                            })
                            .catch(function(err) {
                                alert('Cannot access webcam: ' + err.message);
                            });
                        }

                        function stopWebcam() {
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(function(track) { track.stop(); });
                                webcamStream = null;
                            }
                            var webcamVideo = document.getElementById('webcam-video');
                            if (webcamVideo) { webcamVideo.srcObject = null; webcamVideo.style.display = 'none'; }
                            document.getElementById('webcam-feed').src = '';
                            document.getElementById('webcam-buttons').style.display = 'none';
                        }

                        function startDetection() {
                            fetch('/start_detection/').then(function() {
                                var btn = document.getElementById('start-detection-btn');
                                btn.innerText = 'Stop Detection';
                                btn.setAttribute('onclick', 'stopDetection()');
                            });
                        }

                        function stopDetection() {
                            fetch('/stop_detection/').then(function() {
                                var btn = document.getElementById('start-detection-btn');
                                btn.innerText = 'Start Detection';
                                btn.setAttribute('onclick', 'startDetection()');
                            });
                        }

                        function takeScreenshot() {
                            var videoElement = document.getElementById('webcam-video');
                            if (!videoElement || !videoElement.srcObject) {
                                alert('Please open webcam first.');
                                return;
                            }
                            var canvas = document.getElementById('screenshot-canvas');
                            var context = canvas.getContext('2d');
                            canvas.width = videoElement.videoWidth || 640;
                            canvas.height = videoElement.videoHeight || 480;
                            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
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

if old in c:
    c = c.replace(old, new)
    print("JS section replaced successfully")
else:
    print("Pattern not found, trying alternative approach")
    # Find by markers
    start_marker = '                    <script>\r\n                        // Function to handle video upload'
    end_marker = '                    </script>\r\n\r\n\r\n                </div>\r\n            </div>'
    si = c.find(start_marker)
    ei = c.find(end_marker)
    if si >= 0 and ei >= 0:
        c = c[:si] + new + '\r\n\r\n\r\n                </div>\r\n            </div>' + c[ei+len(end_marker):]
        print("Alternative replacement done")
    else:
        print("FAILED - markers not found")
        print("start:", si, "end:", ei)

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("File saved")
