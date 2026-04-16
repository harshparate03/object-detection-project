with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the Generate Report video button entirely
content = content.replace(
    '                        <!-- Generate Report Button -->\n\n                        <button id="generate-report-video-button" class="btn-default btn-large" style="display: none;"\n                            onclick="generateVideoReport()">Generate Report</button>',
    ''
)

# 2. Add generateVideoReport as empty stub to fix ReferenceError
# Also add pause/play controls to the slideshow
# Find the closeVideoResult function and add after it
old_close = '''                        function closeVideoResult() {
                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.src = ''; slide.style.display = 'none'; }
                            var v = document.getElementById('annotated-video');
                            v.pause();
                            document.getElementById('video-source').src = '';
                            v.load();
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                            document.getElementById('generate-report-video-button').style.display = 'none';
                        }'''

new_close = '''                        function closeVideoResult() {
                            if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                            var slide = document.getElementById('video-slideshow');
                            if (slide) { slide.src = ''; slide.style.display = 'none'; }
                            var v = document.getElementById('annotated-video');
                            v.pause();
                            document.getElementById('video-source').src = '';
                            v.load();
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                        }

                        // Slideshow pause/play
                        var _slideshowPaused = false;
                        function toggleSlideshow() {
                            _slideshowPaused = !_slideshowPaused;
                            var btn = document.getElementById('slideshow-toggle-btn');
                            if (_slideshowPaused) {
                                if (window._videoInterval) { clearInterval(window._videoInterval); window._videoInterval = null; }
                                if (btn) btn.textContent = '▶ Play';
                            } else {
                                var slide = document.getElementById('video-slideshow');
                                if (slide && window._slideshowFrames) {
                                    if (window._videoInterval) clearInterval(window._videoInterval);
                                    var idx = window._slideshowFrameIdx || 0;
                                    window._videoInterval = setInterval(function() {
                                        idx = (idx + 1) % window._slideshowFrames.length;
                                        window._slideshowFrameIdx = idx;
                                        slide.src = window._slideshowFrames[idx];
                                    }, 1000 / (window._slideshowFps || 5));
                                }
                                if (btn) btn.textContent = '⏸ Pause';
                            }
                        }

                        function generateVideoReport() {}'''

if old_close in content:
    content = content.replace(old_close, new_close)
    print("closeVideoResult replaced")
else:
    # fallback - just add stub
    content = content.replace(
        'function closeVideoResult()',
        'function generateVideoReport() {}\n                        function closeVideoResult()'
    )
    print("Added generateVideoReport stub")

# 3. Add pause/play button to the video container and store frames globally
# Update the DOMContentLoaded handler to store frames in window vars
content = content.replace(
    '''                                            resultContainer.style.display = "block";

                                            const slideImg = document.getElementById("video-slideshow");
                                            slideImg.style.display = "block";
                                            slideImg.src = frames[0];

                                            if (window._videoInterval) clearInterval(window._videoInterval);
                                            window._videoInterval = setInterval(() => {
                                                frameIdx = (frameIdx + 1) % frames.length;
                                                slideImg.src = frames[frameIdx];
                                            }, 1000 / fps);''',
    '''                                            resultContainer.style.display = "block";

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
)

# 4. Add pause/play button inside the video container (after the close button)
content = content.replace(
    '''                            <button onclick="closeVideoResult()" style="position: absolute; top: 5px; right: 5px; background: red; color: white; border: none; border-radius: 50%; width: 32px; height: 32px; font-size: 18px; cursor: pointer; z-index: 10;">&times;</button>
                            <h4>Processed Video:</h4>''',
    '''                            <button onclick="closeVideoResult()" style="position: absolute; top: 5px; right: 5px; background: red; color: white; border: none; border-radius: 50%; width: 32px; height: 32px; font-size: 18px; cursor: pointer; z-index: 10;">&times;</button>
                            <h4>Processed Video:</h4>
                            <button id="slideshow-toggle-btn" onclick="toggleSlideshow()" class="btn-default btn-small" style="margin-bottom:10px;">⏸ Pause</button>'''
)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("All fixes applied")
