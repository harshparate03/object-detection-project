content = open('vision/templates/dashboard.html', encoding='utf-8').read()

# Fix 1: Replace all CSRF token reads with cookie-based method
# First add getCsrfToken function
old1 = "function clearAllPanels() {"
new1 = """function getCsrfToken() {
            var name = 'csrftoken';
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var c = cookies[i].trim();
                if (c.startsWith(name + '=')) return decodeURIComponent(c.substring(name.length + 1));
            }
            var el = document.querySelector('[name=csrfmiddlewaretoken]');
            return el ? el.value : '';
        }

        function clearAllPanels() {"""

if old1 in content:
    content = content.replace(old1, new1)
    print("FIX 1: getCsrfToken added")
else:
    # No clearAllPanels - add before image upload listener
    old1b = "    <script>\n        document.getElementById('image-upload').addEventListener"
    new1b = """    <script>
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
    </script>
    <script>
        document.getElementById('image-upload').addEventListener"""
    if old1b in content:
        content = content.replace(old1b, new1b)
        print("FIX 1: getCsrfToken added before image upload")
    else:
        print("FIX 1 FAILED")

# Fix 2: Replace all CSRF token reads
content = content.replace(
    "document.querySelector('#image-upload-form [name=csrfmiddlewaretoken]').value",
    "getCsrfToken()"
)
content = content.replace(
    "document.querySelector('[name=csrfmiddlewaretoken]').value",
    "getCsrfToken()"
)
content = content.replace(
    "'X-CSRFToken': '{{ csrf_token }}'",
    "'X-CSRFToken': getCsrfToken()"
)
print("FIX 2: All CSRF reads replaced with getCsrfToken()")

# Fix 3: Fix webcam stop - openWebcam uses getUserMedia
old3 = """                        function openWebcam() {
                            document.getElementById("webcam-feed").src = "/video_feed/";
                            document.getElementById("webcam-buttons").style.display = "inline-block"; // Show all buttons
                            document.getElementById("stop-webcam-btn").style.display = "inline-block"; // Show Stop Webcam immediately
                        }"""

new3 = """                        var webcamStream = null;

                        function openWebcam() {
                            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                                navigator.mediaDevices.getUserMedia({ video: true })
                                .then(function(stream) {
                                    webcamStream = stream;
                                    var webcamVideo = document.getElementById("webcam-video");
                                    webcamVideo.srcObject = stream;
                                    webcamVideo.style.display = "block";
                                    document.getElementById("webcam-buttons").style.display = "inline-block";
                                    document.getElementById("stop-webcam-btn").style.display = "inline-block";
                                })
                                .catch(function(err) {
                                    alert("Cannot access webcam: " + err.message);
                                });
                            } else {
                                alert("Webcam not supported in this browser.");
                            }
                        }"""

if old3 in content:
    content = content.replace(old3, new3)
    print("FIX 3: openWebcam fixed with getUserMedia")
else:
    print("FIX 3 FAILED")

# Fix 4: Fix stopWebcam to properly stop getUserMedia stream
old4 = """                        function stopWebcam() {
                            fetch('/stop_webcam/').then(response => {
                                console.log("Webcam stopped");
                                document.getElementById("webcam-feed").src = "";
                                document.getElementById("webcam-buttons").style.display = "none"; // Hide all buttons after stopping
                            });
                        }"""

new4 = """                        function stopWebcam() {
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(function(track) { track.stop(); });
                                webcamStream = null;
                            }
                            var webcamVideo = document.getElementById("webcam-video");
                            webcamVideo.srcObject = null;
                            webcamVideo.style.display = "none";
                            document.getElementById("webcam-feed").src = "";
                            document.getElementById("webcam-buttons").style.display = "none";
                        }"""

if old4 in content:
    content = content.replace(old4, new4)
    print("FIX 4: stopWebcam fixed")
else:
    print("FIX 4 FAILED")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("done")
