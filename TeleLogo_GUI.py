import os
import logging
import shutil
import time
import ffmpeg
import threading
import asyncio
import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMainWindow, QMessageBox,QPlainTextEdit,QSplashScreen
from PySide6.QtCore import QMetaObject,Qt,QTimer,Signal,QThread
from PySide6.QtGui import QTextCursor,QPixmap
from pathlib import Path
import httpcore
import psutil
from telegram import Update
import httpx
import telegram
#from telegram.ext import Application as TelegramApplication, MessageHandler, filters, ContextTypes,Updater
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,filters
import subprocess
import traceback
from UI.ui_MainWindow import Ui_MainWindow
from UI.ui_LocalServerWidget import Ui_Dialog  
import subprocess
import UI.EditLogoWidget as EditLogoW



DEBUG=False
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
        self.editLogo = EditLogoW.LogoEditWindow(resource_path())
       
        # Initialize bot variables
        self.bot_thread = None
        self.localServer_thread = None
        self.telegram_app = None
        self.localServerEnabled = False
        self.ui.LoggingTextWig.setReadOnly(True)


        self.root_logger = logging.getLogger()
           
        text_handler = LogHandler(self.ui.LoggingTextWig)
        self.root_logger.addHandler(text_handler)
        self.root_logger.info("Application started.")
        
        self.load_config()
        self.editLogo.trigger_saveToConfigFile.connect(self.save_config)
        self.editLogo.trigger_LoadConfigFile.connect(self.load_config)
        folders = ["Downloads", "Converted"]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)  # Create folder if it doesn't exist
                self.root_logger.info(f"Created folder: {folder}")
            else:
                self.root_logger.info(f"Folder already exists: {folder}")
        self.clean_dir("LSDIR")
        
    def clean_dir(self,path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                self.root_logger.info(f"Folder '{path}' removed successfully.")
            else:
                self.root_logger.info(f"Folder '{path}' does not exist.")
        except OSError as e:
            self.root_logger.error(f"Error removing folder '{path}': {e}")

    def onClickEditLogo(self):
        self.editLogo.show()

        
    def toggle_LocalServer(self):
        self.click_count += 1
        if self.click_count % 2 == 1:
            self.ui.startLSbtn.setText("Stop Local Server..")
            self.ui.startLSbtn.setStyleSheet(""" QPushButton { background-color: rgb(207, 75, 77); color: white; font: 700 Arial; border-radius: 10px; padding: 5px 15px; } """)
            exe_path = "./bot-server/telegram-bot-api/bin/telegram-bot-api.exe"
            global DEBUG
            arguments = ["--verbosity=4" if DEBUG else "--local","--local", f"--api-id={API_ID}", f"--api-hash={API_HASH}","--temp-dir=LS_temp","--dir=LSDIR"]

            self.run_exe_as_thread(exe_path, arguments)
            self.localServerEnabled = True
            self.root_logger.info("Local Server started successfully.")
        else: 
            try:
                if self.bot_thread:
                    self.stop_bot()
                LS_PROCESS.terminate()        
                self.localServerEnabled = False
                self.localServer_thread.join()
                self.ui.startLSbtn.setText("Start Local Server")
                self.ui.startLSbtn.setStyleSheet(""" QPushButton { background-color: rgb(12,129,213); color: white; font: 700 Arial; border-radius: 10px; padding: 5px 15px; } """)    
                self.root_logger.info("Local Server Process terminated successfully.")
            except Exception as e:
                self.root_logger.error(f"Error while killing the process: {e}")
        
    def open_settings(self):
        dialog = SettingsDialog(self)  # Open the settings dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.root_logger.info(f"Bot Token: {dialog.ui.API_ID_Edit.text()}")  # For example, use the entered token

    def start_bot(self):
        """Start the Telegram bot."""
        token = self.ui.TokenlineEdit.text().strip()
        if not token:
            self.root_logger.info("Error: Bot token is required.")
            return

        self.bot_thread = TelegramBotThread(token,self.localServerEnabled,self.root_logger,self.editLogo) 
        self.bot_thread.start()
        self.bot_thread.stop_signal.connect(self.on_bot_stopped) 

        self.ui.startBotBtn.setEnabled(False)
        self.ui.stopBotBtn.setEnabled(True)


    def stop_bot(self):
        """
        Stop the Telegram bot.
        """  
        if self.bot_thread:
            self.bot_thread.stop()
            while (self.bot_thread.telegram_app._running):
                continue
            self.bot_thread = None
            self.ui.startBotBtn.setEnabled(True)
            self.ui.stopBotBtn.setEnabled(False)           


    def on_bot_stopped(self):
        # You can add actions to perform when the bot is stopped here
        print("Bot stopped.")
    def closeEvent(self, event):
        #Override closeEvent
        if self.localServerEnabled:
            try:
                if self.bot_thread:
                    self.stop_bot()
                LS_PROCESS.terminate()  
                self.localServer_thread.join()      
                self.localServerEnabled = False
                self.ui.startLSbtn.setText("Start Local Server")
                self.ui.startLSbtn.setStyleSheet(""" QPushButton { background-color: rgb(12,129,213); color: white; font: 700 Arial; border-radius: 10px; padding: 5px 15px; } """)    
                self.root_logger.info("Local Server Process terminated successfully.")
            except Exception as e:
                self.root_logger.error(f"Error while killing the process: {e}")
        else:
            if self.bot_thread:
                self.stop_bot()
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
                self.ui.TokenlineEdit.setText(config["TOKEN"])
                API_ID = config["API_ID"] 
                API_HASH = config["HASH_ID"]
                self.editLogo.setLogoPath(config["LOGO_PATH"])   
                self.editLogo.setX(config["LogoPosX"])
                self.editLogo.setY(config["LogoPosY"])          
                self.editLogo.setScaleFactor(config["LogoScaleFactor"]) 
                self.editLogo.setSafeMarginState(Qt.CheckState.Checked if bool(config["SafeMargin"]) else Qt.CheckState.Unchecked)
                self.root_logger.info("Config File Loaded")
        except (FileNotFoundError, json.JSONDecodeError):
            self.root_logger.info("No valid config file found. Using default config.")

    def run_exe_as_thread(self,exe_path, args=None):
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
                #atexit.register(LS_PROCESS.terminate)
                out, err = process.communicate()

                
                #Log the FFmpeg output
                if out:
                    self.root_logger.info(out.decode('utf-8'))
                if err:
                    self.root_logger.error(err.decode('utf-8'))
                # Save the process to be able to terminate it later
                #return process
            except Exception as e:
                self.root_logger.info(f"Error: {e}")
        # Create and start a thread
        self.localServer_thread = threading.Thread(target=run)
        self.localServer_thread.start()
        
        
        #return thread # Return the process object to interact with it
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

class TelegramBotThread(QThread):
    #message_received = Signal(str)
    stop_signal = Signal()
    def __init__(self, token,localServerEnabled,root_logger,editLogo):
        super().__init__()
        self.token = token
        self.editLogo = editLogo
        self.root_logger = root_logger
        self.telegram_app = None
        self.localServerEnabled = localServerEnabled
        self.loop = asyncio.new_event_loop() 
       
    def run(self):
        asyncio.set_event_loop(self.loop)
        if DEBUG:
            self.loop.set_debug(True)
        try:
            if self.localServerEnabled:
                self.application = ApplicationBuilder()
                self.application.token(self.token)
                self.application.base_url(r'http://localhost:8081/bot')
                self.application.base_file_url(r'http://localhost:8081/file/bot')
                self.application.local_mode(local_mode = True)
                self.telegram_app = self.application.build() 
                self.telegram_app.add_handler(MessageHandler(filters.VIDEO, self.video_handler))
                #self.telegram_app.add_error_handler(self.error_handler)
                self.telegram_app.run_polling(close_loop=False,timeout=20)
            else:
                self.telegram_app = ApplicationBuilder().token(self.token).concurrent_updates(True).build()
                self.telegram_app.add_handler(MessageHandler(filters.VIDEO, self.video_handler))
                #self.telegram_app.add_error_handler(self.error_handler)   
                self.telegram_app.run_polling(close_loop=False,timeout=20)
                
        except asyncio.CancelledError as e:
            self.root_logger.info(e) 
        except RuntimeError as e:
            self.root_logger.info(e) 
        except httpcore.ConnectError as e:
            self.root_logger.info(f"Connection error occurred: {e}")
        except httpx.ConnectError as e:
           self.root_logger.info(f"Connection error: {e}")
        except Exception as e:
            self.root_logger.info(e) 
                        # Error handler
    async def error_handler(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.root_logger.error(f"Update {update} caused error")


    def stop(self):
        try:
        
            #self.loop.call_soon_threadsafe(self.telegram_app.stop)
            self.loop.call_soon_threadsafe(self.loop.stop)
            #await asyncio.sleep(10)
        except asyncio.CancelledError as e:
            self.root_logger.info(e) 
        except telegram.error.NetworkError as e:
            self.root_logger.info(f"Connection error occurred: {e}")
        except httpcore.ConnectError as e:
            self.root_logger.info(f"Connection error occurred: {e}")
        except httpx.ConnectError as e:
           self.root_logger.info(f"Connection error: {e}")
        except RuntimeError as e:
            self.root_logger.info(e) 
        
    async def video_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming video messages."""
    
        video_file = await update.message.video.get_file()
        file_name = f"Downloads/{video_file.file_unique_id}.mp4"
 
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

            w, h = None,None
            in_file = ffmpeg.input(input_video)
            probe = ffmpeg.probe(input_video)
            streams = probe.get('streams', [])
            #print(any(stream.get('codec_type') == 'audio' for stream in streams))
            hasAudio = False
            for stream in streams:
                if stream.get('width'):
                    w = int(stream.get('width'))
                if stream.get('height'):
                    h = int(stream.get('height'))
                if stream.get('codec_type') == 'audio':
                    hasAudio = True 
            scaleFactor = self.editLogo.getScaleFactor()*2
            overlay_file = ffmpeg.input(self.editLogo.getLogoPath()).filter("scale", f"iw*{scaleFactor}", f"ih*{scaleFactor}")
            

            if w / h < 1:  # Vertical video
                blurred_video = in_file.filter("scale", "1920x1080").filter("boxblur", 20)
                vertical_video = in_file.filter("scale", "1080", "1080")
                final_video = ffmpeg.filter([blurred_video, vertical_video], "overlay", x=420, y=0).overlay(
                    overlay_file, x=self.editLogo.getX(), y=self.editLogo.getY(),
                )
            else:  # Horizontal video
                final_video = in_file.filter("scale", "1920x1080").overlay(overlay_file, x=self.editLogo.getX(), y=self.editLogo.getY())


            if hasAudio:
                command = (final_video.output(in_file.audio, output_name).compile(overwrite_output=True))
            else:
                command = (final_video.output(output_name).compile(overwrite_output=True))
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
def resource_path():
    """ Get the absolute path to a resource, works for dev and PyInstaller """
    try:
        # PyInstaller's _MEIPASS provides the base path for bundled files
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # For development, use the current directory
        base_path = Path(".")

    # Use the / operator to concatenate paths
    return base_path

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
            #self.text_edit.update()
        except Exception as e:
            print(f"Error in LogHandler.emit: {e}")

def loggerConfig():
    #global DEBUG

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG if DEBUG else logging.INFO)
    
    #logger = logging.getLogger(__name__)
def terminate_process_by_name(name):
    """
    Check if a process with the given name is running and terminate it.
    """
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # Match process name
            if process.info['name'] == name:
                print(f"Terminating process: {name} (PID: {process.info['pid']})")
                psutil.Process(process.info['pid']).terminate()
                print(f"Process {name} terminated successfully.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Ignore errors for processes that no longer exist or cannot be accessed
    
    print(f"No process named {name} found.")

# Usage



if __name__ == "__main__":
    
    try:
        
     
        terminate_process_by_name("telegram-bot-api.exe")
        #print(len(sys.argv))
        if len(sys.argv) > 1:
            if '--debug' in sys.argv:
                DEBUG = True
                #print("DEBUG ENABLED")
                loggerConfig()
            else:
                loggerConfig()
        else:
            loggerConfig()
                

        app = QApplication(sys.argv)
        #Create the splash screen with a logo image
        pixmap = QPixmap(str(resource_path() / "UI/resources/TeleLogo600.png"))  # Replace with the path to your logo
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        splash.setWindowFlag(Qt.FramelessWindowHint)
        splash.show()
        # Show splash for 2 seconds (adjust as needed)
        QTimer.singleShot(2000, splash.close)  # Close splash after 2000 ms (2 seconds)
        main_window = LogoBotApp()
        time.sleep(2)
        main_window.show()
    
        app.exec()

    except Exception as e:
        
        logging.error("An error occurred:", exc_info=True)
        traceback.print_exc()
        sys.exit(1)
    

