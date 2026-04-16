with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find script block containing closeVideoResult starting around line 448
script_start = None
script_end = None

for i, line in enumerate(lines):
    if '<script>' in line and i > 440 and i < 460:
        script_start = i
        for j in range(i, min(i+400, len(lines))):
            if '</script>' in lines[j] and j > i + 50:
                script_end = j
                break
        break

print("Script block: lines %d to %d" % (script_start, script_end))

new_script = '''                    <script>
                        function closeImageResult() {
                            document.getElementById('annotated-image-container').style.display = 'none';
                            document.getElementById('annotated-image').src = '';
                            document.getElementById('detection-results').style.display = 'none';
                            document.getElementById('detection-list').innerHTML = '';
                            document.getElementById('generate-report-button').style.display = 'none';
                        }

                        var _vp = { frames:[], fps:5, idx:0, playing:false, timer:null, seeking:false };

                        function vpFmtTime(sec) {
                            var m = Math.floor(sec/60), s = Math.floor(sec%60);
                            return m + ':' + (s<10?'0':'') + s;
                        }

                        function vpUpdateUI() {
                            var total = _vp.frames.length;
                            var pct = total > 1 ? (_vp.idx / (total-1)) * 100 : 0;
                            var fill = document.getElementById('vp-progress-fill');
                            var thumb = document.getElementById('vp-thumb');
                            var time  = document.getElementById('vp-time');
                            if (fill)  fill.style.width = pct + '%';
                            if (thumb) thumb.style.left = pct + '%';
                            if (time)  time.textContent = vpFmtTime(_vp.idx/_vp.fps) + ' / ' + vpFmtTime((total-1)/_vp.fps);
                        }

                        function vpTogglePlay() {
                            if (!_vp.frames.length) return;
                            _vp.playing = !_vp.playing;
                            var btn = document.getElementById('vp-play-btn');
                            if (btn) btn.innerHTML = _vp.playing ? '&#9646;&#9646;' : '&#9654;';
                            if (_vp.playing) {
                                if (_vp.idx >= _vp.frames.length - 1) _vp.idx = 0;
                                if (_vp.timer) clearInterval(_vp.timer);
                                _vp.timer = setInterval(function() {
                                    _vp.idx++;
                                    if (_vp.idx >= _vp.frames.length) {
                                        _vp.idx = _vp.frames.length - 1;
                                        clearInterval(_vp.timer); _vp.timer = null;
                                        _vp.playing = false;
                                        var b = document.getElementById('vp-play-btn');
                                        if (b) b.innerHTML = '&#9654;';
                                    }
                                    var slide = document.getElementById('video-slideshow');
                                    if (slide) slide.src = _vp.frames[_vp.idx];
                                    vpUpdateUI();
                                }, 1000 / _vp.fps);
                            } else {
                                if (_vp.timer) { clearInterval(_vp.timer); _vp.timer = null; }
                            }
                        }

                        function vpSeekToPos(e) {
                            if (!_vp.frames.length) return;
                            var bar = document.getElementById('vp-progress-bg');
                            if (!bar) return;
                            var rect = bar.getBoundingClientRect();
                            var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                            _vp.idx = Math.round(pct * (_vp.frames.length - 1));
                            var slide = document.getElementById('video-slideshow');
                            if (slide) slide.src = _vp.frames[_vp.idx];
                            vpUpdateUI();
                        }
                        function vpSeekStart(e) { _vp.seeking = true; vpSeekToPos(e); }
                        function vpSeekMove(e)  { if (_vp.seeking) vpSeekToPos(e); }
                        function vpSeekEnd(e)   { _vp.seeking = false; }
                        function vpSetVolume(v) {}

                        function vpDownload() {
                            if (!_vp.frames.length) return;
                            var btn = document.getElementById('vp-download-btn');
                            if (btn) { btn.textContent = 'Preparing...'; btn.disabled = true; }
                            _vp.frames.forEach(function(dataUrl, i) {
                                var a = document.createElement('a');
                                a.href = dataUrl;
                                a.download = 'frame_' + String(i+1).padStart(3,'0') + '.jpg';
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                            });
                            setTimeout(function() {
                                if (btn) { btn.innerHTML = '&#11015; Download'; btn.disabled = false; }
                            }, 1500);
                        }

                        function vpInit(frames, fps) {
                            if (!frames || !frames.length) return;
                            _vp.frames = frames; _vp.fps = fps || 5;
                            _vp.idx = 0; _vp.playing = false;
                            if (_vp.timer) { clearInterval(_vp.timer); _vp.timer = null; }
                            document.getElementById('annotated-video-container').style.display = 'block';
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.style.display = 'block'; slide.src = frames[0]; }
                            var btn = document.getElementById('vp-play-btn');
                            if (btn) btn.innerHTML = '&#9654;';
                            var err = document.getElementById('vp-error');
                            if (err) err.style.display = 'none';
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

                        function generateVideoReport() {}
                        function toggleVideoPlay() { vpTogglePlay(); }
                        function seekVideo(e) { vpSeekToPos(e); }
                    </script>
'''

if script_start is not None and script_end is not None:
    lines[script_start:script_end+1] = [new_script]
    print("Replaced %d lines with clean script block" % (script_end - script_start + 1))
else:
    print("ERROR: could not find script block")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
