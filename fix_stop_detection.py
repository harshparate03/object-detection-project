f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

i = c.find('function stopDetection()')
j = c.find('\n                        }', i) + len('\n                        }')
print("Old stopDetection:", repr(c[i:j]))

new_stop = """function stopDetection() {
                            detectionActive = false;
                            // Reset button
                            var btn = document.getElementById('start-detection-btn');
                            if (btn) {
                                btn.innerText = 'Start Detection';
                                btn.setAttribute('onclick', 'startDetection()');
                            }
                            // Hide and clear overlay canvas completely
                            var overlay = document.getElementById('detection-overlay');
                            if (overlay) {
                                overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
                                overlay.style.display = 'none';
                            }
                            // Hide detection results
                            var wr = document.getElementById('webcam-detection-results');
                            if (wr) wr.style.display = 'none';
                        }"""

c = c[:i] + new_stop + c[j:]
print("stopDetection fixed")

# Also fix openWebcam to show overlay again when detection starts
old_open = "                                overlay.style.display = 'block';\r\n                                overlay.width = 640;\r\n                                overlay.height = 480;"
new_open = "                                overlay.style.display = 'none'; // hidden until detection starts\r\n                                overlay.width = 640;\r\n                                overlay.height = 480;"
if old_open in c:
    c = c.replace(old_open, new_open)
    print("openWebcam: overlay hidden by default")

# Fix startDetection to show overlay when detection starts
old_start = "                            detectionActive = true;\r\n                            var btn = document.getElementById('start-detection-btn');"
new_start = "                            detectionActive = true;\r\n                            // Show overlay when detection starts\r\n                            var ov = document.getElementById('detection-overlay');\r\n                            if (ov) ov.style.display = 'block';\r\n                            var btn = document.getElementById('start-detection-btn');"
if old_start in c:
    c = c.replace(old_start, new_start)
    print("startDetection: shows overlay")
else:
    print("startDetection pattern not found")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("File saved")
