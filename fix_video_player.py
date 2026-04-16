with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the video container HTML - proper player UI, no autoplay
old_container = '''                        <!-- Video Result Panel -->
                        <div id="annotated-video-container" style="display:none; position:relative; text-align:center; margin-top:24px; width:100%;">
                            <div style="background:linear-gradient(135deg,#1a1a2e,#16213e); border:1px solid #ba42ff44; border-radius:16px; padding:20px; display:inline-block; width:100%; max-width:960px; box-shadow:0 0 30px #ba42ff18;">
                                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;padding:0 4px;">
                                    <span style="color:#ba42ff;font-weight:700;font-size:15px;letter-spacing:1px;">&#9654; PROCESSED VIDEO</span>
                                    <button onclick="closeVideoResult()" style="background:#e74c3c22;border:1px solid #e74c3c;color:#e74c3c;border-radius:8px;padding:4px 12px;cursor:pointer;font-size:13px;">&times; Close</button>
                                </div>
                                <img id="video-slideshow" src="" style="max-width:100%;border:1px solid #ba42ff44;border-radius:10px;display:none;margin:0 auto;">
                                <video id="annotated-video" controls style="display:none;width:100%;max-width:900px;border:1px solid #ba42ff44;border-radius:10px;margin:0 auto;">
                                    <source id="video-source" src="">
                                </video>
                            </div>
                        </div>'''

new_container = '''                        <!-- Video Result Panel -->
                        <div id="annotated-video-container" style="display:none; position:relative; text-align:center; margin-top:24px; width:100%;">
                            <button onclick="closeVideoResult()" style="position:absolute;top:8px;right:8px;background:red;color:white;border:none;border-radius:50%;width:30px;height:30px;font-size:16px;cursor:pointer;z-index:10;">&times;</button>
                            <h4>Processed Video:</h4>

                            <!-- Frame display -->
                            <img id="video-slideshow" src="" style="max-width:100%;max-width:900px;height:auto;border:2px solid white;border-radius:10px;display:none;margin:0 auto;">
                            <video id="annotated-video" controls style="display:none;width:100%;max-width:900px;border:2px solid white;border-radius:10px;margin:0 auto;">
                                <source id="video-source" src="">
                            </video>

                            <!-- Custom player controls -->
                            <div id="video-player-controls" style="display:none; margin-top:12px; max-width:900px; margin-left:auto; margin-right:auto;">
                                <!-- Progress bar -->
                                <div id="video-progress-bg" onclick="seekVideo(event)" style="background:#333;border-radius:4px;height:6px;cursor:pointer;margin-bottom:10px;position:relative;">
                                    <div id="video-progress-fill" style="background:linear-gradient(90deg,#ba42ff,#00e1ff);height:100%;border-radius:4px;width:0%;pointer-events:none;"></div>
                                </div>
                                <!-- Buttons row -->
                                <div style="display:flex;align-items:center;gap:12px;justify-content:center;">
                                    <button id="video-play-btn" onclick="toggleVideoPlay()" style="background:#ba42ff;border:none;color:white;border-radius:50%;width:40px;height:40px;font-size:18px;cursor:pointer;">&#9654;</button>
                                    <span id="video-time-label" style="color:#ccc;font-size:13px;font-family:monospace;">0 / 0 frames</span>
                                </div>
                            </div>
                        </div>'''

if old_container in content:
    content = content.replace(old_container, new_container)
    print("Container replaced")
else:
    # fallback - find by key marker
    content = content.replace(
        '<h4>Processed Video:</h4>\n                            <button id="slideshow-toggle-btn"',
        '<h4>Processed Video:</h4>\n                            <!-- toggle removed -->'
    )
    print("Fallback applied")

# 2. Replace the JS handler to NOT autoplay, use custom player
old_player_js = '''                                            resultContainer.style.display = "block";

                                            const slideImg = document.getElementById("video-slideshow");
                                            slideImg.style.display = "block";
                                            slideImg.src = frames[0];

                                            // Store globally for pause/play
                                            window._slideshowFrames = frames;
                                            window._slideshowFps = fps;
                                            window._slideshowFrameIdx = 0;
                                            _slideshowPaused = false;
                                            var toggleBtn = document.getElementById("slideshow-toggle-btn");
                                            if (toggleBtn) toggleBtn.textContent = "⏸ Pause";

                                            if (window._videoInterval) clearInterval(window._videoInterval);
                                            window._videoInterval = setInterval(() => {
                                                frameIdx = (frameIdx + 1) % frames.length;
                                                window._slideshowFrameIdx = frameIdx;
                                                slideImg.src = frames[frameIdx];
                                            }, 1000 / fps);'''

