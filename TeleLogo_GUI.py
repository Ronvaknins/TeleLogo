import os
import logging
import time
import ffmpeg
import threading
import asyncio
import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMainWindow, QMessageBox,QPlainTextEdit,QSplashScreen
from PySide6.QtCore import QMetaObject,Qt,QTimer
from PySide6.QtGui import QTextCursor,QPixmap
import signal
from telegram import Update
from telegram.ext import Application as TelegramApplication, MessageHandler, filters, ContextTypes,Updater
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import subprocess

# Example usage


from UI.ui_MainWindow import Ui_MainWindow
from UI.ui_LocalServerWidget import Ui_Dialog  
import subprocess
import UI.EditLogoWidget as EditLogoW
# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


API_ID = ""
API_HASH = ""
LS_PROCESS = None

class LogoBotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.click_count = 0

        # Connect buttons
        self.ui.startBotBtn.clicked.connect(self.start_bot)
        self.ui.stopBotBtn.clicked.connect(self.stop_bot)
        self.ui.stopBotBtn.setEnabled(False)
        self.ui.LSSettingBtn.clicked.connect(self.open_settings)
        self.ui.startLSbtn.clicked.connect(self.toggle_LocalServer)

        self.ui.editLogoBtn.clicked.connect(self.onClickEditLogo)
        self.editLogo = EditLogoW.LogoEditWindow()
       
        # Initialize bot variables
        self.bot_thread = None
        self.telegram_app = None
        self.event_loop = None
        self.localServerEnabled = False
        self.LS_process = None
    
        self.ui.LoggingTextWig.setReadOnly(True)


       
        self.root_logger = logging.getLogger()
       
       
        text_handler = LogHandler(self.ui.LoggingTextWig)
        self.root_logger.addHandler(text_handler)
        self.root_logger.info("Application started.")
        self.load_config()
        self.editLogo.trigger_saveToConfigFile.connect(self.save_config)
        self.editLogo.trigger_LoadConfigFile.connect(self.load_config)
       
    def onClickEditLogo(self):
        self.editLogo.show()

        
    def toggle_LocalServer(self):
        self.click_count += 1
        if self.click_count % 2 == 1:  # Odd clicks
            self.ui.startLSbtn.setText("Stop Local Server..")
            self.ui.startLSbtn.setStyleSheet(""" QPushButton { background-color: rgb(207, 75, 77); color: white; font: 700 Arial; border-radius: 10px; padding: 5px 15px; } """)
            exe_path = r"bot-server/telegram-bot-api/bin/telegram-bot-api.exe"
            arguments = ["--local", f"--api-id={API_ID}", f"--api-hash={API_HASH}","--dir=temp"]
            run_exe_as_thread(exe_path, arguments)
            self.localServerEnabled = True
            self.root_logger.info("Local Server started successfully.")
        else: 
            try:
                self.stop_bot()
                LS_PROCESS.terminate()        
                self.localServerEnabled = False
                self.ui.startLSbtn.setText("Start Local Server")
                self.ui.startLSbtn.setStyleSheet(""" QPushButton { background-color: rgb(12,129,213); color: white; font: 700 Arial; border-radius: 10px; padding: 5px 15px; } """)    
                self.root_logger.info("Local Server Process terminated successfully.")
            except Exception as e:
                self.root_logger.error(f"Error while killing the process: {e}")
        
    def open_settings(self):
        dialog = SettingsDialog(self)  # Open the settings dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print(f"Bot Token: {dialog.ui.API_ID_Edit.text()}")  # For example, use the entered token

    def append_log(self, message):
        """Append a log message to the QTextEdit widget."""
        self.ui.LoggingTextWig.appendPlainText(message)
        cursor = self.ui.LoggingTextWig.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.LoggingTextWig.setTextCursor(cursor)

    def start_bot(self):
        """Start the Telegram bot."""
        token = self.ui.TokenlineEdit.text().strip()
        if not token:
            self.root_logger.info("Error: Bot token is required.")
            return

        self.ui.startBotBtn.setEnabled(False)
        self.ui.stopBotBtn.setEnabled(True)
        #self.run_bot(token)
        #asyncio.run(self.run_bot(token))
        self.bot_thread = threading.Thread(target=self.run_bot, args=(token,), daemon=True)
        self.bot_thread.start()

    def stop_bot(self):
        """Stop the Telegram bot."""  
        #self.telegram_app.stop()   
        if self.telegram_app and self.event_loop: 

            self.event_loop.call_soon_threadsafe(self.event_loop.stop)
            #self.event_loop.stop()
            self.bot_thread.join()
        #     self.append_log("Bot stopped.")
            self.telegram_app = None
            self.event_loop = None
            self.bot_thread = None
        self.ui.startBotBtn.setEnabled(True)
        self.ui.stopBotBtn.setEnabled(False)

    def run_bot(self, token):
        """Run the Telegram bot."""
        try:
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)   
            if self.localServerEnabled:      
                    builder = TelegramApplication.builder()
                    builder.token(token)
                    builder.base_url(r'http://localhost:8081/bot')
                    builder.base_file_url(r'http://localhost:8081/file/bot')
                    builder.local_mode(local_mode = True)
                    self.telegram_app = builder.build()       

                    # Register handlers
                    self.telegram_app.add_handler(MessageHandler(filters.VIDEO, self.video_handler))  # Use filters.VIDEO

                    # Register error handler
                    self.telegram_app.add_error_handler(self.error_handler)

                    # Start the bot
                    self.event_loop.run_until_complete(self.telegram_app.run_polling())
        
                    
            else:
               
                self.telegram_app = TelegramApplication.builder().token(token).concurrent_updates(True).build()
                self.telegram_app.add_handler(MessageHandler(filters.VIDEO, self.video_handler))
                self.telegram_app.add_error_handler(self.error_handler)
                self.event_loop.run_until_complete(self.telegram_app.run_polling())
        except RuntimeError as e:
            self.root_logger.info(f"Event Loop Closed {e}")
    
        
            
        # Error handler
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.warning(f"Update {update} caused error {context.error}")

    def closeEvent(self, event):
        #Override closeEvent to save config on exit.
        self.save_config()
        event.accept()
    def save_config(self):
        """Save config to a file."""
        try:
            with open("config", "w") as file:
                global API_ID,API_HASH
                config = {
                    "TOKEN": self.ui.TokenlineEdit.text().strip(),
                    "API_ID": API_ID,
                    "HASH_ID": API_HASH,
                    "LOGO_PATH": self.editLogo.getLogoPath(),       
                    "LogoPosX": self.editLogo.getX(),
                    "LogoPosY": self.editLogo.getY(),
                    "LogoScaleFactor": self.editLogo.getScaleFactor(),
                    "SafeMargin": self.editLogo.logo_frame.safeMarginEnabled.isChecked()
                }
                
                json.dump(config, file, indent=4)
            self.root_logger.info("Config saved successfully.")
        except Exception as e:
            self.root_logger.info(f"Failed to save config: {e}")
    def load_config(self):
        """Load config from a file."""
        try:
            with open("config", "r") as file:
                global API_HASH,API_ID
                config = json.load(file)
                self.ui.TokenlineEdit.setText(config["TOKEN"]),
                API_ID = config["API_ID"] 
                API_HASH = config["HASH_ID"]
                self.editLogo.setLogoPath(config["LOGO_PATH"])   
                # if(config["LOGO_PATH"]):
                #    self.editLogo.logo_frame.load_image(config["LOGO_PATH"])
                self.editLogo.setX(config["LogoPosX"])
                self.editLogo.setY(config["LogoPosY"])          
                self.editLogo.setScaleFactor(config["LogoScaleFactor"]) 
                self.editLogo.setSafeMarginState(Qt.CheckState.Checked if bool(config["SafeMargin"]) else Qt.CheckState.Unchecked)
                self.root_logger.info("Config File Loaded")
        except (FileNotFoundError, json.JSONDecodeError):
            self.root_logger.info("No valid config file found. Using default config.")

    async def video_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        folders = ["Downloads", "Converted"]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)  # Create folder if it doesn't exist
                self.root_logger.info(f"Created folder: {folder}")
            else:
                self.root_logger.info(f"Folder already exists: {folder}")
        """Handle incoming video messages."""
        video_file = await update.message.video.get_file()
        file_name = f"Downloads/{video_file.file_id}.mp4"

        await video_file.download_to_drive(file_name)
        output_name = f"Converted/{video_file.file_unique_id}_withLogo.mp4"

        self.root_logger.info(f"Processing video: {file_name}")
        output_video = self.burn_logo(file_name, output_name)

        if output_video:
            await update.message.reply_video(video=open(output_video, 'rb'))
            self.root_logger.info(f"Processed video sent: {output_video}")
        else:
            await update.message.reply_text("Error processing the video.")
            self.root_logger.info("Error processing the video.")

    def burn_logo(self, input_video: str, output_name: str) -> str:
        """Overlay a logo on the video."""
        try:
            w, h = self.get_video_resolution(input_video)
            in_file = ffmpeg.input(input_video)
            
            scaleFactor = self.editLogo.getScaleFactor()*2
            overlay_file = ffmpeg.input(self.editLogo.getLogoPath()).filter("scale", f"iw*{scaleFactor}", f"ih*{scaleFactor}")
            audio = in_file.audio

            if w / h < 1:  # Vertical video
                blurred_video = in_file.filter("scale", "1920x1080").filter("boxblur", 20)
                vertical_video = in_file.filter("scale", "1080", "1080")
                final_video = ffmpeg.filter([blurred_video, vertical_video], "overlay", x=420, y=0).overlay(
                    overlay_file, x=self.editLogo.getX(), y=self.editLogo.getY(),
                )
            else:  # Horizontal video
                final_video = in_file.filter("scale", "1920x1080").overlay(overlay_file, x=self.editLogo.getX(), y=self.editLogo.getY())

            command = (final_video.output(audio, output_name).compile())
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
            out, err = process.communicate()
            #Log the FFmpeg output
            if out:
                self.root_logger.info(out.decode('utf-8'))
            if err:
                self.root_logger.error(err.decode('utf-8'))
                
            return output_name
        
        except Exception as e:
            self.root_logger.error(f"Error processing video: {e}")
            return None

    def get_video_resolution(self, file_path: str) -> tuple:
        """Get the resolution of a video."""
        parser = createParser(file_path)
        if not parser:
            raise ValueError(f"Could not open file {file_path}")

        metadata = extractMetadata(parser)
        if not metadata:
            raise ValueError(f"Could not extract metadata from {file_path}")

        width = metadata.get("width")
        height = metadata.get("height")
        return width, height

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        global API_ID,API_HASH
        if API_ID:
            self.ui.API_ID_Edit.setText(API_ID)
        if API_HASH:
            self.ui.HASH_Edit.setText(API_HASH)
        # You can access widgets from the .ui file directly by their names
        # Example: self.token_input is automatically created by loading the UI
        
        # Setup actions for the buttons
        self.ui.buttonBox.accepted.connect(self.onClickOk)
        self.ui.buttonBox.rejected.connect(self.reject)
   

    def onClickOk(self):
        global API_ID,API_HASH
        API_ID = self.ui.API_ID_Edit.text()
        API_HASH = self.ui.HASH_Edit.text()
        #print(API_HASH,API_ID)


def run_exe_as_thread(exe_path, args=None):
    def run():
        try:
            # Build the command with arguments
            command = [exe_path]
            if args:
                command.extend(args)
            # Start the subprocess and get the process object
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)     
            global LS_PROCESS
            LS_PROCESS = process
            # Save the process to be able to terminate it later
            #return process
        except Exception as e:
            print(f"Error: {e}")
    # Create and start a thread
    thread = threading.Thread(target=run)
    thread.start()
    #return thread # Return the process object to interact with it


class LogHandler(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)


    def emit(self, record):
        try:
            msg = self.format(record)
            self.text_edit.appendPlainText(msg)
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.update()
        except Exception as e:
            print(f"Error in LogHandler.emit: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create the splash screen with a logo image
    pixmap = QPixmap("./UI/resources/TeleLogo.png")  # Replace with the path to your logo
    pixmap = pixmap.scaled(600, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.setStyleSheet("background-color: rgb(31,31,31);")
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()
       # Show splash for 3 seconds (adjust as needed)
    QTimer.singleShot(2000, splash.close)  # Close splash after 3000 ms (3 seconds)
    main_window = LogoBotApp()
    time.sleep(2)
    main_window.show()
    sys.exit(app.exec())
