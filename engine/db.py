import csv
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# cursor.execute('''CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))''')
# # query = "CREATE TABLE IF NOT  EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# # cursor.execute(query)
# # # List of local Windows applications

# apps = [
#     # 🔵 Social Media & Communication
#     ('Instagram', r'C:\Users\Piyush sharma\AppData\Local\Instagram\Instagram.exe'),
#     ('Twitter', r'C:\Users\Piyush sharma\AppData\Local\Twitter\Twitter.exe'),
#     ('WhatsApp Desktop', r'C:\Users\Piyush sharma\AppData\Local\WhatsApp\WhatsApp.exe'),
#     ('Telegram', r'C:\Users\Piyush sharma\AppData\Roaming\Telegram Desktop\Telegram.exe'),
#     ('Discord', r'C:\Users\Piyush sharma\AppData\Local\Discord\Update.exe'),
#     ('Facebook Messenger', r'C:\Users\Piyush sharma\AppData\Local\Facebook\Messenger.exe'),

#     # 🎵 Media & Streaming
#     ('Spotify', r'C:\Users\Piyush sharma\AppData\Roaming\Spotify\Spotify.exe'),
#     ('Netflix App', r'C:\Users\Piyush sharma\AppData\Local\Netflix\Netflix.exe'),
#     ('VLC Media Player', r'C:\Program Files\VideoLAN\VLC\vlc.exe'),
#     ('Windows Media Player', r'C:\Program Files\Windows Media Player\wmplayer.exe'),

#     # 🌐 Web Browsers
#     ('Google Chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
#     ('Microsoft Edge', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'),
#     ('Mozilla Firefox', r'C:\Program Files\Mozilla Firefox\firefox.exe'),
#     ('Brave Browser', r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'),

#     # 💻 Development Tools
#     ('Visual Studio Code', r'C:\Users\Piyush sharma\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
#     ('Android Studio', r'C:\Program Files\Android\Android Studio\bin\studio64.exe'),
#     ('Git Bash', r'C:\Program Files\Git\git-bash.exe'),
#     ('XAMPP', r'C:\xampp\xampp-control.exe'),
#     ('Sublime Text', r'C:\Program Files\Sublime Text\sublime_text.exe'),
#     ('Notepad++', r'C:\Program Files\Notepad++\notepad++.exe'),

#     # 📁 System Utilities
#     ('Task Manager', r'C:\Windows\System32\Taskmgr.exe'),
#     ('Command Prompt', r'C:\Windows\System32\cmd.exe'),
#     ('Control Panel', r'C:\Windows\System32\control.exe'),
#     ('Settings', r'C:\Windows\ImmersiveControlPanel\SystemSettings.exe'),
#     ('Snipping Tool', r'C:\Windows\System32\SnippingTool.exe'),
#     ('Registry Editor', r'C:\Windows\regedit.exe'),
#     ('Calculator', r'C:\Windows\System32\calc.exe'),

#     # 🛠️ Productivity / Design
#     ('OBS Studio', r'C:\Program Files\obs-studio\bin\64bit\obs64.exe'),
#     ('Figma', r'C:\Users\Piyush sharma\AppData\Local\Figma\Figma.exe'),
#     ('Zoom', r'C:\Users\Piyush sharma\AppData\Roaming\Zoom\bin\Zoom.exe'),
#     ('Notion', r'C:\Users\Piyush sharma\AppData\Local\Programs\Notion\Notion.exe'),
#     ('Adobe Photoshop', r'C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe'),
#     ('Adobe Illustrator', r'C:\Program Files\Adobe\Adobe Illustrator 2023\Support Files\Contents\Windows\Illustrator.exe'),
#     ('MS Word', r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'),
#     ('MS Excel', r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'),
#     ('MS PowerPoint', r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE')
# ]

# # Insert updated applications, removing duplicates by name
# for name, path in apps:
#     try:
        
#         cursor.execute("INSERT INTO sys_command VALUES (NULL, ?, ?)", (name, path))
#     except Exception as e:
#         print(f"Failed to insert {name}: {e}")

# # Commit and close connection
# con.commit()

# con.close()




# Create the web_command table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS web_command (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         url TEXT
#     )
# ''')

# # List of websites
# websites = [
#     # 🔍 Search Engines
#     ('Google', 'https://www.google.com'),
#     ('Bing', 'https://www.bing.com'),
#     ('DuckDuckGo', 'https://duckduckgo.com'),

#     # 📧 Email
#     ('Gmail', 'https://mail.google.com'),
#     ('Outlook', 'https://outlook.live.com'),
#     ('Yahoo Mail', 'https://mail.yahoo.com'),

#     # 💬 Communication
#     ('WhatsApp Web', 'https://web.whatsapp.com'),
#     ('Telegram Web', 'https://web.telegram.org'),
#     ('Messenger', 'https://www.messenger.com'),

