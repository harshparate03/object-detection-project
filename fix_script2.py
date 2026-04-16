with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 434 and 435 (0-indexed: 433 and 434) are both <script>
# Remove the extra one
new_lines = []
prev_was_script = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '<script>':
        if prev_was_script:
            print(f"Removed duplicate <script> at line {i+1}")
            continue
        prev_was_script = True
    else:
        prev_was_script = False
    new_lines.append(line)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done")
