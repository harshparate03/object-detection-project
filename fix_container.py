with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find annotated-video-container div
start = None
end = None
for i, line in enumerate(lines):
    if 'id="annotated-video-container"' in line and start is None:
        start = i - 1  # include the comment line before
        depth = 0
        for j in range(i, min(i + 40, len(lines))):
            depth += lines[j].count('<div') - lines[j].count('</div>')
            if depth <= 0 and j > i:
                end = j
                break
        break

print(f"Container: lines {start} to {end}")

new_html = '''                        <!-- Processed Video Player -->
                        <div id="annotated-video-container" style="display:none; margin-top:24px; width:100%; max-width:920px; margin-left:auto; margin-right:auto;">
                            <div style="background:#111827; border:1px solid #374151; border-radius:14px; overflow:hidden; box-shadow:0 8px 32px rgba(0,0,0,0.5);">

                                <!-- Header -->
                                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px; border-bottom:1px solid #1f2937;">
                                    <span style="color:#9ca3af; font-size:13px; font-weight:600;">&#127909; PROCESSED VIDEO</span>
                                    <button onclick="closeVideoResult()" title="Close" style="background:none; border:1px solid #374151; color:#9ca3af; border-radius:6px; width:28px; height:28px; cursor:pointer; font-size:14px;">&times;</button>
                                </div>

                                <!-- Frame display -->
                                <div style="background:#000; min-height:180px; display:flex; align-items:center; justify-content:center;">
                                    <img id="video-slideshow" src="" alt="Video frame" style="width:100%; max-height:480px; object-fit:contain; display:none;">
                                    <div id="vp-error" style="display:none; color:#ef4444; font-size:14px; padding:20px;">&#9888; Could not load video.</div>
                                </div>

                                <!-- Controls -->
                                <div style="padding:12px 16px; background:#111827;">
                                    <!-- Progress bar -->
                                    <div style="margin-bottom:10px; padding:4px 0; cursor:pointer;"
                                        onmousedown="vpSeekStart(event)" onmousemove="vpSeekMove(event)"
                                        onmouseup="vpSeekEnd(event)" onmouseleave="vpSeekEnd(event)">
                                        <div id="vp-progress-bg" style="background:#374151; border-radius:99px; height:5px; position:relative;">
                                            <div id="vp-progress-fill" style="background:linear-gradient(90deg,#8b5cf6,#06b6d4); height:100%; border-radius:99px; width:0%; pointer-events:none;"></div>
                                            <div id="vp-thumb" style="position:absolute; top:50%; left:0%; transform:translate(-50%,-50%); width:13px; height:13px; background:#fff; border-radius:50%; pointer-events:none; box-shadow:0 0 4px rgba(0,0,0,0.6);"></div>
                                        </div>
                                    </div>
                                    <!-- Buttons -->
                                    <div style="display:flex; align-items:center; gap:10px;">
                                        <button id="vp-play-btn" onclick="vpTogglePlay()" title="Play / Pause"
                                            style="background:#8b5cf6; border:none; color:#fff; border-radius:50%; width:38px; height:38px; font-size:16px; cursor:pointer; flex-shrink:0;">&#9654;</button>
                                        <span id="vp-time" style="color:#d1d5db; font-size:12px; font-family:monospace; white-space:nowrap; min-width:90px;">0:00 / 0:00</span>
                                        <div style="flex:1;"></div>
                                        <span style="color:#9ca3af; font-size:14px;">&#128266;</span>
                                        <input id="vp-volume" type="range" min="0" max="100" value="80"
                                            oninput="vpSetVolume(this.value)"
                                            style="width:70px; accent-color:#8b5cf6; cursor:pointer;">
                                        <button id="vp-download-btn" onclick="vpDownload()" title="Download frames"
                                            style="background:none; border:1px solid #374151; color:#9ca3af; border-radius:8px; padding:5px 10px; font-size:12px; cursor:pointer;">&#11015; Download</button>
                                    </div>
                                </div>
                            </div>
                        </div>
'''

if start is not None and end is not None:
    lines[start:end+1] = [new_html]
    print("Replaced successfully")

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
