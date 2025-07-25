pps = [
    # 🔵 Social Media & Communication
    ('Instagram', r'C:\Users\Piyush sharma\AppData\Local\Instagram\Instagram.exe'),
    ('Twitter', r'C:\Users\Piyush sharma\AppData\Local\Twitter\Twitter.exe'),
    ('WhatsApp Desktop', r'C:\Users\Piyush sharma\AppData\Local\WhatsApp\WhatsApp.exe'),
    ('Telegram', r'C:\Users\Piyush sharma\AppData\Roaming\Telegram Desktop\Telegram.exe'),
    ('Discord', r'C:\Users\Piyush sharma\AppData\Local\Discord\Update.exe'),
    ('Facebook Messenger', r'C:\Users\Piyush sharma\AppData\Local\Facebook\Messenger.exe'),

    # 🎵 Media & Streaming
    ('Spotify', r'C:\Users\Piyush sharma\AppData\Roaming\Spotify\Spotify.exe'),
    ('Netflix App', r'C:\Users\Piyush sharma\AppData\Local\Netflix\Netflix.exe'),
    ('VLC Media Player', r'C:\Program Files\VideoLAN\VLC\vlc.exe'),
    ('Windows Media Player', r'C:\Program Files\Windows Media Player\wmplayer.exe'),

    # 🌐 Web Browsers
    ('Google Chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
    ('Microsoft Edge', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'),
    ('Mozilla Firefox', r'C:\Program Files\Mozilla Firefox\firefox.exe'),
    ('Brave Browser', r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'),

    # 💻 Development Tools
    ('Visual Studio Code', r'C:\Users\Piyush sharma\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
    ('Android Studio', r'C:\Program Files\Android\Android Studio\bin\studio64.exe'),
    ('Git Bash', r'C:\Program Files\Git\git-bash.exe'),
    ('XAMPP', r'C:\xampp\xampp-control.exe'),
    ('Sublime Text', r'C:\Program Files\Sublime Text\sublime_text.exe'),
    ('Notepad++', r'C:\Program Files\Notepad++\notepad++.exe'),

    # 📁 System Utilities
    ('Task Manager', r'C:\Windows\System32\Taskmgr.exe'),
    ('Command Prompt', r'C:\Windows\System32\cmd.exe'),
    ('Control Panel', r'C:\Windows\System32\control.exe'),
    ('Settings', r'C:\Windows\ImmersiveControlPanel\SystemSettings.exe'),
    ('Snipping Tool', r'C:\Windows\System32\SnippingTool.exe'),
    ('Registry Editor', r'C:\Windows\regedit.exe'),
    ('Calculator', r'C:\Windows\System32\calc.exe'),

    # 🛠️ Productivity / Design
    ('OBS Studio', r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'),
    ('Figma', r'C:\Users\Piyush sharma\AppData\Local\Figma\Figma.exe'),
    ('Zoom', r'C:\Users\Piyush sharma\AppData\Roaming\Zoom\bin\Zoom.exe'),
    ('Notion', r'C:\Users\Piyush sharma\AppData\Local\Programs\Notion\Notion.exe'),
    ('Adobe Photoshop', r'C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe'),
    ('Adobe Illustrator', r'C:\Program Files\Adobe\Adobe Illustrator 2023\Support Files\Contents\Windows\Illustrator.exe'),
    ('MS Word', r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'),
    ('MS Excel', r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'),
    ('MS PowerPoint', r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE')
]

# Insert updated applications, removing duplicates by name
for name, path in apps:
    try:
        
        cursor.execute("INSERT INTO sys_command VALUES (NULL, ?, ?)", (name, path))
    except Exception as e:
        print(f"Failed to insert {name}: {e}")

# Commit and close connection
con.commit()