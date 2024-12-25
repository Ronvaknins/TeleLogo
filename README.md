



# TeleLogo
<p align="center">
<img src="https://github.com/user-attachments/assets/15492bf5-0b84-4812-a339-90eaf58973cf" alt="TeleLogo Logo" width="500">
  <br>
<img src="https://github.com/user-attachments/assets/c891c7f7-06c1-42d3-8701-c3dd81f6114a" alt="TeleLogo Logo" width="500">
</p>
<div style="text-align: center;">
TeleLogo is a user-friendly desktop application designed to streamline the process of adding logos to video files. It utilizes a Telegram bot to receive video files from users, processes the files to include the specified logo, and then sends the modified video back to the user. The app provides flexibility for operating on Telegram servers or running locally for larger file sizes.
</div>

## Features

- **Logo Customization:** Add,position and scale a logo within a 1920x1080 (Full HD) video frame.
- detects if video ratio is not 16/9 meaning vertically video it will scale the orginal video to 1920x1080 will add blur to it, and will overlay it with the vertical video, and above it the logo layout will be 
- **Flexible File Handling:**
  - Run the bot on Telegram servers (50 MB file size limit).
  - Use a local server with your Telegram app ID and hash ID for larger files.
- **User-Friendly Interface:** Simple and intuitive controls for starting/stopping the bot and editing logo positions.
- **Logging:** Real-time logs to monitor application activity and debug issues.
- users cross-platform support since it's using telegram app (Android,OSX,Web...)

  
## Downloads
  Zip file with executable file ready to run (**ffmpeg with CUDA included**)
  
  | File        | Version   | Platform  | Arch      |
  |-------------|-----------|-----------|-----------|
  | [TeleLogo-V1.0.0-x64.zip](https://github.com/Ronvaknins/TeleLogo/releases/download/v1.0.0/TeleLogo-V1.0.0-x64.zip) | 1.0.0     | Windows   | x64 |
 

## Requirements

- **Operating System:** Windows 10 or later
- **Python:** Version 3.9 or higher
- **Dependencies:**
  - `PySide6=6.8.1`
  - `ffmpeg-python=0.2.0`
  - `python-telegram-bot=21.6`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ronvaknins/TeleLogo.git
   cd TeleLogo
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
  
3. Ensure `ffmpeg` is installed and added to your system PATH.
    - Download `ffmpeg` from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
4. Run TeleLogo_GUI.py
    ```bash
   python TeleLogo_GUI.py
   ```
   

## Getting Started

### Using Telegram Servers

1. Obtain a Telegram bot token from [BotFather](https://t.me/BotFather).
2. Launch the application and paste your bot token into the "Token" field.
3. Add and Position your logo by clicking the "Edit Logo" (preferably a transpernt PNG)
4. Click the **Start** button to activate the bot.
5. Send a video file (up to 50 MB) to your bot via Telegram.
6. The bot will process the video, add the logo, and send it back.

### Running Locally

1. Obtain your `app_id` and `hash_id` from [Telegram's Developer Console](https://my.telegram.org/apps).
2. Configure the application with these credentials.
3. Add and Position your logo by clicking the "Edit Logo" (preferably a transpernt PNG)
4. Click **Start Local Server** to activate the bot locally.
5. Click the **Start** button to activate the bot.
6. Send video files of any size to your bot via Telegram.
7. The bot will process the video, add the logo, and send it back.

### Editing the Logo


<img src="https://github.com/user-attachments/assets/efca2358-d4de-4d01-b3cf-6dc96d1699e8" alt="Logo Editing Window" width="400">


1. Click the **Edit Logo** button.
2. Adjust the position of the logo within the Full HD (1920x1080) frame.
3. you can use **Mouse Wheel** to scale the logo up and down
4. Save your changes

## Logging

The application provides a logging window to display real-time events, such as:
- Bot activity
- App configuration activity
- General app activity
- ffmpeg stdout & stderr
## NOTE: Vertical Videos
  the app detects if video ratio is not 16/9 meaning vertically video it will scale the orginal video to 1920x1080 will add blur to it, and will overlay it with the vertical video, and above it the logo layout will be
![image](https://github.com/user-attachments/assets/21cf9d24-39ef-4596-a84a-2ec710b297ab)


## Troubleshooting

- Ensure your bot token is valid when running on Telegram servers.
- Check your app ID and hash ID when using the local server.
- Verify `ffmpeg` is installed and accessible in your system PATH.
- Refer to the logs for detailed error messages.
## ToDo List
- [ ] Adding support to choose encoding codecs (right now it's using libx264)
- [ ] Add more resolutions (2K,4K etc.)
## Acknowledgments
- [Telegram API](https://core.telegram.org/)
- [Telegram Bot Python Warpper](https://python-telegram-bot.org/)
- [ffmpeg](https://www.ffmpeg.org/)
- [ffmpeg python package](https://github.com/kkroening/ffmpeg-python)
  
**Developed by Ron Vaknin. Feel free to contribute to the project by submitting issues or pull requests on GitHub.**

---

For further questions or support, contact [anylizerexe@gmail.com].

