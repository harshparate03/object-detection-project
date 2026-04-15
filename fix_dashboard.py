content = open('vision/templates/dashboard.html', encoding='utf-8').read()

# ============================================================
# FIX 1: Add clearAllPanels function (one panel at a time)
# ============================================================
old1 = "// placeholder - real handleImageUpload is defined below\n                    </script>"
new1 = """function clearAllPanels() {
            // Hide image panel
            document.getElementById('annotated-image-container').style.display = 'none';
            document.getElementById('annotated-image').src = '';
            document.getElementById('detection-results').style.display = 'none';
            document.getElementById('detection-list').innerHTML = '';
            document.getElementById('generate-report-button').style.display = 'none';
            document.getElementById('ai-loader').style.display = 'none';
            // Hide video panel
            try {
                var v = document.getElementById('annotated-video');
                v.pause();
                document.getElementById('video-source').src = '';
                v.load();
            } catch(e) {}
            document.getElementById('annotated-video-container').style.display = 'none';
            document.getElementById('detection-results-video').style.display = 'none';
            document.getElementById('video-detection-list').innerHTML = '';
            document.getElementById('generate-report-video-button').style.display = 'none';
            document.getElementById('ai-loader-video').style.display = 'none';
            // Hide webcam panel
            document.getElementById('webcam-feed').src = '';
            document.getElementById('webcam-buttons').style.display = 'none';
        }
                    </script>"""
if old1 in content:
    content = content.replace(old1, new1)
    print("FIX 1: clearAllPanels added")
else:
    print("FIX 1 FAILED")

# ============================================================
# FIX 2: Call clearAllPanels in image upload
# ============================================================
old2 = "if (file && file.type.startsWith('image/')) {\n                const formData = new FormData();\n                formData.append('image', file);\n\n                // Show the AI loader while processing\n                document.getElementById('ai-loader').style.display = 'flex';"
new2 = "if (file && file.type.startsWith('image/')) {\n                clearAllPanels();\n                const formData = new FormData();\n                formData.append('image', file);\n\n                // Show the AI loader while processing\n                document.getElementById('ai-loader').style.display = 'flex';"
if old2 in content:
    content = content.replace(old2, new2)
    print("FIX 2: image clearAllPanels added")
else:
    print("FIX 2 FAILED")

# ============================================================
# FIX 3: Call clearAllPanels in video upload + fix video upload
# The video upload uses 'video-upload-input' via change event
# but the bottom script listens to form submit with 'video-upload' (wrong id)
# Fix: replace bottom video script to use change event on video-upload-input
# ============================================================
old3 = """    <!-- video script -->
    <script>
        document.getElementById('video-upload-form').addEventListener('submit', function (event) {
            event.preventDefault();
            const videoFile = document.getElementById(\"video-upload\").files[0];
            if (!videoFile) {
                alert(\"Please select a video file.\");
                return;
            }

            const formData = new FormData();
            formData.append(\"video\", videoFile);

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            document.getElementById(\"ai-loader-video\").style.display = \"block\";

            fetch(\"{% url 'upload_video' %}\", {
                method: \"POST\",
                body: formData,
                headers: { \"X-CSRFToken\": csrfToken }
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById(\"ai-loader-video\").style.display = \"none\";

                    if (!data.processed_video_url) {
                        console.error(\"❌ No processed_video_url returned:\", data);
                        alert(\"Error: Video processing failed.\");
                        return;
                    }

                    let videoUrl = data.processed_video_url.trim();
                    console.log(\"✅ Processed Video URL:\", videoUrl);

                    // Hide image panel when video is shown
                    document.getElementById('annotated-image-container').style.display = 'none';
                    document.getElementById('detection-results').style.display = 'none';
                    document.getElementById('generate-report-button').style.display = 'none';

                    let videoElement = document.getElementById(\"annotated-video\");
                    let sourceElement = document.getElementById(\"video-source\");

                    sourceElement.src = videoUrl;
                    videoElement.load();

                    videoElement.play().catch(error => console.error(\"❌ Video play error:\", error));

                    document.getElementById(\"annotated-video-container\").style.display = \"block\";
                })
                .catch(error => {
                    console.error(\"❌ Video upload error:\", error);
                    alert(\"Failed to process video.\");
                });
        });
    </script>"""