#     # 🧠 AI & Productivity
#     ('ChatGPT', 'https://chat.openai.com'),
#     ('Bard AI (Gemini)', 'https://gemini.google.com'),
#     ('Notion', 'https://www.notion.so'),
#     ('Trello', 'https://trello.com'),
#     ('Google Docs', 'https://docs.google.com'),
#     ('Google Sheets', 'https://sheets.google.com'),

#     # 📚 Learning & Development
#     ('Stack Overflow', 'https://stackoverflow.com'),
#     ('GeeksforGeeks', 'https://www.geeksforgeeks.org'),
#     ('W3Schools', 'https://www.w3schools.com'),
#     ('MDN Web Docs', 'https://developer.mozilla.org'),
#     ('Khan Academy', 'https://www.khanacademy.org'),
#     ('Coursera', 'https://www.coursera.org'),
#     ('Udemy', 'https://www.udemy.com'),

#     # 💻 Code Hosting
#     ('GitHub', 'https://github.com'),
#     ('GitLab', 'https://gitlab.com'),
#     ('Replit', 'https://replit.com'),

#     # 🎨 Design & Inspiration
#     ('Figma', 'https://www.figma.com'),
#     ('Dribbble', 'https://dribbble.com'),
#     ('Behance', 'https://www.behance.net'),
#     ('Canva', 'https://www.canva.com'),

#     # 📺 Entertainment & Streaming
#     ('YouTube', 'https://www.youtube.com'),
#     ('Netflix', 'https://www.netflix.com'),
#     ('Prime Video', 'https://www.primevideo.com'),
#     ('Hotstar', 'https://www.hotstar.com'),
#     ('Spotify', 'https://open.spotify.com'),
#     ('SoundCloud', 'https://www.soundcloud.com'),
#     ('Twitch', 'https://www.twitch.tv'),
#     ('Crunchyroll', 'https://www.crunchyroll.com'),
#     ('Hulu', 'https://www.hulu.com'),
#     ('Disney+', 'https://www.disneyplus.com'),
#     ('Apple Music', 'https://music.apple.com'),
#     ('Deezer', 'https://www.deezer.com'),
#     ('Gaana', 'https://www.gaana.com'),
#     ('JioSaavn', 'https://www.jiosaavn.com'),

#     # 🛒 Shopping
#     ('Amazon', 'https://www.amazon.in'),
#     ('Flipkart', 'https://www.flipkart.com'),
#     ('Myntra', 'https://www.myntra.com'),
#     ('eBay', 'https://www.ebay.com'),
#     ('Alibaba', 'https://www.alibaba.com'),
#     ('Snapdeal', 'https://www.snapdeal.com'),
#     ('Ajio', 'https://www.ajio.com'),
#     ('Jabong', 'https://www.jabong.com'),
#     ('Paytm', 'https://www.paytm.com'),
#     ('BookMyShow', 'https://www.bookmyshow.com'),
#     ('OLX', 'https://www.olx.in'),

#     # 📈 Finance
#     ('Google Finance', 'https://www.google.com/finance'),
#     ('TradingView', 'https://www.tradingview.com'),

#     # 📱 Social Media
#     ('Instagram', 'https://www.instagram.com'),
#     ('Facebook', 'https://www.facebook.com'),
#     ('Twitter (X)', 'https://twitter.com'),
#     ('LinkedIn', 'https://www.linkedin.com'),
#     ('physicswhala', 'https://www.physicswallah.com'),
#     ('Unacademy', 'https://www.unacademy.com'),
#     ('Koo', 'https://www.kooapp.com'),
#     ('Snapchat', 'https://www.snapchat.com'),
#     ('Pinterest', 'https://www.pinterest.com'),
#     ('Reddit', 'https://www.reddit.com'),


#     # 📰 News & Info
#     ('BBC', 'https://www.bbc.com'),
#     ('NDTV', 'https://www.ndtv.com'),
#     ('Google News', 'https://news.google.com'),
#     ('Hacker News', 'https://news.ycombinator.com'),
#     ('Reddit', 'https://www.reddit.com'),
#     ('Quora', 'https://www.quora.com'),
#     ('Wikipedia', 'https://www.wikipedia.org'),
#     ('IMDB', 'https://www.imdb.com'),
#     ('Worldometer', 'https://www.worldometers.info'),
#     ('World Bank', 'https://www.worldbank.org'),
#     ('UN', 'https://www.un.org')
# ]

# # Insert into the web_command table
# for name, url in websites:
#     try:
#         cursor.execute("INSERT INTO web_command VALUES (NULL, ?, ?)", (name, url))
#     except Exception as e:
#         print(f"Failed to insert {name}: {e}")

# # Commit changes to the database
# con.commit()

# testing module 
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# # Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = 'me' 
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])