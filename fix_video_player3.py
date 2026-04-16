with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── Replace the video container HTML ────────────────────────────────────────
old_container = '''                        <!-- Placeholder for Annotated Video -->

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
                        </div>'''

new_container = '''                        <!-- Processed Video Player -->
                        <div id="annotated-video-container" style="display:none; margin-top:24px; width:100%; max-width:920px; margin-left:auto; margin-right:auto;">
                            <div style="background:#111827; border:1px solid #374151; border-radius:14px; overflow:hidden; box-shadow:0 8px 32px rgba(0,0,0,0.5);">

                                <!-- Player header -->
                                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px; border-bottom:1px solid #1f2937;">
                                    <span style="color:#9ca3af; font-size:13px; font-weight:600; letter-spacing:0.5px;">&#127909; PROCESSED VIDEO</span>
                                    <button onclick="closeVideoResult()" title="Close" style="background:none; border:1px solid #374151; color:#9ca3af; border-radius:6px; width:28px; height:28px; cursor:pointer; font-size:14px; line-height:1;">&times;</button>
                                </div>

                                <!-- Frame display area -->
                                <div style="background:#000; position:relative; min-height:200px; display:flex; align-items:center; justify-content:center;">
                                    <img id="video-slideshow" src="" alt="Video frame"
                                        style="width:100%; max-height:500px; object-fit:contain; display:none;">
                                    <!-- Error state -->
                                    <div id="vp-error" style="display:none; color:#ef4444; font-size:14px; padding:20px;">
                                        &#9888; Could not load video frames.
                                    </div>
                                </div>

                                <!-- Controls bar -->
                                <div style="padding:12px 16px; background:#111827;">

                                    <!-- Progress bar -->
                                    <div style="margin-bottom:10px;">
                                        <div id="vp-progress-bg" style="background:#374151; border-radius:99px; height:5px; cursor:pointer; position:relative;"
                                            onmousedown="vpSeekStart(event)" onmousemove="vpSeekMove(event)" onmouseup="vpSeekEnd(event)" onmouseleave="vpSeekEnd(event)">
                                            <div id="vp-progress-fill" style="background:linear-gradient(90deg,#8b5cf6,#06b6d4); height:100%; border-radius:99px; width:0%; transition:width 0.1s linear; pointer-events:none;"></div>
                                            <div id="vp-thumb" style="position:absolute; top:50%; right:auto; transform:translate(-50%,-50%); width:13px; height:13px; background:#fff; border-radius:50%; left:0%; pointer-events:none; box-shadow:0 0 4px rgba(0,0,0,0.5);"></div>
                                        </div>
                                    </div>

                                    <!-- Buttons row -->
                                    <div style="display:flex; align-items:center; gap:10px;">

                                        <!-- Play/Pause -->
                                        <button id="vp-play-btn" onclick="vpTogglePlay()" title="Play / Pause"
                                            style="background:#8b5cf6; border:none; color:#fff; border-radius:50%; width:38px; height:38px; font-size:16px; cursor:pointer; flex-shrink:0; display:flex; align-items:center; justify-content:center;">
                                            &#9654;
                                        </button>

                                        <!-- Time display -->
                                        <span id="vp-time" style="color:#d1d5db; font-size:12px; font-family:monospace; white-space:nowrap; min-width:80px;">0:00 / 0:00</span>

                                        <!-- Spacer -->
                                        <div style="flex:1;"></div>

                                        <!-- Volume -->
                                        <span style="color:#9ca3af; font-size:14px;">&#128266;</span>
                                        <input id="vp-volume" type="range" min="0" max="100" value="80"
                                            oninput="vpSetVolume(this.value)"
                                            style="width:70px; accent-color:#8b5cf6; cursor:pointer;">

                                        <!-- Download -->
                                        <button id="vp-download-btn" onclick="vpDownload()" title="Download video frames as ZIP"
                                            style="background:none; border:1px solid #374151; color:#9ca3af; border-radius:8px; padding:5px 10px; font-size:12px; cursor:pointer; display:flex; align-items:center; gap:5px; white-space:nowrap;">
                                            &#11015; Download
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>'''

if old_container in content:
    content = content.replace(old_container, new_container)
    print("Container replaced")
else:
    print("ERROR: container not found")

# ── Replace player JS functions ──────────────────────────────────────────────
old_funcs = '''                        function generateVideoReport() {}
                        function closeVideoResult() {

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
                        }'''

