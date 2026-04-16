with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the first handler's success block
start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'data.status === "success"' in line and start_line is None:
        start_line = i
    if start_line and 'processedVideoContainer.scrollIntoView' in line:
        end_line = i
        break

print(f"Found block: lines {start_line} to {end_line}")

if start_line and end_line:
    new_block = '''                                            if (data.status === "success" && data.frames && data.frames.length > 0) {
                                                console.log("✅ Frames received:", data.frames.length);
                                                const frames = data.frames;
                                                const fps = data.fps || 5;
                                                let frameIdx = 0;

                                                processedVideoContainer.style.display = "block";
                                                processedVideo.style.display = "none";

                                                let slideImg = document.getElementById('video-slideshow');
                                                if (!slideImg) {
                                                    slideImg = document.createElement('img');
                                                    slideImg.id = 'video-slideshow';
                                                    slideImg.style.cssText = 'max-width:100%;border:2px solid white;border-radius:10px;display:block;margin:0 auto;';
                                                    processedVideoContainer.appendChild(slideImg);
                                                }
                                                slideImg.style.display = 'block';
                                                slideImg.src = frames[0];

                                                if (window._videoInterval) clearInterval(window._videoInterval);
                                                window._videoInterval = setInterval(() => {
                                                    frameIdx = (frameIdx + 1) % frames.length;
                                                    slideImg.src = frames[frameIdx];
                                                }, 1000 / fps);

                                                if (data.detected_objects && data.detected_objects.length > 0) {
                                                    detectionsList.innerHTML = '';
                                                    data.detected_objects.forEach(obj => {
                                                        const li = document.createElement('li');
                                                        li.textContent = obj.label + ': ' + obj.count;
                                                        li.style.color = 'white';
                                                        detectionsList.appendChild(li);
                                                    });
                                                    document.getElementById('detection-results-video').style.display = 'block';
                                                    reportButton.style.display = 'inline-block';
                                                }

                                                setTimeout(() => processedVideoContainer.scrollIntoView({ behavior: 'smooth', block: 'center' }), 300);
'''
    lines[start_line:end_line+1] = [new_block]
    print("Replaced successfully")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
