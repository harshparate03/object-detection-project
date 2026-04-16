with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the form submit handler success block and replace it
start = None
end = None
for i, line in enumerate(lines):
    if "document.getElementById('video-upload-form').addEventListener" in line:
        start = i
    if start and "});\n" == lines[i] and i > start + 5:
        # check next line is </script>
        if i + 1 < len(lines) and '</script>' in lines[i+1]:
            end = i
            break

print(f"Form submit handler: lines {start} to {end}")

if start and end:
    new_handler = '''    <script>
        document.getElementById('video-upload-form').addEventListener('submit', function (event) {
            event.preventDefault();
            const videoFile = document.getElementById("video-upload").files[0];
            if (!videoFile) { alert("Please select a video file."); return; }

            const formData = new FormData();
            formData.append("video", videoFile);
            const csrfToken = getCsrfToken();

            document.getElementById("ai-loader-video").style.display = "block";
            document.getElementById("annotated-video-container").style.display = "none";

            fetch("{% url 'upload_video' %}", {
                method: "POST",
                body: formData,
                headers: { "X-CSRFToken": csrfToken }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("ai-loader-video").style.display = "none";

                if (data.status === "success" && data.frames && data.frames.length > 0) {
                    const frames = data.frames;
                    const fps = data.fps || 5;

                    // Show container
                    document.getElementById("annotated-video-container").style.display = "block";
                    document.getElementById("annotated-video").style.display = "none";

                    // Show first frame, no autoplay
                    const slideImg = document.getElementById("video-slideshow");
                    slideImg.style.display = "block";
                    slideImg.src = frames[0];

                    // Store for custom player
                    window._slideshowFrames = frames;
                    window._slideshowFps = fps;
                    window._slideshowFrameIdx = 0;
                    window._slideshowPlaying = false;
                    if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }

                    // Init player controls
                    document.getElementById("video-player-controls").style.display = "block";
                    document.getElementById("video-play-btn").innerHTML = "&#9654;";
                    document.getElementById("video-progress-fill").style.width = "0%";
                    document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";

                    // Show detected objects
                    if (data.detected_objects && data.detected_objects.length > 0) {
                        const list = document.getElementById("video-detection-list");
                        list.innerHTML = "";
                        data.detected_objects.forEach(obj => {
                            const li = document.createElement("li");
                            li.textContent = obj.label + ": " + obj.count;
                            li.style.color = "white";
                            list.appendChild(li);
                        });
                        document.getElementById("detection-results-video").style.display = "block";
                    }

                    setTimeout(() => document.getElementById("annotated-video-container").scrollIntoView({ behavior: "smooth", block: "center" }), 300);
                } else {
                    alert("Error: " + (data.message || "Video processing failed."));
                }
            })
            .catch(error => {
                document.getElementById("ai-loader-video").style.display = "none";
                alert("Failed to process video: " + error.message);
            });
        });
    </script>
'''
    lines[start:end+1] = [new_handler]
    print("Replaced successfully")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
