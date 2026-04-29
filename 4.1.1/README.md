# Websocket Paint


Installation:


Go to releases and download the latest release .zip


Development:
```
git clone https://github.com/InconceivableTortoise42/CSE-Unit-3.git
cd SCE-Unit-3/4.1.1/
uv symc
```

Build: (must have cloudflared executable)
```
pyinstaller --noconfirm --onedir --windowed --contents-directory "." --add-data "assets;assets" --add-data "cloudflared.exe;." client.py
```