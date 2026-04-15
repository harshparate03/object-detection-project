content = open('vision/templates/dashboard.html', encoding='utf-8').read()

old = "                sourceElement.src = videoUrl;\n                videoElement.load();\n                videoElement.play().catch(e => console.error(\"Play error:\", e));\n                document.getElementById(\"annotated-video-container\").style.display = \"block\";"

new = "                document.getElementById(\"annotated-video-container\").style.display = \"block\";\n                sourceElement.src = videoUrl;\n                videoElement.load();"

if old in content:
    content = content.replace(old, new)
    print("Fixed: video play error resolved")
else:
    print("FAILED")
    i = content.find('sourceElement.src')
    print(repr(content[i:i+200]))

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(content)
print("done")
