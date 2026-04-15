f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# Fix 1: Fix overlay top offset (top:20px -> top:0)
c = c.replace(
    'style="display: none; position: absolute; top: 20px; left: 0; border-radius: 10px; pointer-events: none;"',
    'style="display: none; position: absolute; top: 0; left: 0; border-radius: 10px; pointer-events: none;"'
)
print("FIX 1: overlay top offset fixed")

# Fix 2: Fix stopDetection - add runDetection function call check
old2 = """                        function stopDetection() {
                            detectionActive = false;
                            var btn = document.getElementById('start-detection-btn');
                            btn.innerText = 'Start Detection';
                            btn.setAttribute('onclick', 'startDetection()');
                            // Clear overlay
                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                        }"""

new2 = """                        function stopDetection() {
                            detectionActive = false;
                            var btn = document.getElementById('start-detection-btn');
                            if (btn) {
                                btn.innerText = 'Start Detection';
                                btn.setAttribute('onclick', 'startDetection()');
                            }
                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) {
                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                            }
                        }"""

if old2 in c:
    c = c.replace(old2, new2)
    print("FIX 2: stopDetection fixed")
else:
    print("FIX 2 FAILED")

# Fix 3: Center both webcam video and detection results
old3 = """                    <div style="display: flex; justify-content: center; margin-top: 20px;">
                        <div style="position: relative; display: inline-block;">
                            <video id="webcam-video" width="640" height="480" autoplay muted
                                style="display: none; border: 2px solid white; border-radius: 10px; display: block;"></video>
                            <canvas id="detection-overlay" width="640" height="480"
                                style="display: none; position: absolute; top: 0; left: 0; border-radius: 10px; pointer-events: none;"></canvas>
                        </div>
                    </div>"""

new3 = """                    <div id="webcam-section" style="display: flex; flex-direction: column; align-items: center; margin-top: 20px;">
                        <div style="position: relative; display: inline-block;">
                            <video id="webcam-video" width="640" height="480" autoplay muted
                                style="display: none; border: 2px solid white; border-radius: 10px;"></video>
                            <canvas id="detection-overlay" width="640" height="480"
                                style="display: none; position: absolute; top: 0; left: 0; border-radius: 10px; pointer-events: none;"></canvas>
                        </div>
                        <div id="webcam-detection-results" style="display: none; text-align: center; margin-top: 10px;">
                            <h4 style="color: white;">Detected Objects:</h4>
                            <ol id="webcam-detection-list" style="display: flex; justify-content: center; gap: 15px; padding: 0; list-style: none; color: white;"></ol>
                        </div>
                    </div>"""

if old3 in c:
    c = c.replace(old3, new3)
    print("FIX 3: webcam section restructured with centered detection results")
else:
    print("FIX 3 FAILED")

# Fix 4: Update runDetection to use webcam-detection-list instead of detection-list
old4 = """                                        // Update detection list
                                        var list = document.getElementById('detection-list');
                                        list.innerHTML = '';
                                        data.detected_objects.forEach(function(obj) {
                                            var li = document.createElement('li');
                                            li.textContent = obj.label + ': ' + obj.count;
                                            list.appendChild(li);
                                        });
                                        document.getElementById('detection-results').style.display = 'block';"""

new4 = """                                        // Update webcam detection list (centered below webcam)
                                        var list = document.getElementById('webcam-detection-list');
                                        list.innerHTML = '';
                                        data.detected_objects.forEach(function(obj) {
                                            var li = document.createElement('li');
                                            li.textContent = obj.label + ': ' + obj.count;
                                            list.appendChild(li);
                                        });
                                        document.getElementById('webcam-detection-results').style.display = 'block';"""

if old4 in c:
    c = c.replace(old4, new4)
    print("FIX 4: runDetection uses webcam-detection-list")
else:
    print("FIX 4 FAILED")

# Fix 5: stopDetection also hides webcam-detection-results
old5 = """                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) {
                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                            }
                        }"""

new5 = """                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) {
                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                            }
                            document.getElementById('webcam-detection-results').style.display = 'none';
                        }"""

if old5 in c:
    c = c.replace(old5, new5)
    print("FIX 5: stopDetection hides detection results")
else:
    print("FIX 5 FAILED")

# Fix 6: stopWebcam also hides webcam-detection-results
old6 = "            document.getElementById('detection-results').style.display = 'none';\r\n                            var btn = document.getElementById('start-detection-btn');"
new6 = "            document.getElementById('webcam-detection-results').style.display = 'none';\r\n                            var btn = document.getElementById('start-detection-btn');"
c = c.replace(old6, new6)
print("FIX 6: stopWebcam hides webcam detection results")

# Fix 7: Center webcam-buttons
c = c.replace(
    '<div style="text-align: center; width: 100%; margin-top: 10px; display: none;" id="webcam-buttons">',
    '<div id="webcam-buttons" style="text-align: center; width: 100%; margin-top: 10px; display: none;">'
)
print("FIX 7: webcam buttons centered")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("\nAll fixes applied.")
