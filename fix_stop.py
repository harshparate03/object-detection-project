f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

i = c.find('function stopWebcam')
j = c.find('// function takeScreenshot', i)
old = c[i:j].rstrip()

new = """function stopWebcam() {
                            if (webcamStream) {
                                webcamStream.getTracks().forEach(function(t) { t.stop(); });
                                webcamStream = null;
                            }
                            var v = document.getElementById('webcam-video');
                            if (v) { v.srcObject = null; v.style.display = 'none'; }
                            document.getElementById('webcam-feed').src = '';
                            document.getElementById('webcam-buttons').style.display = 'none';
                        }"""

print("OLD:", repr(old[:50]))
c = c[:i] + new + '\n\n\n' + c[j:]
open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("Fixed stopWebcam")
