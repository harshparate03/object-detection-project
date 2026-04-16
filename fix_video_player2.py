with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ── Fix 1: Replace video container (lines 390-400 approx) ──────────────────
for i, line in enumerate(lines):
    if 'id="annotated-video-container"' in line and 'Placeholder' not in line:
        # find end of this div
        depth = 0
        end = i
        for j in range(i, min(i+20, len(lines))):
            depth += lines[j].count('<div') - lines[j].count('</div>')
            if depth <= 0 and j > i:
                end = j
                break
        
        new_html = '''                        <!-- Placeholder for Annotated Video -->
                        <div id="annotated-video-container" style="display: none; position: relative; text-align: center; margin-top: 20px; width: 100%;">
                            <button onclick="closeVideoResult()" style="position: absolute; top: 5px; right: 5px; background: red; color: white; border: none; border-radius: 50%; width: 32px; height: 32px; font-size: 18px; cursor: pointer; z-index: 10;">&times;</button>
                            <h4>Processed Video:</h4>
                            <img id="video-slideshow" src="" style="max-width:100%; max-width:900px; height:auto; border:2px solid white; border-radius:10px; display:none; margin:0 auto;">
                            <video id="annotated-video" controls style="width: 100%; max-width: 900px; height: auto; border: 2px solid white; border-radius: 10px; display: none; margin: 0 auto;">
                                <source id="video-source" src="">
                                Your browser does not support the video tag.
                            </video>
                            <!-- Custom player controls -->
                            <div id="video-player-controls" style="display:none; margin-top:10px; max-width:900px; margin-left:auto; margin-right:auto;">
                                <div id="video-progress-bg" onclick="seekVideo(event)" style="background:#444; border-radius:4px; height:6px; cursor:pointer; margin-bottom:10px; position:relative;">
                                    <div id="video-progress-fill" style="background:linear-gradient(90deg,#ba42ff,#00e1ff); height:100%; border-radius:4px; width:0%; pointer-events:none;"></div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; justify-content:center;">
                                    <button id="video-play-btn" onclick="toggleVideoPlay()" style="background:#ba42ff; border:none; color:white; border-radius:50%; width:40px; height:40px; font-size:18px; cursor:pointer;">&#9654;</button>
                                    <span id="video-time-label" style="color:#ccc; font-size:13px; font-family:monospace;">0 / 0 frames</span>
                                </div>
                            </div>
                        </div>
'''
        # find the actual start line (the one with Placeholder comment)
        start = i - 1 if i > 0 and 'Placeholder' in lines[i-1] else i
        lines[start:end+1] = [new_html]
        print(f"Replaced video container at lines {start}-{end}")
        break

# ── Fix 2: Replace the success handler JS ──────────────────────────────────
for i, line in enumerate(lines):
    if 'resultContainer.style.display = "block"' in line:
        # find the setInterval block end
        for j in range(i, min(i+25, len(lines))):
            if 'setInterval' in lines[j] and j > i:
                # find closing of setInterval
                for k in range(j, min(j+10, len(lines))):
                    if '}, 1000 / fps)' in lines[k]:
                        new_js = '''                                            resultContainer.style.display = "block";

                                            const slideImg = document.getElementById("video-slideshow");
                                            slideImg.style.display = "block";
                                            slideImg.src = frames[0];

                                            // Store for custom player - NO autoplay
                                            window._slideshowFrames = frames;
                                            window._slideshowFps = fps;
                                            window._slideshowFrameIdx = 0;
                                            window._slideshowPlaying = false;
                                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                                            document.getElementById("video-player-controls").style.display = "block";
                                            document.getElementById("video-play-btn").innerHTML = "&#9654;";
                                            document.getElementById("video-progress-fill").style.width = "0%";
                                            document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";
'''
                        lines[i:k+1] = [new_js]
                        print(f"Replaced player JS at lines {i}-{k}")
                        break
                break
        break

# ── Fix 3: Replace closeVideoResult + add player functions ─────────────────
for i, line in enumerate(lines):
    if 'function closeVideoResult()' in line:
        for j in range(i, min(i+15, len(lines))):
            if lines[j].strip() == '}':
                new_funcs = '''                        function closeVideoResult() {
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
                            var ctrl = document.getElementById('video-player-controls');
                            if (ctrl) ctrl.style.display = 'none';
                        }

                        function toggleVideoPlay() {
                            if (!window._slideshowFrames || !window._slideshowFrames.length) return;
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
                                    document.getElementById('video-time-label').textContent = (window._slideshowFrameIdx + 1) + ' / ' + window._slideshowFrames.length + ' frames';
                                    if (window._slideshowFrameIdx === window._slideshowFrames.length - 1) {
                                        clearInterval(window._videoInterval); window._videoInterval = null;
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
                            if (!window._slideshowFrames || !window._slideshowFrames.length) return;
                            var bar = document.getElementById('video-progress-bg');
                            var rect = bar.getBoundingClientRect();
                            var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                            var idx = Math.round(pct * (window._slideshowFrames.length - 1));
                            window._slideshowFrameIdx = idx;
                            document.getElementById('video-slideshow').src = window._slideshowFrames[idx];
                            document.getElementById('video-progress-fill').style.width = (pct * 100) + '%';
                            document.getElementById('video-time-label').textContent = (idx + 1) + ' / ' + window._slideshowFrames.length + ' frames';
                        }

                        function generateVideoReport() {}
'''
                lines[i:j+1] = [new_funcs]
                print(f"Replaced closeVideoResult + added player functions at lines {i}-{j}")
                break
        break

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("All done!")
