with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the DOMContentLoaded script block for video upload
start = None
end = None
for i, line in enumerate(lines):
    if 'document.addEventListener("DOMContentLoaded", function ()' in line and start is None:
        start = i
    if start and '</script>' in line and i > start:
        end = i
        break

print(f"DOMContentLoaded block: lines {start} to {end}")

if start and end:
    new_block = '''                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            const videoUploadInput = document.getElementById("video-upload-input");
                            const aiLoader = document.getElementById("ai-loader-video");
                            const processedVideoContainer = document.getElementById("annotated-video-container");
                            const detectionsList = document.getElementById("video-detection-list");
                            const reportButton = document.getElementById("generate-report-video-button");

                            videoUploadInput.addEventListener("change", function () {
                                const file = this.files[0];
                                if (!file || !file.type.startsWith("video/")) {
                                    alert("Please upload a valid video file");
                                    return;
                                }

                                const formData = new FormData();
                                formData.append("video", file);

                                aiLoader.style.display = "flex";
                                processedVideoContainer.style.display = "none";
                                detectionsList.innerHTML = "";
                                reportButton.style.display = "none";

                                fetch("{% url 'upload_video' %}", {
                                    method: "POST",
                                    body: formData,
                                    headers: { "X-CSRFToken": getCsrfToken() }
                                })
                                .then(r => r.json())
                                .then(data => {
                                    aiLoader.style.display = "none";

                                    if (data.status === "success" && data.frames && data.frames.length > 0) {
                                        const frames = data.frames;
                                        const fps = data.fps || 5;
                                        let frameIdx = 0;

                                        processedVideoContainer.style.display = "block";
                                        document.getElementById("annotated-video").style.display = "none";

                                        let slideImg = document.getElementById("video-slideshow");
                                        if (!slideImg) {
                                            slideImg = document.createElement("img");
                                            slideImg.id = "video-slideshow";
                                            slideImg.style.cssText = "max-width:100%;border:2px solid white;border-radius:10px;display:block;margin:0 auto;";
                                            processedVideoContainer.appendChild(slideImg);
                                        }
                                        slideImg.style.display = "block";
                                        slideImg.src = frames[0];

                                        if (window._videoInterval) clearInterval(window._videoInterval);
                                        window._videoInterval = setInterval(() => {
                                            frameIdx = (frameIdx + 1) % frames.length;
                                            slideImg.src = frames[frameIdx];
                                        }, 1000 / fps);

                                        if (data.detected_objects && data.detected_objects.length > 0) {
                                            detectionsList.innerHTML = "";
                                            data.detected_objects.forEach(obj => {
                                                const li = document.createElement("li");
                                                li.textContent = obj.label + ": " + obj.count;
                                                li.style.color = "white";
                                                detectionsList.appendChild(li);
                                            });
                                            document.getElementById("detection-results-video").style.display = "block";
                                            reportButton.style.display = "inline-block";
                                        }

                                        setTimeout(() => processedVideoContainer.scrollIntoView({ behavior: "smooth", block: "center" }), 300);
                                    } else {
                                        alert("Error processing the video: " + (data.message || "Unknown error"));
                                    }
                                })
                                .catch(err => {
                                    aiLoader.style.display = "none";
                                    alert("An error occurred while processing the video: " + err.message);
                                });
                            });
                        });
                    </script>

'''
    lines[start:end+1] = [new_block]
    print("Replaced successfully")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
