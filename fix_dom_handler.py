with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                    <!-- handle video upload -->
                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            const videoUploadInput = document.getElementById("video-upload-input");
                            const aiLoader = document.getElementById("ai-loader-video");

                            const processedVideoContainer = document.getElementById("annotated-video-container");
                            const detectionsList = document.getElementById("video-detection-list");
                            const reportButton = document.getElementById("generate-report-video-button");'''

new = '''                    <!-- handle video upload -->
                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            const videoUploadInput = document.getElementById("video-upload-input");
                            const aiLoader = document.getElementById("ai-loader-video");
                            const processedVideoContainer = document.getElementById("annotated-video-container");
                            const detectionsList = document.getElementById("video-detection-list");'''

if old in content:
    content = content.replace(old, new)
    print("Header replaced")
else:
    print("Header not found - trying line approach")

# Now replace the success block inside this handler
old_success = '''                                    if (data.status === "success" && data.frames && data.frames.length > 0) {

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

                                    }'''

new_success = '''                                    if (data.status === "success" && data.frames && data.frames.length > 0) {
                                        const frames = data.frames;
                                        const fps = data.fps || 5;

                                        processedVideoContainer.style.display = "block";
                                        document.getElementById("annotated-video").style.display = "none";

                                        const slideImg = document.getElementById("video-slideshow");
                                        slideImg.style.display = "block";
                                        slideImg.src = frames[0];

                                        // Custom player - no autoplay
                                        window._slideshowFrames = frames;
                                        window._slideshowFps = fps;
                                        window._slideshowFrameIdx = 0;
                                        window._slideshowPlaying = false;
                                        if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }

                                        document.getElementById("video-player-controls").style.display = "block";
                                        document.getElementById("video-play-btn").innerHTML = "&#9654;";
                                        document.getElementById("video-progress-fill").style.width = "0%";
                                        document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";

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

                                        setTimeout(() => processedVideoContainer.scrollIntoView({ behavior: "smooth", block: "center" }), 300);

                                    } else {
                                        alert("Error processing the video: " + (data.message || "Unknown error"));
                                    }'''

if old_success in content:
    content = content.replace(old_success, new_success)
    print("Success block replaced")
else:
    print("Success block not found - doing targeted fixes")
    # Just fix the two null references
    content = content.replace(
        'const reportButton = document.getElementById("generate-report-video-button");',
        ''
    )
    content = content.replace(
        'reportButton.style.display = "none";',
        ''
    )
    content = content.replace(
        'reportButton.style.display = "inline-block";',
        ''
    )
    # Fix autoplay to use custom player
    content = content.replace(
        '''if (window._videoInterval) clearInterval(window._videoInterval);
                                        window._videoInterval = setInterval(() => {


                                            frameIdx = (frameIdx + 1) % frames.length;

                                            slideImg.src = frames[frameIdx];

                                        }, 1000 / fps);''',
        '''// Custom player - no autoplay
                                        window._slideshowFrames = frames;
                                        window._slideshowFps = fps;
                                        window._slideshowFrameIdx = 0;
                                        window._slideshowPlaying = false;
                                        if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                                        document.getElementById("video-player-controls").style.display = "block";
                                        document.getElementById("video-play-btn").innerHTML = "&#9654;";
                                        document.getElementById("video-progress-fill").style.width = "0%";
                                        document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";'''
    )
    print("Targeted fixes applied")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
