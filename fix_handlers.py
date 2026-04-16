with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix handler 1 - remove old resultContainer.style.display and use vpInit
content = content.replace(
    '''resultContainer.style.display = "block";

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
                                            document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";''',
    'vpInit(frames, fps);'
)

# Fix handler 2 - same
content = content.replace(
    '''document.getElementById("annotated-video-container").style.display = "block";
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
                    document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";''',
    'vpInit(frames, fps);'
)

# Also fix any remaining old-style references
content = content.replace(
    'window._slideshowFrames = frames;\n                                        window._slideshowFps = fps;\n                                        window._slideshowFrameIdx = 0;\n                                        window._slideshowPlaying = false;\n                                        if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }\n\n                                        document.getElementById("video-player-controls").style.display = "block";\n                                        document.getElementById("video-play-btn").innerHTML = "&#9654;";\n                                        document.getElementById("video-progress-fill").style.width = "0%";\n                                        document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";',
    'vpInit(frames, fps);'
)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
