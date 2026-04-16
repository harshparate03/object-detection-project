with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the video success handler to use frame slideshow
old = '''                                        .then((data) => {

                                            aiLoader.style.display = "none"; // Hide loader



                                            if (data.status === "success") {

                                                console.log("✅ Processed Video URL::", data.processed_video_url);



                                                // ✅ Correctly set the video source

                                                videoSource.src = data.processed_video_url;

                                                processedVideo.load();

                                                processedVideoContainer.style.display = "block";
                                                processedVideo.style.display = "block";

                                                // Show detected objects
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

                                                setTimeout(function() { processedVideoContainer.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 300);

                                            } else {
                                                alert("Error processing the video: " + data.message, "error");
                                            }
                                        })'''

new = '''                                        .then((data) => {

                                            aiLoader.style.display = "none";

                                            if (data.status === "success" && data.frames && data.frames.length > 0) {
                                                // Play frames as slideshow
                                                const frames = data.frames;
                                                const fps = data.fps || 5;
                                                let frameIdx = 0;

                                                // Show container with an img instead of video
                                                processedVideoContainer.style.display = "block";
                                                processedVideo.style.display = "none";

                                                // Create or reuse slideshow img
                                                let slideImg = document.getElementById('video-slideshow');
                                                if (!slideImg) {
                                                    slideImg = document.createElement('img');
                                                    slideImg.id = 'video-slideshow';
                                                    slideImg.style.cssText = 'max-width:100%;border:2px solid white;border-radius:10px;display:block;margin:0 auto;';
                                                    processedVideoContainer.appendChild(slideImg);
                                                }
                                                slideImg.style.display = 'block';
                                                slideImg.src = frames[0];

                                                // Loop through frames
                                                if (window._videoInterval) clearInterval(window._videoInterval);
                                                window._videoInterval = setInterval(() => {
                                                    frameIdx = (frameIdx + 1) % frames.length;
                                                    slideImg.src = frames[frameIdx];
                                                }, 1000 / fps);

                                                // Show detected objects
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

                                            } else {
                                                alert("Error processing the video: " + (data.message || 'Unknown error'));
                                            }
                                        })'''

if old in content:
    content = content.replace(old, new)
    print("Dashboard JS replaced successfully")
else:
    print("Pattern not found - trying simpler replace")
    # simpler targeted replace
    content = content.replace(
        'console.log("✅ Processed Video URL::", data.processed_video_url);',
        'console.log("✅ Frames received:", data.frames ? data.frames.length : 0);'
    )
    print("Done simple replace")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
