import sys
f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

idx = c.find('sourceElement.src = videoUrl')
snippet = c[idx-100:idx+300]
sys.stdout.buffer.write(repr(snippet).encode('utf-8') + b'\n')

# Fix: add scroll after video loads
old = "                    document.getElementById(\"annotated-video-container\").style.display = \"block\";\n                    sourceElement.src = videoUrl;\n                    videoElement.load();"
new = "                    document.getElementById(\"annotated-video-container\").style.display = \"block\";\n                    sourceElement.src = videoUrl;\n                    videoElement.load();\n                    setTimeout(function() { document.getElementById('annotated-video-container').scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 300);"

if old in c:
    c = c.replace(old, new)
    print("Video scroll fixed")
else:
    print("Pattern not found, trying DOMContentLoaded version")
    old2 = "                                                videoSource.src = data.processed_video_url;\n                                                processedVideo.load();\n                                                processedVideo.play().catch(error => console.error(\"Play error:\", error));\n\n                                                processedVideoContainer.style.display = \"block\"; // \u2705 Show video container\n                                                processedVideo.style.display = \"block\"; // \u2705 Ensure video is visible"
    new2 = "                                                videoSource.src = data.processed_video_url;\n                                                processedVideo.load();\n\n                                                processedVideoContainer.style.display = \"block\";\n                                                processedVideo.style.display = \"block\";\n                                                setTimeout(function() { processedVideoContainer.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 300);"
    if old2 in c:
        c = c.replace(old2, new2)
        print("DOMContentLoaded video scroll fixed")
    else:
        print("Both patterns failed")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("done")
