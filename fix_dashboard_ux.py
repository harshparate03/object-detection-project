f = open('vision/templates/dashboard.html', encoding='utf-8')
c = f.read()
f.close()

# ============================================================
# FIX 1: Add section IDs and X buttons to result containers
# ============================================================

# Image result - add id and X button
old_img = """                        <!-- Placeholder for Annotated Image -->
                        <div id="annotated-image-container"
                            style="margin-top: 20px; display: none; text-align: center;">
                            <h4>Processed Image:</h4>
                            <img id="annotated-image" src="" alt="Annotated Image"
                                style="max-width: 100%; height: auto;" />
                        </div>"""

new_img = """                        <!-- Placeholder for Annotated Image -->
                        <div id="annotated-image-container" style="margin-top: 20px; display: none; text-align: center; position: relative;">
                            <button onclick="closeImageResult()" style="position: absolute; top: 0; right: 0; background: red; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; font-size: 16px; cursor: pointer; z-index: 10;">&times;</button>
                            <h4>Processed Image:</h4>
                            <img id="annotated-image" src="" alt="Annotated Image" style="max-width: 80%; height: auto; border: 2px solid white; border-radius: 10px;" />
                        </div>"""

if old_img in c:
    c = c.replace(old_img, new_img)
    print("FIX 1: Image X button added")
else:
    print("FIX 1 FAILED")

# Video result - add X button
old_vid = """                        <!-- Placeholder for Annotated Video -->
                        <div id="annotated-video-container" style="display: none;">
                            <video id="annotated-video" controls>
                                <source id="video-source" src="">
                                Your browser does not support the video tag.
                            </video>
                        </div>"""

new_vid = """                        <!-- Placeholder for Annotated Video -->
                        <div id="annotated-video-container" style="display: none; position: relative; text-align: center; margin-top: 20px;">
                            <button onclick="closeVideoResult()" style="position: absolute; top: 0; right: 0; background: red; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; font-size: 16px; cursor: pointer; z-index: 10;">&times;</button>
                            <h4>Processed Video:</h4>
                            <video id="annotated-video" controls style="width: 80%; max-width: 900px; height: auto; border: 2px solid white; border-radius: 10px;">
                                <source id="video-source" src="">
                                Your browser does not support the video tag.
                            </video>
                        </div>"""

if old_vid in c:
    c = c.replace(old_vid, new_vid)
    print("FIX 2: Video X button added")
else:
    print("FIX 2 FAILED")

# ============================================================
# FIX 3: Add section anchor IDs to detection section
# ============================================================
old_sec = """                        <div id="detection-section" class="button-group mt--50 text-center"
                            style="display: flex; flex-direction: column; align-items: center; gap: 20px;"
                            id="upload_section">"""
new_sec = """                        <div id="detection-section" class="button-group mt--50 text-center"
                            style="display: flex; flex-direction: column; align-items: center; gap: 20px;">"""
if old_sec in c:
    c = c.replace(old_sec, new_sec)
    print("FIX 3: Duplicate id removed")

# ============================================================
# FIX 4: Add scroll + close functions to image upload JS
# ============================================================
old_img_success = """                        if (data.status === 'success') {
                            // Show the processed image
                            document.getElementById('annotated-image').src = data.annotated_image_url;
                            document.getElementById('annotated-image-container').style.display = 'block';

                            // Display detected objects below the image
                            const detectionList = document.getElementById('detection-list');
                            detectionList.innerHTML = ''; // Clear previous detections

                            if (data.detected_objects.length > 0) {
                                document.getElementById('detection-results').style.display = 'block';
                                data.detected_objects.forEach(obj => {
                                    let listItem = document.createElement('li');
                                    listItem.textContent = `${obj.label}: ${obj.count}`;
                                    detectionList.appendChild(listItem);
                                });
                            } else {
                                document.getElementById('detection-results').style.display = 'none';
                            }

                            // Show generate report button
                            document.getElementById('generate-report-button').style.display = 'inline-block';"""

