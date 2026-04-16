with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove the first of the two consecutive <!-- video script --> <script> blocks
count = 0
for i, line in enumerate(lines):
    if '<!-- video script -->' in line:
        count += 1
        if count == 2:
            # Remove this duplicate comment + script tag (next non-empty line)
            del lines[i]  # remove the comment
            # remove following blank lines and the <script> tag
            while i < len(lines) and lines[i].strip() in ('', '<script>'):
                del lines[i]
            print("Removed duplicate at line %d" % (i+1))
            break

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")
