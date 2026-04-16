with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the form submit handler
start = None
end = None
for i, line in enumerate(lines):
    if "document.getElementById('video-upload-form').addEventListener" in line:
        start = i
        for j in range(i, min(i + 80, len(lines))):
            if '</script>' in lines[j] and j > i + 10:
                end = j
                break
        break

print("Form handler: lines %d to %d" % (start, end))

new_form_handler = '''    <!-- video script -->
    <script>
        document.getElementById('video-upload-form').addEventListener('submit', function (event) {
            event.preventDefault();
            const videoFile = document.getElementById("video-upload").files[0];
            if (!videoFile) { alert("Please select a video file."); return; }

            const formData = new FormData();
            formData.append("video", videoFile);

            document.getElementById("ai-loader-video").style.display = "block";
            document.getElementById("annotated-video-container").style.display = "none";

            fetch("{% url 'upload_video' %}", {
                method: "POST",
                body: formData,
                headers: { "X-CSRFToken": getCsrfToken() }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("ai-loader-video").style.display = "none";
                if (data.status === "success" && data.frames && data.frames.length > 0) {
                    vpInit(data.frames, data.fps || 5);
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

</body>

</html>
'''

if start is not None:
    # Replace from start to end of file
    lines = lines[:start] + [new_form_handler]
    print("Replaced form handler to end of file")
else:
    print("ERROR: form handler not found")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
