import sqlite3
import os

# Create/Open database
conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

# Create sys_command table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sys_command (
    name TEXT UNIQUE,
    path TEXT
)
''')

# Create web_command table
cursor.execute('''
CREATE TABLE IF NOT EXISTS web_command (
    name TEXT UNIQUE,
    url TEXT
)
''')

apps = {
    "whatsapp": "start whatsapp:",
    "spotify": "start spotify:",
    "camera": "start microsoft.windows.camera:",
    "calculator": "start calculator:",
    "calendar": "start outlookcal:",
    "mail": "start outlookmail:",
    "maps": "start bingmaps:",
    "photos": "start ms-photos:",
    "weather": "start bingweather:",
    "store": "start ms-windows-store:",
    "paint": "mspaint",
    "notepad": "notepad",
    "cmd": "cmd",
    "powershell": "powershell",
    "file explorer": "explorer",
    "task manager": "taskmgr",
    "control panel": "control",
    "vs code": r"C:\Users\Piyush sharma\AppData\Local\Programs\Microsoft VS Code\Code.exe",  # change path if needed
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # or path to your browser
    "edge": "start msedge",
    "youtube": "start msedge https://www.youtube.com",
    "google": "start msedge https://www.google.com",
    "github": "start msedge https://github.com",
    "stackoverflow": "start msedge https://stackoverflow.com",
    "gmail": "start msedge https://mail.google.com",
    "instagram": "start msedge https://www.instagram.com",
    "twitter": "start msedge https://twitter.com",
    "facebook": "start msedge https://www.facebook.com",
    "linkedin": "start msedge https://www.linkedin.com",
    "netflix": "start msedge https://www.netflix.com",
    "amazon": "start msedge https://www.amazon.in",
    "flipkart": "start msedge https://www.flipkart.com",
    "paytm": "start msedge https://www.paytm.com",
    "excel": "start excel:",
    "word": "start winword:",
    "powerpoint": "start powerpnt:",
    "onedrive": "start onedrive:",
    "zoom": "start zoom:",  # Ensure Zoom is installed
    "teams": "start teams:",  # Ensure Microsoft Teams is installed
    "slack": "start slack:",  # Ensure Slack is installed
    "discord": "start discord:",  # Ensure Discord is installed
    "notion": "start notion:",  # Ensure Notion is installed
    "notepad": "notepad",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",  # Ensure VLC is installed
    "audacity": r"C:\Program Files\Audacity\audacity.exe",  # Ensure Audacity is installed
    "blender": r"C:\Program Files\Blender Foundation\Blender\blender.exe",  # Ensure Blender is installed
    "clipchamp": r"C:\Program Files\Microsoft Clipchamp\Clipchamp.exe",  # Ensure Clipchamp is installed
    "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",  # Ensure OBS Studio is installed
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",  # Ensure Steam is installed
    "xbox": r"C:\Program Files\WindowsApps\Microsoft.XboxApp_48.69.20001.0_x64__8wekyb3d8bbwe\Xbox.exe",  # Ensure Xbox app is installed
    "solitaire": r"C:\Program Files\Microsoft Solitaire Collection\Solitaire.exe",  # Ensure Microsoft Solitaire is installed
    "clock": "start ms-clock:",  # Windows Clock app
    "alarm": "start ms-clock:",  # Windows Alarm app
    "news": "start ms-news:",  # Windows News app
    "weather": "start ms-weather:",  # Windows Weather app

    "photos": "start ms-photos:",  # Windows Photos app
    "calculator": "start calculator:",  # Windows Calculator app
    "snipping tool": "start snippingtool:",  # Windows Snipping Tool
    "voice recorder": "start voice recorder:",  # Windows Voice Recorder app
    "microsoft edge": "start msedge:",  # Microsoft Edge browser
    "microsoft store": "start ms-windows-store:",  # Microsoft Store app
    "microsoft teams": "start teams:",  # Microsoft Teams app
    "microsoft word": "start winword:",  # Microsoft Word app
    "microsoft excel": "start excel:",  # Microsoft Excel app
    "microsoft powerpoint": "start powerpnt:",  # Microsoft PowerPoint app
    "microsoft onenote": "start onenote:",  # Microsoft OneNote
    "microsoft outlook": "start outlook:",  # Microsoft Outlook app
    "microsoft publisher": "start mspub:",  # Microsoft Publisher app


}
for name, path in apps.items():
    try:
        cursor.execute("INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)", (name, path))
    except Exception as e:
        print(f"Error inserting website {name}: {e}")

# Top websites
# websites = {
#     "google": "https://www.google.com",
#     "youtube": "https://www.youtube.com",
#     "github": "https://github.com",
#     "stackoverflow": "https://stackoverflow.com",
#     "gmail": "https://mail.google.com",
#     "instagram": "https://www.instagram.com",
#     "twitter": "https://twitter.com",
#     "facebook": "https://www.facebook.com",
#     "linkedin": "https://www.linkedin.com",
#     "netflix": "https://www.netflix.com",
#     "amazon": "https://www.amazon.in",
#     "flipkart": "https://www.flipkart.com",
#     "paytm": "https://www.paytm.com",
#     "phonepe": "https://www.phonepe.com",
#     "canva": "https://www.canva.com",
#     "zomato": "https://www.zomato.com",
#     "swiggy": "https://www.swiggy.com",
#     "bookmyshow": "https://in.bookmyshow.com",
#     "snapchat": "https://web.snapchat.com",
#     "uber": "https://www.uber.com/in/en/",
#     "ola": "https://www.olacabs.com",
#     "irctc": "https://www.irctc.co.in",
#     "makemytrip": "https://www.makemytrip.com",
#     "chatgpt": "https://chat.openai.com",
#     "bing": "https://www.bing.com",
#     "duckduckgo": "https://www.duckduckgo.com",
#     "reddit": "https://www.reddit.com",
#      "youtube": "https://www.youtube.com",
#     "google": "https://www.google.com",
#     "gmail": "https://mail.google.com",
#     "facebook": "https://www.facebook.com",
#     "instagram": "https://www.instagram.com",
#     "twitter": "https://twitter.com",
#     "linkedin": "https://www.linkedin.com",
#     "whatsapp": "https://web.whatsapp.com",
#     "github": "https://github.com",
#     "stackoverflow": "https://stackoverflow.com",
#     "chatgpt": "https://chat.openai.com",
#     "netflix": "https://www.netflix.com",
#     "amazon": "https://www.amazon.in",
#     "flipkart": "https://www.flipkart.com",
#     "snapdeal": "https://www.snapdeal.com",
#     "zomato": "https://www.zomato.com",
#     "swiggy": "https://www.swiggy.com",
#     "hotstar": "https://www.hotstar.com",
#     "spotify": "https://open.spotify.com",
#     "gaana": "https://gaana.com",
#     "jiosaavn": "https://www.jiosaavn.com",
#     "google maps": "https://maps.google.com",
#     "bing": "https://www.bing.com",
#     "duckduckgo": "https://duckduckgo.com",
#     "udemy": "https://www.udemy.com",
#     "coursera": "https://www.coursera.org",
#     "edx": "https://www.edx.org",
#     "khan academy": "https://www.khanacademy.org",
#     "wikipedia": "https://www.wikipedia.org",
#     "quora": "https://www.quora.com",
#     "reddit": "https://www.reddit.com",
#     "amazon prime": "https://www.primevideo.com",
#     "pinterest": "https://www.pinterest.com",
#     "cricbuzz": "https://www.cricbuzz.com",
#     "espn cricinfo": "https://www.espncricinfo.com",
#     "irctc": "https://www.irctc.co.in",
#     "bookmyshow": "https://in.bookmyshow.com",
#     "makemytrip": "https://www.makemytrip.com",
#     "goibibo": "https://www.goibibo.com",
#     "yatra": "https://www.yatra.com",
#     "redbus": "https://www.redbus.in",
#     "cleartrip": "https://www.cleartrip.com",
#     "airbnb": "https://www.airbnb.co.in",
#     "ola": "https://www.olacabs.com",
#     "uber": "https://www.uber.com",
#     "canva": "https://www.canva.com",
#     "pixabay": "https://pixabay.com",
#     "pexels": "https://www.pexels.com",
#     "unsplash": "https://unsplash.com",
#     "chatpdf": "https://www.chatpdf.com",
#     "dribble": "https://dribbble.com",
#     "behance": "https://www.behance.net",
#     "github pages": "https://pages.github.com",
#     "replit": "https://replit.com",
#     "codesandbox": "https://codesandbox.io",
#     "jsfiddle": "https://jsfiddle.net",
#     "codepen": "https://codepen.io",
#     "notion": "https://www.notion.so",
#     "figma": "https://www.figma.com",
#     "cloudflare": "https://www.cloudflare.com",
#     "firebase": "https://console.firebase.google.com",
#     "vercel": "https://vercel.com",
#     "netlify": "https://www.netlify.com",
#     "vscode online": "https://vscode.dev",
#     "weather": "https://www.weather.com",
#     "news": "https://news.google.com",
#     "tradingview": "https://www.tradingview.com",
#     "coinmarketcap": "https://coinmarketcap.com",
#     "wazirx": "https://wazirx.com",
#     "binance": "https://www.binance.com",
# }

# # Insert websites
# for name, url in websites.items():
#     try:
#         cursor.execute("INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)", (name, url))
#     except Exception as e:
#         print(f"Error inserting website {name}: {e}")

# Save and close
conn.commit()
conn.close()
print("✅ Database setup complete with system apps and websites.")
