<?php
session_start();

// --- CONFIGURATION ---
// Change this to your desired password
$ADMIN_PASSWORD = 'iisdr_admin_2026';
$UPLOADS_DIR = __DIR__ . '/uploads';

// Ensure uploads directory exists
if (!file_exists($UPLOADS_DIR)) {
    mkdir($UPLOADS_DIR, 0755, true);
}

// --- AUTHENTICATION ---
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: admin.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login_password'])) {
    if ($_POST['login_password'] === $ADMIN_PASSWORD) {
        $_SESSION['authenticated'] = true;
        header("Location: admin.php");
        exit;
    } else {
        $login_error = "Incorrect password!";
    }
}

if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    // Show Login Page
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>IISDR Admin Portal - Login</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
            input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background: #003d99; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background: #002d77; }
            .error { color: red; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>IISDR Admin Portal</h2>
            <?php if (isset($login_error)) echo "<div class='error'>$login_error</div>"; ?>
            <form method="POST">
                <input type="password" name="login_password" placeholder="Enter Admin Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// --- LOGIC: HANDLE FILE SAVE ---
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'save_page') {
    $file_to_save = $_POST['file_name'];
    $new_content = $_POST['page_content']; // This now comes from our JS structured editor
    
    // Security check: only allow saving to .html files in the current directory
    if (preg_match('/^[a-zA-Z0-9_-]+\.html$/', $file_to_save) && file_exists(__DIR__ . '/' . $file_to_save)) {
        if (file_put_contents(__DIR__ . '/' . $file_to_save, $new_content) !== false) {
            $message = "<div class='success'>Page '$file_to_save' saved successfully!</div>";
        } else {
            $message = "<div class='error'>Error: Could not write to file. Check file permissions.</div>";
        }
    } else {
        $message = "<div class='error'>Error: Invalid file name.</div>";
    }
}

// --- LOGIC: HANDLE FILE UPLOAD ---
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'upload_file') {
    if (isset($_FILES['upload_file']) && $_FILES['upload_file']['error'] === UPLOAD_ERR_OK) {
        $file_tmp = $_FILES['upload_file']['tmp_name'];
        $file_name = preg_replace("/[^a-zA-Z0-9._-]/", "", basename($_FILES['upload_file']['name']));
        $destination = $UPLOADS_DIR . '/' . $file_name;
        
        if (move_uploaded_file($file_tmp, $destination)) {
            // Get public URL path
            $public_url = 'uploads/' . $file_name;
            $message = "<div class='success'>File uploaded successfully! URL to use in images/links: <strong>$public_url</strong></div>";
        } else {
            $message = "<div class='error'>Error: Failed to move uploaded file. Check directory permissions.</div>";
        }
    } else {
        $message = "<div class='error'>Error: Upload failed. Please try again.</div>";
    }
}

// --- GET AVAILABLE PAGES ---
$html_files = glob(__DIR__ . '/*.html');
$pages = [];
foreach ($html_files as $file) {
    $pages[] = basename($file);
}

