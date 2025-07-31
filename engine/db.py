import sqlite3

# Connect to your SQLite DB (it will create one if not exists)
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sys_command (
        name TEXT PRIMARY KEY,
        path TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS web_command (
        name TEXT PRIMARY KEY,
        url TEXT NOT NULL
    )
''')

# List of system apps (name, path)
sys_apps = [
    ('chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
    ('edge', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'),
    ('notepad', r'C:\Windows\system32\notepad.exe'),
    ('calculator', r'C:\Windows\System32\calc.exe'),
    ('paint', r'C:\Windows\system32\mspaint.exe'),
    ('word', r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'),
    ('excel', r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'),
    ('powerpoint', r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE'),
    ('vlc', r'C:\Program Files\VideoLAN\VLC\vlc.exe'),
    ('cmd', r'C:\Windows\System32\cmd.exe'),
    ('control panel', r'C:\Windows\System32\control.exe'),
    ('task manager', r'C:\Windows\System32\Taskmgr.exe'),
    ('settings', r'C:\Windows\System32\djoin.exe'),
    ('explorer', r'C:\Windows\explorer.exe'),
    ('snipping tool', r'C:\Windows\System32\SnippingTool.exe'),
    ('obs', r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'),
    ('visual studio code', r'C:\Users\Piyush sharma\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
    ('pycharm', r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1\bin\pycharm64.exe'),
    ('android studio', r'C:\Program Files\Android\Android Studio\bin\studio64.exe'),
    ('xampp', r'C:\xampp\xampp-control.exe'),
    ('mysql', r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'),
    ('spotify', r'C:\Users\Piyush sharma\AppData\Roaming\Spotify\Spotify.exe'),
    ('discord', r'C:\Users\Piyush sharma\AppData\Local\Discord\Update.exe'),
    ('steam', r'C:\Program Files (x86)\Steam\Steam.exe'),
    ('epic games', r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe')
    # Add up to 50 as needed
]

# List of websites (name, url)
websites = [
    ('google', 'https://www.google.com'),
    ('youtube', 'https://www.youtube.com'),
    ('facebook', 'https://www.facebook.com'),
    ('twitter', 'https://www.twitter.com'),
    ('instagram', 'https://www.instagram.com'),
    ('github', 'https://www.github.com'),
    ('stackoverflow', 'https://stackoverflow.com'),
    ('linkedin', 'https://www.linkedin.com'),
    ('gmail', 'https://mail.google.com'),
    ('amazon', 'https://www.amazon.in'),
    ('flipkart', 'https://www.flipkart.com'),
    ('netflix', 'https://www.netflix.com'),
    ('chatgpt', 'https://chat.openai.com'),
    ('wikipedia', 'https://www.wikipedia.org'),
    ('quora', 'https://www.quora.com'),
    ('zomato', 'https://www.zomato.com'),
    ('swiggy', 'https://www.swiggy.com'),
    ('udemy', 'https://www.udemy.com'),
    ('coursera', 'https://www.coursera.org'),
    ('edx', 'https://www.edx.org'),
    ('canva', 'https://www.canva.com'),
    ('notion', 'https://www.notion.so'),
    ('figma', 'https://www.figma.com'),
    ('codeforces', 'https://codeforces.com'),
    ('leetcode', 'https://leetcode.com'),
    ('hackerrank', 'https://www.hackerrank.com'),
    ('geeksforgeeks', 'https://www.geeksforgeeks.org'),
    ('irctc', 'https://www.irctc.co.in'),
    ('snapdeal', 'https://www.snapdeal.com'),
    ('ajio', 'https://www.ajio.com'),
    ('myntra', 'https://www.myntra.com'),
    ('cricbuzz', 'https://www.cricbuzz.com'),
    ('espncricinfo', 'https://www.espncricinfo.com'),
    ('weather', 'https://www.weather.com'),
    ('ndtv', 'https://www.ndtv.com'),
    ('timesofindia', 'https://timesofindia.indiatimes.com'),
    ('hindustantimes', 'https://www.hindustantimes.com'),
    ('indianexpress', 'https://indianexpress.com'),
    ('jiosaavn', 'https://www.jiosaavn.com'),
    ('gaana', 'https://gaana.com'),
    ('spotifyweb', 'https://open.spotify.com'),
    ('soundcloud', 'https://soundcloud.com'),
    ('telegramweb', 'https://web.telegram.org'),
    ('whatsappweb', 'https://web.whatsapp.com'),
    ('duckduckgo', 'https://duckduckgo.com'),
    ('bing', 'https://www.bing.com'),
    ('yahoo', 'https://www.yahoo.com'),
    ('fliphtml5', 'https://fliphtml5.com'),
    ('pinterest', 'https://www.pinterest.com'),
    ('redbus', 'https://www.redbus.in'),
    ('makemytrip', 'https://www.makemytrip.com')
    # Add up to 100 as needed
]

# Insert data
cursor.executemany('INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)', sys_apps)
cursor.executemany('INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)', websites)

# Commit and close
conn.commit()
conn.close()

print("✅ Data inserted successfully.")
