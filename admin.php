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
    $new_content = $_POST['page_content'];
    
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
    <title>IISDR Admin Portal</title>
    <!-- TinyMCE WYSIWYG Editor -->
    <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
    <script>
      tinymce.init({
        selector: '#editor',
        height: 800,
        // IMPORTANT: We want it to allow full HTML editing, including head/body tags, but TinyMCE typically strips them. 
        // For editing full static HTML files safely, we configure TinyMCE to be full page aware.
        plugins: 'advlist autolink lists link image charmap preview anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking table emoticons template help fullpage',
        toolbar: 'undo redo | blocks | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | code | fullpage | preview fullscreen',
        setup: function (editor) {
            editor.on('change', function () {
                editor.save();
            });
        },
        fullpage_default_doctype: "<!DOCTYPE html>",
        verify_html: false,
        valid_children: '+body[style],+body[script]'
      });
    </script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f9f9f9; }
        .header { background: #003d99; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; font-size: 20px; }
        .header a { color: #ff9933; text-decoration: none; font-weight: bold; }
        .container { display: flex; max-width: 1400px; margin: 20px auto; padding: 0 20px; gap: 20px; }
        
        .sidebar { width: 300px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: max-content; }
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
        
        button { background: #ff9933; color: white; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 16px; margin-top: 15px;}
        button:hover { background: #e68a1f; }
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
                    <button type="submit" style="width: 100%;">Upload File</button>
                </form>
                <p style="font-size: 12px; color: #666; margin-top: 10px; line-height: 1.4;">
                    Uploaded files go to the <strong>/uploads/</strong> folder. Copy the URL provided after upload and paste it into the editor when linking or inserting an image.
                </p>
            </div>
        </div>

        <!-- MAIN CONTENT (EDITOR) -->
        <div class="main-content">
            <?php if ($message) echo $message; ?>
            
            <?php if ($selected_file): ?>
                <h3 style="margin-top: 0; color: #003d99;">Editing: <?= htmlspecialchars($selected_file) ?></h3>
                <p style="color: #d32f2f; font-weight: bold; font-size: 14px; background: #fff3f3; padding: 10px; border: 1px solid #ffcdd2;">
                    ⚠️ WARNING: You are editing the raw HTML document directly. The visual editor will try to render the layout, but some scripts/styles might display oddly in edit mode. <strong>Do not delete large structural blocks or javascript at the bottom of the page.</strong> It is best used for fixing typos or updating text content.
                </p>
                <form method="POST">
                    <input type="hidden" name="action" value="save_page">
                    <input type="hidden" name="file_name" value="<?= htmlspecialchars($selected_file) ?>">
                    <!-- Editor text area -->
                    <textarea id="editor" name="page_content"><?= htmlspecialchars($page_content) ?></textarea>
                    
                    <button type="submit">Save Changes to <?= htmlspecialchars($selected_file) ?></button>
                </form>
            <?php else: ?>
                <div style="text-align: center; color: #666; margin-top: 100px;">
                    <h2>Welcome to the IISDR Admin Portal</h2>
                    <p>Select a page from the left sidebar to start editing.</p>
                </div>
            <?php endif; ?>
        </div>
        
    </div>

</body>
</html>