new_img_success = """                        if (data.status === 'success') {
                            // Show the processed image
                            document.getElementById('annotated-image').src = data.annotated_image_url;
                            document.getElementById('annotated-image-container').style.display = 'block';

                            // Display detected objects below the image
                            const detectionList = document.getElementById('detection-list');
                            detectionList.innerHTML = ''; // Clear previous detections

                            if (data.detected_objects.length > 0) {
                                document.getElementById('detection-results').style.display = 'block';
                                data.detected_objects.forEach(obj => {
                                    let listItem = document.createElement('li');
                                    listItem.textContent = `${obj.label}: ${obj.count}`;
                                    detectionList.appendChild(listItem);
                                });
                            } else {
                                document.getElementById('detection-results').style.display = 'none';
                            }

                            // Show generate report button
                            document.getElementById('generate-report-button').style.display = 'inline-block';

                            // Auto-scroll to result
                            document.getElementById('annotated-image-container').scrollIntoView({ behavior: 'smooth', block: 'center' });"""

if old_img_success in c:
    c = c.replace(old_img_success, new_img_success)
    print("FIX 4: Image auto-scroll added")
else:
    print("FIX 4 FAILED")

# ============================================================
# FIX 5: Add scroll to video result
# ============================================================
old_vid_show = """                    document.getElementById("annotated-video-container").style.display = "block";
                    sourceElement.src = videoUrl;
                    videoElement.load();"""
new_vid_show = """                    document.getElementById("annotated-video-container").style.display = "block";
                    sourceElement.src = videoUrl;
                    videoElement.load();
                    // Auto-scroll to video result
                    setTimeout(function() {
                        document.getElementById('annotated-video-container').scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 300);"""
if old_vid_show in c:
    c = c.replace(old_vid_show, new_vid_show)
    print("FIX 5: Video auto-scroll added")
else:
    print("FIX 5 FAILED")

# ============================================================
# FIX 6: Add scroll to webcam section when opened
# ============================================================
old_wc = """                                document.getElementById('detection-overlay').style.display = 'none';
                                document.getElementById('webcam-buttons').style.display = 'inline-block';"""
new_wc = """                                document.getElementById('detection-overlay').style.display = 'none';
                                document.getElementById('webcam-buttons').style.display = 'inline-block';
                                // Auto-scroll to webcam section
                                setTimeout(function() {
                                    document.getElementById('webcam-video').scrollIntoView({ behavior: 'smooth', block: 'center' });
                                }, 300);"""
if old_wc in c:
    c = c.replace(old_wc, new_wc)
    print("FIX 6: Webcam auto-scroll added")
else:
    print("FIX 6 FAILED")

# ============================================================
# FIX 7: Add closeImageResult and closeVideoResult functions
# ============================================================
old_placeholder = "// placeholder - real handleImageUpload is defined below\n                    </script>"
new_placeholder = """// Close functions for result panels
                        function closeImageResult() {
                            document.getElementById('annotated-image-container').style.display = 'none';
                            document.getElementById('annotated-image').src = '';
                            document.getElementById('detection-results').style.display = 'none';
                            document.getElementById('detection-list').innerHTML = '';
                            document.getElementById('generate-report-button').style.display = 'none';
                        }
                        function closeVideoResult() {
                            var v = document.getElementById('annotated-video');
                            v.pause();
                            document.getElementById('video-source').src = '';
                            v.load();
                            document.getElementById('annotated-video-container').style.display = 'none';
                            document.getElementById('detection-results-video').style.display = 'none';
                            document.getElementById('generate-report-video-button').style.display = 'none';
                        }
                    </script>"""
if old_placeholder in c:
    c = c.replace(old_placeholder, new_placeholder)
    print("FIX 7: closeImageResult and closeVideoResult added")
else:
    print("FIX 7 FAILED")

open('vision/templates/dashboard.html', 'w', encoding='utf-8').write(c)
print("\nAll fixes applied.")