new_player_js = '''                                            resultContainer.style.display = "block";

                                            const slideImg = document.getElementById("video-slideshow");
                                            slideImg.style.display = "block";
                                            slideImg.src = frames[0];

                                            // Store globally for custom player
                                            window._slideshowFrames = frames;
                                            window._slideshowFps = fps;
                                            window._slideshowFrameIdx = 0;
                                            window._slideshowPlaying = false;
                                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }

                                            // Show controls, reset to frame 0, NOT playing
                                            document.getElementById("video-player-controls").style.display = "block";
                                            document.getElementById("video-play-btn").innerHTML = "&#9654;";
                                            document.getElementById("video-progress-fill").style.width = "0%";
                                            document.getElementById("video-time-label").textContent = "0 / " + frames.length + " frames";'''

if old_player_js in content:
    content = content.replace(old_player_js, new_player_js)
    print("Player JS replaced")
else:
    print("WARNING: player JS pattern not found")

# 3. Replace closeVideoResult to also reset player
content = content.replace(
    '''                        function closeVideoResult() {
                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.src = ''; slide.style.display = 'none'; }
                            var v = document.getElementById('annotated-video');
                            v.pause();
                            document.getElementById('video-source').src = '';
                            v.load();
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                        }''',
    '''                        function closeVideoResult() {
                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                            window._slideshowPlaying = false;
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.src = ''; slide.style.display = 'none'; }
                            var v = document.getElementById('annotated-video');
                            v.pause();
                            document.getElementById('video-source').src = '';
                            v.load();
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                            document.getElementById('video-player-controls').style.display = 'none';
                        }

                        function toggleVideoPlay() {
                            if (!window._slideshowFrames || window._slideshowFrames.length === 0) return;
                            window._slideshowPlaying = !window._slideshowPlaying;
                            var btn = document.getElementById('video-play-btn');
                            if (window._slideshowPlaying) {
                                btn.innerHTML = "&#9646;&#9646;";
                                if (window._videoInterval) clearInterval(window._videoInterval);
                                window._videoInterval = setInterval(function() {
                                    window._slideshowFrameIdx = (window._slideshowFrameIdx + 1) % window._slideshowFrames.length;
                                    document.getElementById('video-slideshow').src = window._slideshowFrames[window._slideshowFrameIdx];
                                    var pct = (window._slideshowFrameIdx / (window._slideshowFrames.length - 1)) * 100;
                                    document.getElementById('video-progress-fill').style.width = pct + '%';
                                    document.getElementById('video-time-label').textContent = window._slideshowFrameIdx + ' / ' + window._slideshowFrames.length + ' frames';
                                    // Stop at end
                                    if (window._slideshowFrameIdx === window._slideshowFrames.length - 1) {
                                        clearInterval(window._videoInterval);
                                        window._videoInterval = null;
                                        window._slideshowPlaying = false;
                                        btn.innerHTML = "&#9654;";
                                    }
                                }, 1000 / (window._slideshowFps || 5));
                            } else {
                                btn.innerHTML = "&#9654;";
                                if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                            }
                        }

                        function seekVideo(e) {
                            if (!window._slideshowFrames || window._slideshowFrames.length === 0) return;
                            var bar = document.getElementById('video-progress-bg');
                            var rect = bar.getBoundingClientRect();
                            var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                            var idx = Math.round(pct * (window._slideshowFrames.length - 1));
                            window._slideshowFrameIdx = idx;
                            document.getElementById('video-slideshow').src = window._slideshowFrames[idx];
                            document.getElementById('video-progress-fill').style.width = (pct * 100) + '%';
                            document.getElementById('video-time-label').textContent = idx + ' / ' + window._slideshowFrames.length + ' frames';
                        }'''
)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
