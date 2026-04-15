f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

idx = c.find('sourceElement.src = videoUrl')
print("Found at:", idx)
print(repr(c[idx-100:idx+200]))
