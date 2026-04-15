content = open('vision/templates/dashboard.html', encoding='utf-8').read()

# Fix 1: Fix video display after processing - remove auto play, fix size
old1 = """                document.getElementById("annotated-video-container").style.display = "block\"; // \u2705 Show video container\r\n                                                processedVideo.style.display = \"block\"; // \u2705 Ensure video is visible"""

# Fix 2: Fix the video source setting and play in DOMContentLoaded handler
old2 = """                                                // \u2705 Correctly set the video source
                                                videoSource.src = data.processed_video_url;
                                                processedVideo.load();
                                                processedVideo.play().catch(error => console.error("Play error:", error));

                                                processedVideoContainer.style.display = "block"; // \u2705 Show video container
                                                processedVideo.style.display = "block"; // \u2705 Ensure video is visible"""

new2 = """                                                // Set video source and show container
                                                processedVideoContainer.style.display = "block";
                                                videoSource.src = data.processed_video_url;
                                                processedVideo.load();"""

if old2 in content:
    content = content.replace(old2, new2)
    print("FIX 1: DOMContentLoaded video play fixed")
else:
    print("FIX 1 FAILED")

# Fix 3: Fix the bottom video script play error
old3 = """                    sourceElement.src = videoUrl;
                    videoElement.load();

                    videoElement.play().catch(error => console.error("\u274c Video play error:", error));

                    document.getElementById("annotated-video-container").style.display = "block";"""

new3 = """                    document.getElementById("annotated-video-container").style.display = "block";
                    sourceElement.src = videoUrl;
                    videoElement.load();"""

if old3 in content:
    content = content.replace(old3, new3)
    print("FIX 2: bottom video script play fixed")
else:
    print("FIX 2 FAILED")

# Fix 4: Fix video container size - make it proper width not webcam size
old4 = """                        <!-- Placeholder for Annotated Video -->
                        <div id="annotated-video-container" style="display: none; position: relative; text-align: center; margin-top: 20px;">
                            <button onclick="closeVideoPanel()" style="position: absolute; top: 5px; right: 5px; background: red; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; font-size: 16px; cursor: pointer; z-index: 10;">\u2715</button>
                            <h4>Processed Video:</h4>
                            <video id="annotated-video" controls style="max-width: 100%; height: auto; border: 2px solid white; border-radius: 10px;">
                                <source id="video-source" src="">
                                Your browser does not support the video tag.
                            </video>
                        </div>"""

new4 = """                        <!-- Placeholder for Annotated Video -->
                        <div id="annotated-video-container" style="display: none; position: relative; text-align: center; margin-top: 20px; width: 100%;">
                            <button onclick="closeVideoPanel()" style="position: absolute; top: 5px; right: 5px; background: red; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; font-size: 16px; cursor: pointer; z-index: 10;">\u2715</button>
                            <h4>Processed Video:</h4>
                            <video id="annotated-video" controls style="width: 80%; max-width: 900px; height: auto; border: 2px solid white; border-radius: 10px;">
                                <source id="video-source" src="">
                                Your browser does not support the video tag.
                            </video>
                        </div>"""

if old4 in content:
    content = content.replace(old4, new4)
    print("FIX 3: video container size fixed")
else:
    print("FIX 3 FAILED")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("done")
