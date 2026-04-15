f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# Fix webcam container - find exact text
old = '                    <div align="center" style="position: relative; display: inline-block;">\n                        <video id="webcam-video" width="640" height="480" autoplay muted\n                            style="display: none; border: 2px solid white; border-radius: 10px; margin-top: 20px;"></video>\n                        <canvas id="detection-overlay" width="640" height="480"\n                            style="display'

idx = c.find(old[:80])
if idx >= 0:
    # Find end of this div block
    end_idx = c.find('</div>', idx) + len('</div>')
    old_block = c[idx:end_idx]
    print("Found block:", repr(old_block[:100]))
    
    new_block = """                    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 20px;">
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
    
    c = c[:idx] + new_block + c[end_idx:]
    print("Webcam container fixed")
else:
    print("FAILED - not found")

# Fix stopDetection to properly work
old_stop = "function stopDetection() {\n                            detectionActive = false;\n                            var btn = document.getElementById('start-detection-btn');\n                            if (btn) {\n                                btn.innerText = 'Start Detection';\n                                btn.setAttribute('onclick', 'startDetection()');\n                            }\n                            var overlay = document.getElementById('detection-overlay');\n                            if (overlay) {\n                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);\n                            }\n                            document.getElementById('webcam-detection-results').style.display = 'none';\n                        }"

if old_stop in c:
    print("stopDetection already correct")
else:
    # Find and replace stopDetection
    i = c.find('function stopDetection()')
    j = c.find('\n                        }', i) + len('\n                        }')
    print("Replacing stopDetection at:", i, j)
    new_stop = """function stopDetection() {
                            detectionActive = false;
                            var btn = document.getElementById('start-detection-btn');
                            if (btn) {
                                btn.innerText = 'Start Detection';
                                btn.setAttribute('onclick', 'startDetection()');
                            }
                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                            var wr = document.getElementById('webcam-detection-results');
                            if (wr) wr.style.display = 'none';
                        }"""
    c = c[:i] + new_stop + c[j:]
    print("stopDetection fixed")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("File saved")