// --- LOAD SELECTED PAGE ---
$selected_file = isset($_GET['page']) ? $_GET['page'] : '';
$page_content = '';
if ($selected_file && in_array($selected_file, $pages)) {
    $page_content = file_get_contents(__DIR__ . '/' . $selected_file);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IISDR Admin Portal - Structured Editor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f9f9f9; }
        .header { background: #003d99; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; font-size: 20px; }
        .header a { color: #ff9933; text-decoration: none; font-weight: bold; }
        .container { display: flex; max-width: 1600px; margin: 20px auto; padding: 0 20px; gap: 20px; }
        
        .sidebar { width: 300px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: max-content; position: sticky; top: 20px; }
        .sidebar h3 { margin-top: 0; color: #003d99; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .page-list { list-style: none; padding: 0; margin: 0; }
        .page-list li { margin-bottom: 5px; }
        .page-list a { display: block; padding: 8px 10px; text-decoration: none; color: #333; border-radius: 4px; transition: background 0.2s; }
        .page-list a:hover { background: #e3f2fd; color: #003d99; }
        .page-list a.active { background: #003d99; color: white; }
        
        .upload-section { margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee; }
        .upload-section input[type="file"] { margin-bottom: 10px; width: 100%; }
        
        .main-content { flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .success { background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 15px; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin-bottom: 15px; border: 1px solid #f5c6cb; }
        
        /* Structured Editor Styles */
        .editor-section { margin-bottom: 40px; }
        .editor-section h4 { background: #003d99; color: white; padding: 10px; border-radius: 4px; margin-bottom: 10px; }
        .field-group { background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; margin-bottom: 10px; border-radius: 4px; display: flex; gap: 15px; align-items: flex-start; }
        .field-group:hover { border-color: #003d99; }
        .field-preview { width: 150px; flex-shrink: 0; }
        .field-preview img { max-width: 100%; max-height: 100px; border: 1px solid #ccc; object-fit: contain; }
        .field-inputs { flex: 1; display: flex; flex-direction: column; gap: 8px; }
        .field-inputs label { font-size: 12px; font-weight: bold; color: #555; }
        .field-inputs input[type="text"] { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-family: monospace; width: 100%; box-sizing: border-box; }
        .field-inputs textarea { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-family: sans-serif; width: 100%; box-sizing: border-box; resize: vertical; min-height: 60px; }
        
        .save-bar { position: sticky; bottom: 0; background: white; padding: 15px; border-top: 1px solid #ddd; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); display: flex; justify-content: flex-end; z-index: 100; margin-top: 30px;}
        button.save-btn { background: #28a745; color: white; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 16px; }
        button.save-btn:hover { background: #218838; }
        
        button.upload-btn { background: #ff9933; color: white; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 16px; width: 100%; margin-top: 10px;}
        button.upload-btn:hover { background: #e68a1f; }
        
        .tag-badge { display: inline-block; background: #e0e0e0; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-right: 5px; color: #333; }
    </style>
</head>
<body>

    <div class="header">
        <h1>IISDR Admin Portal</h1>
        <a href="?logout=1">Logout</a>
    </div>

    <div class="container">
        
        <!-- SIDEBAR -->
        <div class="sidebar">
            <h3>Select a Page to Edit</h3>
            <ul class="page-list">
                <?php foreach ($pages as $p): ?>
                    <li>
                        <a href="?page=<?= urlencode($p) ?>" class="<?= $p === $selected_file ? 'active' : '' ?>">
                            <?= htmlspecialchars($p) ?>
                        </a>
                    </li>
                <?php endforeach; ?>
            </ul>

            <!-- FILE UPLOAD SECTION -->
            <div class="upload-section">
                <h3>Upload Image / PDF</h3>
                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="action" value="upload_file">
                    <input type="file" name="upload_file" required>
                    <button type="submit" class="upload-btn">Upload File</button>
                </form>
                <p style="font-size: 12px; color: #666; margin-top: 10px; line-height: 1.4;">
                    Uploaded files go to the <strong>/uploads/</strong> folder. Copy the URL provided after upload and paste it into the Image URL or PDF Link URL fields.
                </p>
            </div>
        </div>

        <!-- MAIN CONTENT (STRUCTURED EDITOR) -->
        <div class="main-content">
            <?php if ($message) echo $message; ?>
            
            <?php if ($selected_file): ?>
                <h3 style="margin-top: 0; color: #003d99;">Structured Editing: <?= htmlspecialchars($selected_file) ?></h3>
                <p style="color: #555; font-size: 14px; background: #e3f2fd; padding: 10px; border-radius: 4px; border: 1px solid #b3d4fc;">
                    Every image, link, and text block from the page has been extracted below. Make your changes and click Save at the bottom. Your changes will be injected back into the exact correct layout!
                </p>
                
                <div id="structured-editor-container">
                    <!-- Javascript will render forms here -->
                    <p>Loading editor...</p>
                </div>

                <form method="POST" id="save-form" style="display:none;">
                    <input type="hidden" name="action" value="save_page">
                    <input type="hidden" name="file_name" value="<?= htmlspecialchars($selected_file) ?>">
                    <textarea id="final_page_content" name="page_content"></textarea>
                </form>

            <?php else: ?>
                <div style="text-align: center; color: #666; margin-top: 100px;">
                    <h2>Welcome to the IISDR Admin Portal</h2>
                    <p>Select a page from the left sidebar to start editing.</p>
                </div>
            <?php endif; ?>
        </div>
        
    </div>

    <?php if ($selected_file): ?>
    <script>
        const rawHtml = <?php echo json_encode($page_content); ?>;
        
        // Use DOMParser to safely parse HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(rawHtml, 'text/html');
        
        let elementId = 0;
        const images = [];
        const links = [];
        const texts = [];
        
        // Find all editable elements (ignore scripts, styles, etc)
        // We target body elements specifically to avoid messing with head
        const elements = doc.body.querySelectorAll('img, a, h1, h2, h3, h4, h5, h6, p, span, li');
        
        elements.forEach(el => {
            // Assign a temporary tracking ID
            const id = 'el_' + elementId;
            el.setAttribute('data-admin-id', id);
            
            if (el.tagName === 'IMG') {
                images.push({ id: id, tag: el.tagName, el: el });
            } else if (el.tagName === 'A') {
                // Ignore empty links or purely layout links without text/pdfs
                if (el.innerText.trim() !== '' || el.href.includes('.pdf') || el.href.includes('.jpg')) {
                    links.push({ id: id, tag: el.tagName, el: el });
                }
            } else {
                // Text blocks
                // Only include blocks that actually have text directly inside them (not just child elements)
                let hasDirectText = false;
                for (let i = 0; i < el.childNodes.length; i++) {
                    if (el.childNodes[i].nodeType === 3 && el.childNodes[i].nodeValue.trim().length > 2) {
                        hasDirectText = true;
                        break;
                    }
                }
                
                if (hasDirectText) {
                    texts.push({ id: id, tag: el.tagName, el: el });
                }
            }
            elementId++;
        });

        // Function to render the UI
        function renderUI() {
            const container = document.getElementById('structured-editor-container');
            container.innerHTML = '';
            
            // Render Images
            if (images.length > 0) {
                const sec = document.createElement('div');
                sec.className = 'editor-section';
                sec.innerHTML = `<h4>📸 Images (${images.length})</h4>`;
                
                images.forEach(item => {
                    const group = document.createElement('div');
                    group.className = 'field-group';
                    group.innerHTML = `
                        <div class="field-preview">
                            <img src="${item.el.src}" onerror="this.src='https://via.placeholder.com/150?text=No+Preview'">
                        </div>
                        <div class="field-inputs">
                            <label><span class="tag-badge">IMG</span> Image URL (src)</label>
                            <input type="text" id="input_${item.id}" value="${item.el.getAttribute('src') || ''}">
                        </div>
                    `;
                    sec.appendChild(group);
                    
                    // Add listener
                    setTimeout(() => {
                        document.getElementById('input_' + item.id).addEventListener('input', (e) => {
                            item.el.setAttribute('src', e.target.value);
                            item.el.src = e.target.value; // update absolute for preview
                        });
                    }, 0);
                });
                container.appendChild(sec);
            }
            
            // Render Links
            if (links.length > 0) {
                const sec = document.createElement('div');
                sec.className = 'editor-section';
                sec.innerHTML = `<h4>🔗 Links & PDFs (${links.length})</h4>`;
                
                links.forEach(item => {
                    const group = document.createElement('div');
                    group.className = 'field-group';
                    group.innerHTML = `
                        <div class="field-inputs">
                            <label><span class="tag-badge">A</span> Link URL (href)</label>
                            <input type="text" id="href_${item.id}" value="${item.el.getAttribute('href') || ''}">
                            <label style="margin-top:5px;">Link Text</label>
                            <input type="text" id="text_${item.id}" value="${item.el.innerText}">
                        </div>
                    `;
                    sec.appendChild(group);
                    
                    // Add listener
                    setTimeout(() => {
                        document.getElementById('href_' + item.id).addEventListener('input', (e) => {
                            item.el.setAttribute('href', e.target.value);
                        });
                        document.getElementById('text_' + item.id).addEventListener('input', (e) => {
                            item.el.innerText = e.target.value;
                        });
                    }, 0);
                });
                container.appendChild(sec);
            }
            
            // Render Texts
            if (texts.length > 0) {
                const sec = document.createElement('div');
                sec.className = 'editor-section';
                sec.innerHTML = `<h4>📝 Text Content (${texts.length})</h4>`;
                
                texts.forEach(item => {
                    const group = document.createElement('div');
                    group.className = 'field-group';
                    group.innerHTML = `
                        <div class="field-inputs">
                            <label><span class="tag-badge">${item.tag}</span> Text Content</label>
                            <textarea id="text_${item.id}">${item.el.innerHTML.trim()}</textarea>
                        </div>
                    `;
                    sec.appendChild(group);
                    
                    // Add listener
                    setTimeout(() => {
                        document.getElementById('text_' + item.id).addEventListener('input', (e) => {
                            item.el.innerHTML = e.target.value;
                        });
                    }, 0);
                });
                container.appendChild(sec);
            }
            
            // Add Save Button Bar
            const saveBar = document.createElement('div');
            saveBar.className = 'save-bar';
            saveBar.innerHTML = `<button class="save-btn" onclick="saveChanges()">Save All Changes</button>`;
            container.appendChild(saveBar);
        }
        
        function saveChanges() {
            // Clean up temporary IDs
            const clonedDoc = doc.cloneNode(true);
            const elementsWithId = clonedDoc.querySelectorAll('[data-admin-id]');
            elementsWithId.forEach(el => el.removeAttribute('data-admin-id'));
            
            let finalHtml = clonedDoc.documentElement.outerHTML;
            
            // Preserve Doctype if it existed
            if (rawHtml.toLowerCase().includes('<!doctype html>')) {
                finalHtml = '<!DOCTYPE html>\n' + finalHtml;
            }
            
            // Submit form
            const form = document.getElementById('save-form');
            document.getElementById('final_page_content').value = finalHtml;
            form.submit();
        }

        // Initialize UI
        renderUI();
    </script>
    <?php endif; ?>

</body>
</html>
