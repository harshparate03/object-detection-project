with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the handle video upload script block
start = None
end = None
for i, line in enumerate(lines):
    if '<!-- handle video upload -->' in line:
        start = i
        for j in range(i, min(i + 120, len(lines))):
            if '</script>' in lines[j] and j > i + 10:
                end = j
                break
        break

print("Handler block: lines %d to %d" % (start, end))

new_handler = '''                    <!-- handle video upload -->
                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            const videoUploadInput = document.getElementById("video-upload-input");
                            const aiLoader = document.getElementById("ai-loader-video");
                            const detectionsList = document.getElementById("video-detection-list");

                            videoUploadInput.addEventListener("change", function () {
                                const file = this.files[0];
                                if (!file || !file.type.startsWith("video/")) {
                                    alert("Please upload a valid video file");
                                    return;
                                }

                                const formData = new FormData();
                                formData.append("video", file);

                                aiLoader.style.display = "flex";
                                document.getElementById("annotated-video-container").style.display = "none";
                                detectionsList.innerHTML = "";

                                fetch("{% url 'upload_video' %}", {
                                    method: "POST",
                                    body: formData,
                                    headers: { "X-CSRFToken": getCsrfToken() }
                                })
                                .then(r => r.json())
                                .then(data => {
                                    aiLoader.style.display = "none";
                                    if (data.status === "success" && data.frames && data.frames.length > 0) {
                                        vpInit(data.frames, data.fps || 5);
                                        if (data.detected_objects && data.detected_objects.length > 0) {
                                            detectionsList.innerHTML = "";
                                            data.detected_objects.forEach(obj => {
                                                const li = document.createElement("li");
                                                li.textContent = obj.label + ": " + obj.count;
                                                li.style.color = "white";
                                                detectionsList.appendChild(li);
                                            });
                                            document.getElementById("detection-results-video").style.display = "block";
                                        }
                                        setTimeout(() => document.getElementById("annotated-video-container").scrollIntoView({ behavior: "smooth", block: "center" }), 300);
                                    } else {
                                        alert("Error: " + (data.message || "Video processing failed."));
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

if start is not None and end is not None:
    lines[start:end+1] = [new_handler]
    print("Replaced successfully")
else:
    print("ERROR: block not found")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