new_funcs = '''                        function generateVideoReport() {}

                        // ── Video Player ──────────────────────────────────
                        var _vp = {
                            frames: [], fps: 5, idx: 0, playing: false,
                            timer: null, seeking: false, volume: 0.8
                        };

                        function vpFmtTime(sec) {
                            var m = Math.floor(sec / 60), s = Math.floor(sec % 60);
                            return m + ':' + (s < 10 ? '0' : '') + s;
                        }

                        function vpUpdateUI() {
                            var total = _vp.frames.length;
                            var pct = total > 1 ? (_vp.idx / (total - 1)) * 100 : 0;
                            document.getElementById('vp-progress-fill').style.width = pct + '%';
                            document.getElementById('vp-thumb').style.left = pct + '%';
                            var cur = vpFmtTime(_vp.idx / _vp.fps);
                            var dur = vpFmtTime((total - 1) / _vp.fps);
                            document.getElementById('vp-time').textContent = cur + ' / ' + dur;
                        }

                        function vpTogglePlay() {
                            if (!_vp.frames.length) return;
                            _vp.playing = !_vp.playing;
                            document.getElementById('vp-play-btn').innerHTML = _vp.playing ? '&#9646;&#9646;' : '&#9654;';
                            if (_vp.playing) {
                                // restart from beginning if at end
                                if (_vp.idx >= _vp.frames.length - 1) _vp.idx = 0;
                                if (_vp.timer) clearInterval(_vp.timer);
                                _vp.timer = setInterval(function() {
                                    _vp.idx++;
                                    if (_vp.idx >= _vp.frames.length) {
                                        _vp.idx = _vp.frames.length - 1;
                                        clearInterval(_vp.timer); _vp.timer = null;
                                        _vp.playing = false;
                                        document.getElementById('vp-play-btn').innerHTML = '&#9654;';
                                    }
                                    document.getElementById('video-slideshow').src = _vp.frames[_vp.idx];
                                    vpUpdateUI();
                                }, 1000 / _vp.fps);
                            } else {
                                if (_vp.timer) { clearInterval(_vp.timer); _vp.timer = null; }
                            }
                        }

                        function vpSeekToPos(e) {
                            if (!_vp.frames.length) return;
                            var bar = document.getElementById('vp-progress-bg');
                            var rect = bar.getBoundingClientRect();
                            var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                            _vp.idx = Math.round(pct * (_vp.frames.length - 1));
                            document.getElementById('video-slideshow').src = _vp.frames[_vp.idx];
                            vpUpdateUI();
                        }
                        function vpSeekStart(e) { _vp.seeking = true; vpSeekToPos(e); }
                        function vpSeekMove(e)  { if (_vp.seeking) vpSeekToPos(e); }
                        function vpSeekEnd(e)   { _vp.seeking = false; }

                        function vpSetVolume(v) { _vp.volume = v / 100; }

                        function vpDownload() {
                            if (!_vp.frames.length) return;
                            var btn = document.getElementById('vp-download-btn');
                            btn.textContent = 'Preparing...';
                            btn.disabled = true;
                            var count = 0;
                            _vp.frames.forEach(function(dataUrl, i) {
                                var a = document.createElement('a');
                                a.href = dataUrl;
                                a.download = 'frame_' + String(i + 1).padStart(3, '0') + '.jpg';
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                count++;
                            });
                            setTimeout(function() {
                                btn.innerHTML = '&#11015; Download';
                                btn.disabled = false;
                            }, 1500);
                        }

                        function vpInit(frames, fps) {
                            _vp.frames = frames; _vp.fps = fps || 5;
                            _vp.idx = 0; _vp.playing = false;
                            if (_vp.timer) { clearInterval(_vp.timer); _vp.timer = null; }
                            var slide = document.getElementById('video-slideshow');
                            slide.style.display = 'block';
                            slide.src = frames[0];
                            document.getElementById('vp-play-btn').innerHTML = '&#9654;';
                            document.getElementById('vp-error').style.display = 'none';
                            vpUpdateUI();
                        }

                        function closeVideoResult() {
                            if (_vp.timer) { clearInterval(_vp.timer); _vp.timer = null; }
                            _vp.playing = false; _vp.frames = [];
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.src = ''; slide.style.display = 'none'; }
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                        }

                        // legacy stubs (unused but referenced in old code)
                        function toggleVideoPlay() { vpTogglePlay(); }
                        function seekVideo(e) { vpSeekToPos(e); }'''

if old_funcs in content:
    content = content.replace(old_funcs, new_funcs)
    print("Functions replaced")
else:
    print("Functions not found exactly - doing targeted replace")
    # Replace just the key functions
    content = content.replace('function generateVideoReport() {}', new_funcs)
    print("Inserted via generateVideoReport stub")

# ── Update both success handlers to call vpInit ─────────────────────────────
# Handler 1 (DOMContentLoaded)
content = content.replace(
    '''// Custom player - no autoplay
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

# Handler 2 (form submit)
content = content.replace(
    '''                    window._slideshowFrames = frames;
                    window._slideshowFps = fps;
                    window._slideshowFrameIdx = 0;
                    window._slideshowPlaying = false;
                    if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }

                    document.getElementById("video-player-controls").style.display = "block";
                    document.getElementById("video-play-btn").innerHTML = "&#9654;";
                    document.getElementById("video-progress-fill").style.width = "0%";
                    document.getElementById("video-time-label").textContent = "1 / " + frames.length + " frames";''',
    '                    vpInit(frames, fps);'
)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("All done!")