new3 = """    <!-- video script -->
    <script>
        document.getElementById('video-upload-input').addEventListener('change', function () {
            const videoFile = this.files[0];
            if (!videoFile) return;

            clearAllPanels();

            const formData = new FormData();
            formData.append("video", videoFile);
            const csrfToken = document.querySelector('#image-upload-form [name=csrfmiddlewaretoken]').value;

            document.getElementById("ai-loader-video").style.display = "flex";

            fetch("{% url 'upload_video' %}", {
                method: "POST",
                body: formData,
                headers: { "X-CSRFToken": csrfToken }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("ai-loader-video").style.display = "none";
                if (!data.processed_video_url) {
                    alert("Error: Video processing failed. " + (data.message || ''));
                    return;
                }
                let videoUrl = data.processed_video_url.trim();
                let videoElement = document.getElementById("annotated-video");
                let sourceElement = document.getElementById("video-source");
                sourceElement.src = videoUrl;
                videoElement.load();
                videoElement.play().catch(e => console.error("Play error:", e));
                document.getElementById("annotated-video-container").style.display = "block";
            })
            .catch(error => {
                document.getElementById("ai-loader-video").style.display = "none";
                alert("Failed to process video: " + error.message);
            });
        });
    </script>"""

if old3 in content:
    content = content.replace(old3, new3)
    print("FIX 3: video upload fixed")
else:
    print("FIX 3 FAILED")

# ============================================================
# FIX 4: Fix webcam - use getUserMedia instead of /video_feed/
# Replace openWebcam to use browser camera API
# ============================================================
old4 = """                        function openWebcam() {
                            document.getElementById("webcam-feed").src = "/video_feed/";
                            document.getElementById("webcam-buttons").style.display = "inline-block";
                            document.getElementById("stop-webcam-btn").style.display = "inline-block";
                        }"""

new4 = """                        var webcamStream = null;

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

if old4 in content:
    content = content.replace(old4, new4)
    print("FIX 4: webcam fixed with getUserMedia")
else:
    print("FIX 4 FAILED")

# ============================================================
# FIX 5: Fix stopWebcam to stop getUserMedia stream
# ============================================================
old5 = """                        function stopWebcam() {
                            fetch('/stop_webcam/').then(response => {
                                console.log("Webcam stopped");
                                document.getElementById("webcam-feed").src = "";
                                document.getElementById("webcam-buttons").style.display = "none"; // Hide all buttons after stopping
                            });
                        }"""

new5 = """                        function stopWebcam() {
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

if old5 in content:
    content = content.replace(old5, new5)
    print("FIX 5: stopWebcam fixed")
else:
    print("FIX 5 FAILED")

# ============================================================
# FIX 6: Fix takeScreenshot to use webcam-video element
# ============================================================
old6 = """                        function takeScreenshot() {
                            let videoElement = document.getElementById("webcam-feed");
                            let canvas = document.getElementById("screenshot-canvas");
                            let context = canvas.getContext("2d");

                            if (!videoElement || videoElement.srcObject === null) {
                                alert("Webcam not started or no video feed detected.");
                                return;
                            }"""

new6 = """                        function takeScreenshot() {
                            let videoElement = document.getElementById("webcam-video");
                            let canvas = document.getElementById("screenshot-canvas");
                            let context = canvas.getContext("2d");

                            if (!videoElement || !videoElement.srcObject) {
                                alert("Webcam not started.");
                                return;
                            }"""

if old6 in content:
    content = content.replace(old6, new6)
    print("FIX 6: takeScreenshot fixed")
else:
    print("FIX 6 FAILED")

# Also add clearAllPanels call to openWebcam in the DOMContentLoaded video handler
old7 = "function handleVideoUpload(input) {\n                                const file = input.files[0];\n\n                                if (file && file.type.startsWith(\"video/\")) {\n                                    const formData = new FormData();\n                                    formData.append(\"video\", file);\n\n                                    aiLoader.style.display = \"flex\";"
new7 = "function handleVideoUpload(input) {\n                                const file = input.files[0];\n\n                                if (file && file.type.startsWith(\"video/\")) {\n                                    clearAllPanels();\n                                    const formData = new FormData();\n                                    formData.append(\"video\", file);\n\n                                    aiLoader.style.display = \"flex\";"
if old7 in content:
    content = content.replace(old7, new7)
    print("FIX 7: DOMContentLoaded video handler clearAllPanels added")
else:
    print("FIX 7 SKIPPED (not found)")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("\nAll fixes applied and file saved.")
