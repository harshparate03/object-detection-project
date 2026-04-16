with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with 'processed_video_url' check in the form submit handler
start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'if (!data.processed_video_url)' in line:
        start_line = i
    if start_line and 'annotated-video-container' in line and 'display' in line and i > start_line:
        end_line = i
        break

if start_line and end_line:
    new_block = '''                    if (data.status === "success" && data.frames && data.frames.length > 0) {
                        const frames = data.frames;
                        const fps = data.fps || 5;
                        let frameIdx = 0;

                        document.getElementById("annotated-video-container").style.display = "block";
                        document.getElementById("annotated-video").style.display = "none";

                        let slideImg = document.getElementById('video-slideshow');
                        if (!slideImg) {
                            slideImg = document.createElement('img');
                            slideImg.id = 'video-slideshow';
                            slideImg.style.cssText = 'max-width:100%;border:2px solid white;border-radius:10px;display:block;margin:0 auto;';
                            document.getElementById("annotated-video-container").appendChild(slideImg);
                        }
                        slideImg.style.display = 'block';
                        slideImg.src = frames[0];

                        if (window._videoInterval) clearInterval(window._videoInterval);
                        window._videoInterval = setInterval(() => {
                            frameIdx = (frameIdx + 1) % frames.length;
                            slideImg.src = frames[frameIdx];
                        }, 1000 / fps);

                        if (data.detected_objects && data.detected_objects.length > 0) {
                            const list = document.getElementById("video-detection-list");
                            list.innerHTML = '';
                            data.detected_objects.forEach(obj => {
                                const li = document.createElement('li');
                                li.textContent = obj.label + ': ' + obj.count;
                                li.style.color = 'white';
                                list.appendChild(li);
                            });
                            document.getElementById("detection-results-video").style.display = "block";
                        }

                        setTimeout(() => document.getElementById("annotated-video-container").scrollIntoView({ behavior: 'smooth', block: 'center' }), 300);
                    } else {
                        alert("Error: " + (data.message || "Video processing failed."));
                    }
'''
    lines[start_line:end_line+1] = [new_block]
    print(f"Replaced lines {start_line} to {end_line}")
else:
    print(f"start_line={start_line}, end_line={end_line} - not found")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
