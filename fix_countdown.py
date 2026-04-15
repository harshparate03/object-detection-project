f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# Fix 1: Add countdown timer display inside video loader
old_loader = """                        <!-- Loader (Appears while processing the video) -->
                        <div id="ai-loader-video" class="loader-container" style="display: none;">
                            <div class="spinner">
                                <div class="spinner1"></div>
                            </div>
                            <p style="color: white; font-weight: bold; margin-top: 10px;">Processing Video...</p>
                        </div>"""

new_loader = """                        <!-- Loader (Appears while processing the video) -->
                        <div id="ai-loader-video" class="loader-container" style="display: none;">
                            <div class="spinner">
                                <div class="spinner1"></div>
                            </div>
                            <p style="color: white; font-weight: bold; margin-top: 10px;">Processing Video...</p>
                            <p id="video-countdown" style="color: #00e1ff; font-size: 1.2rem; font-weight: bold; margin-top: 5px;"></p>
                        </div>"""

if old_loader in c:
    c = c.replace(old_loader, new_loader)
    print("FIX 1: Countdown display added to loader")
else:
    print("FIX 1 FAILED")

# Fix 2: Find video upload trigger and add scroll + countdown start
# The video upload is triggered by video-upload-input change event
old_video_start = """                                    aiLoader.style.display = \"flex\"; // Show loader
                                    processedVideoContainer.style.display = \"none\";
                                    detectionsList.innerHTML = \"\";
                                    reportButton.style.display = \"none\";"""

new_video_start = """                                    aiLoader.style.display = \"flex\"; // Show loader
                                    processedVideoContainer.style.display = \"none\";
                                    detectionsList.innerHTML = \"\";
                                    reportButton.style.display = \"none\";
                                    // Auto-scroll to processing message
                                    setTimeout(function() {
                                        aiLoader.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                    }, 100);
                                    // Start countdown timer (estimate 2 min for average video)
                                    startVideoCountdown(120);"""

if old_video_start in c:
    c = c.replace(old_video_start, new_video_start)
    print("FIX 2: Scroll + countdown start added to DOMContentLoaded handler")
else:
    print("FIX 2 FAILED")

# Fix 3: Stop countdown when video finishes in DOMContentLoaded handler
old_video_done = """                                            processedVideoContainer.style.display = \"block\"; // \u2705 Show video container
                                                processedVideo.style.display = \"block\"; // \u2705 Ensure video is visible
                                                setTimeout(function() { processedVideoContainer.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 300);"""

new_video_done = """                                            processedVideoContainer.style.display = \"block\";
                                                processedVideo.style.display = \"block\";
                                                stopVideoCountdown();
                                                setTimeout(function() { processedVideoContainer.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 300);"""

if old_video_done in c:
    c = c.replace(old_video_done, new_video_done)
    print("FIX 3: Countdown stop added on video complete")
else:
    print("FIX 3 FAILED")

# Fix 4: Also handle the bottom video script (submit handler)
old_bottom_start = """            document.getElementById(\"ai-loader-video\").style.display = \"block\";

            fetch(\"{% url 'upload_video' %}\", {"""

new_bottom_start = """            document.getElementById(\"ai-loader-video\").style.display = \"flex\";
            // Auto-scroll to processing message
            setTimeout(function() {
                document.getElementById('ai-loader-video').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
            startVideoCountdown(120);

            fetch(\"{% url 'upload_video' %}\", {"""

if old_bottom_start in c:
    c = c.replace(old_bottom_start, new_bottom_start)
    print("FIX 4: Bottom video script scroll + countdown added")
else:
    print("FIX 4 FAILED")

# Fix 5: Add countdown functions before closing </script> of the main image upload script
old_script_end = "    </script>\n    <script src=\"{% static 'js/jspdf.umd.min.js' %}\">"
new_script_end = """    </script>
    <script>
        var countdownInterval = null;

        function startVideoCountdown(seconds) {
            stopVideoCountdown(); // clear any existing
            var remaining = seconds;
            var el = document.getElementById('video-countdown');
            if (!el) return;

            function update() {
                if (remaining <= 0) {
                    el.textContent = 'Almost done...';
                    stopVideoCountdown();
                    return;
                }
                var m = Math.floor(remaining / 60);
                var s = remaining % 60;
                el.textContent = 'Estimated time: ' + (m > 0 ? m + 'm ' : '') + s + 's remaining';
                remaining--;
            }
            update();
            countdownInterval = setInterval(update, 1000);
        }

        function stopVideoCountdown() {
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
            var el = document.getElementById('video-countdown');
            if (el) el.textContent = '';
        }
    </script>
    <script src="{% static 'js/jspdf.umd.min.js' %}">"""

if old_script_end in c:
    c = c.replace(old_script_end, new_script_end)
    print("FIX 5: Countdown functions added")
else:
    print("FIX 5 FAILED")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("\nAll fixes applied.")
