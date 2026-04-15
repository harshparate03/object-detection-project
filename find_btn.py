import sys
f = open('vision/templates/index.html', encoding='utf-8')
c = f.read()
f.close()

i = c.lower().find('get started free')
sys.stdout.buffer.write(repr(c[i-300:i+100]).encode('utf-8') + b'\n')
