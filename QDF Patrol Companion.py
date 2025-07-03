#  ██████╗ ██████╗ ███████╗    ██████╗  █████╗ ████████╗██████╗  ██████╗ ██╗          ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗
# ██╔═══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗██║         ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗████╗  ██║██║██╔═══██╗████╗  ██║
# ██║   ██║██║  ██║█████╗      ██████╔╝███████║   ██║   ██████╔╝██║   ██║██║         ██║     ██║   ██║██╔████╔██║██████╔╝███████║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
# ██║▄▄ ██║██║  ██║██╔══╝      ██╔═══╝ ██╔══██║   ██║   ██╔══██╗██║   ██║██║         ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██║╚██╗██║██║██║   ██║██║╚██╗██║
# ╚██████╔╝██████╔╝██║         ██║     ██║  ██║   ██║   ██║  ██║╚██████╔╝███████╗    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║██║ ╚████║██║╚██████╔╝██║ ╚████║
#  ╚══▀▀═╝ ╚═════╝ ╚═╝         ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
# QDF Patrol Companion
# Developed by simplynixyn
version = "0.2 alpha"
# This script is designed to monitor DMR temperature and status from Roblox logs.
# It will notify the user of temperature changes and status updates.
# It also includes a debug mode for additional expremimental features, and additional logging.
# =====================================
# NOITCE!!! This script uses antitamper techniques to prevent unauthorized access and use.
# Thus meaning, if you are not within the QDF Roblox group, you will not be able to run this script.


print("Starting QDF Patrol Companion...")
print("Loading Imports...")
try:
    import os
    import time
    import glob
    import json
    import re
    import tkinter as tk
    from tkinter import Tk, PhotoImage
    from threading import Thread
    from win10toast import ToastNotifier
    import colorsys
    import requests
    import pyaudio
    import os
    import threading
    import time
    from pathlib import Path
    from playsound import playsound
    import pygame
    import ctypes
    import numpy as np
    from pathlib import Path
    import os
    import threading
    import time
    import ctypes
    from pydub import AudioSegment
    from pydub.playback import play
    import random
    import random, time, threading
    import sys
    print("Loaded Imports")
except:
    print("One or more imports failed to load!")

# --- Configuration ---
home_dir = Path.home() # Get the user's home directory
log_dir = home_dir/"AppData"/"Local"/"Roblox"/"logs" # Path to Roblox logs
script_dir = Path(__file__).parent.resolve() # Path to the script directory
# icon_image will be created after Tk root is initialized in DMRTempGUI
keyword = "BloxstrapRPC" # Keyword to look for in logs
temp_pattern = re.compile(r"at (\d{3,})K") # Pattern to extract temperature
status_pattern = re.compile(r"DMR (operational|normal|offline|starting up|in code black|in code omni|in maintenance)", re.IGNORECASE) # Pattern to extract status
rbxuserid = None # DO NOT CHANGE THIS, it is used to store the Roblox user ID after fetching it.
rbxusername = None # DO NOT CHANGE THIS, it is used to store the Roblox username after fetching it.

# Settings
debug_mode = True  # Set to True for debug mode, which enables additional features, such as debug commands.
music = True # Set to True to enable music playback during events.
master = True # prevents automatic updates from github, set to True if you wish to suppress automatic updates.

# Integrity degradation rates (seconds per 1% loss)
DEGRADATION_RATES = {
    (3500, 3749): 11.6,
    (3750, 3999): 5.9,
    (4000, 4249): 5.5,
    (4250, 4499): 2.8,
    (4500, 4749): 2.73,
    (4750, 4999): 1.8,
    (5000, float('inf')): 1.4
}

# Toast notifier
toaster = ToastNotifier()

# Temperature thresholds
thresholds = {
    500: "DMR Temp {temp_int}.",
    2000: "DMR Temp {temp_int}.",
    3000: "DMR Temp, {temp_int}.",
    3400: "DMR Temp, {temp_int}.",
    4555: "DMR Temp, {temp_int}.",
}

print("Loaded Config")

# --- GitHub Version Check ---
def check_github_version():
    try:
        github_raw_url = "https://raw.githubusercontent.com/simplynixyn/QDF-Patrol-Companion/main/QDF%20Patrol%20Companion.py"
        resp = requests.get(github_raw_url, timeout=5)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                if line.strip().startswith("version"):
                    github_version = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if github_version != version:
                        print(f"[UPDATE] Your script version ({version}) is not up to date! Latest: {github_version}")
                    else:
                        print("[INFO] Script is up to date with GitHub.")
                    break
        else:
            print("[WARN] Could not fetch latest version info from GitHub.")
    except Exception as e:
        print(f"[WARN] Version check failed: {e}")

if not master:
    check_github_version()
# --- End GitHub Version Check ---

# --- Utility Functions ---

def debugprint(*args, **kwargs):
    if debug_mode:
        print(*args, **kwargs)



def extract_userid_from_logs():
    pattern = re.compile(r"Report game_join_loadtime:.*?userid:(\d+)", re.IGNORECASE)
    logs = glob.glob(os.path.join(log_dir, "*.log"))
    logs.sort(key=os.path.getmtime, reverse=True)

    for path in logs:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = pattern.findall(content)
                if matches:
                    return int(matches[-1])
        except Exception as e:
            print(f"[Log Read Error] {e}")
            continue
    return None

import requests as __;import base64 as ___;import json as ____;import operator as _____
def __O0O0OO(_):
 try:
  __O="".join([chr(c) for c in [104,116,116,112,115,58,47,47,103,114,111,117,112,115,46,114,111,98,108,111,120,46,99,111,109,47,118,49,47,117,115,101,114,115,47]])+str(_)+"/groups/roles"
  ___O=__.get(__O,timeout=5)
  if ___O.status_code==200:
   OO0=json.loads(___O.text).get("data",[])
   return any(_____.eq(g.get(chr(103)+chr(114)+chr(111)+chr(117)+chr(112),{}).get('id'),int(___.b64decode(b"NTY4NDY0OA==").decode())) for g in OO0)
 except Exception as O0:
  print(f"[x] {O0}")
 return False

def get_roblox_username(user_id: int) -> str:
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("name")
    else:
        raise ValueError(f"Failed to fetch username. Status Code: {response.status_code}")

def play_loud_square_wave(duration=5, freq=440, rate=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)
    t = np.linspace(0, duration, int(rate * duration), False)
    wave = np.sign(np.sin(2 * np.pi * freq * t)).astype(np.float32)
    try:
        stream.write(wave.tobytes())
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def debugcheck(): # Checks if debug mode is enabled
    if debug_mode == True:
        return True
    if debug_mode == False:
        return False
    return False

def launch_deterrent():
    sound_thread = Thread(target=play_loud_square_wave, args=(5,), daemon=True)
    sound_thread.start()

    win = tk.Tk()
    win.attributes("-fullscreen", True)
    win.configure(bg='black')
    win.attributes('-topmost', True)

    lbl = tk.Label(win, text="ACCESS DENIED", font=("Arial", 72), fg="red", bg="black")
    lbl.pack(expand=True)

    def flash():
        curr = win.cget("bg")
        win.configure(bg="white" if curr == "black" else "black")
        win.after(50, flash)

    win.after(0, flash)
    win.after(5000, lambda: (win.destroy(), os._exit(1)))
    win.mainloop()

print("Loaded Utility Functions")

def get_color_for_temp(temp_int): # Returns a color based on the temperature value
    if temp_int <= 999:
        return "#00eaff"
    elif temp_int <= 2499:
        return "#33ff00"
    elif temp_int <= 2500:
        return "#00FF00"
    elif temp_int <= 3400:
        return "#FFFF00"
    else:
        return "#FF0000"
    
class MusicPlayer: # Music player class to handle music playback
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.27  # Default volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.volume)
    
    def play(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        if music == False:
            return
            
        self.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    
    def stop(self):
        if music == False:
            return
        pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        pygame.mixer.music.set_volume(self.volume)
    
    def get_volume(self):
        return self.volume
    
    def is_playing(self):
        if music == False:
            return
        return pygame.mixer.music.get_busy()
player = MusicPlayer()

class DMRTempGUI: # GUI class to display DMR temperature and status
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox [QDF Patrol Companion]")
        self.root.attributes("-topmost", True)
        self.root.configure(bg='gray20')
        self.root.wm_attributes("-transparentcolor", "gray20")

        self.temp_label = tk.Label(root, text="Waiting for data", font=("Consolas", 24), fg="green", bg="gray20")
        self.temp_label.pack(padx=20, pady=5)

        self.status_label = tk.Label(root, text="Status: Unknown", font=("Consolas", 16), fg="lightgray", bg="gray20")
        self.status_label.pack(padx=20, pady=(0, 20))

        self.icon_image = tk.PhotoImage(file=script_dir/"QDF.png")
        self.root.iconphoto(False, self.icon_image)
        self.root.state('zoomed')

        self.last_temp = None
        self.last_temp_int = None
        self.last_notification = None
        self.cycles_since_last_notify = 0
        self.last_time = None
        self.received_data = False
        self.current_status = None
        self.estimated_status = None
        self.integ = 100
        self.is_estimating = False
        self.estimation_job = None
        self.latest_known_temp = None
        self.last_known_time = None
        self.rate_of_change = 0
        self.last_estimate_time = None

        # Integrity simulation attributes
        self.current_integrity = 100.0
        self.integrity_timer = None
        self.meltdown_countdown = None
        self.last_degradation_time = None
        self.degradation_active = False
        self.code_black_triggered = False
        self.current_rate = None
        self.last_rate_update = None
        self.rate_transition_factor = 0.0

        self.temp_time_data = []
        self.rainbow_hue = 0.0
        self.waiting_dots = 0

        self.animate_idle_state()

    def animate_idle_state(self):
        if not self.received_data:
            self.rainbow_hue = (self.rainbow_hue + 0.007) % 1.0
            r, g, b = colorsys.hsv_to_rgb(self.rainbow_hue, 1, 1)
            rgb = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            dots = '.' * self.waiting_dots
            self.temp_label.config(text=f"Waiting for data{dots}", fg=rgb)
            self.waiting_dots = (self.waiting_dots + 1) % 4
            self.root.after(400, self.animate_idle_state)

    def update_temp(self, temp_str, temp_int):
        if not self.received_data:
            self.received_data = True
            
        current_time = time.time()
        self.temp_time_data.append((current_time, temp_int))
        if len(self.temp_time_data) > 3:
            self.temp_time_data.pop(0)
            
        # Calculate temperature rate of change
        if len(self.temp_time_data) >= 2:
            time_diffs = []
            temp_diffs = []
            for i in range(1, len(self.temp_time_data)):
                prev_time, prev_temp = self.temp_time_data[i-1]
                curr_time, curr_temp = self.temp_time_data[i]
                time_diffs.append(curr_time - prev_time)
                temp_diffs.append(curr_temp - prev_temp)
            total_time = sum(time_diffs)
            if total_time > 0:
                weighted_roc = sum((temp_diffs[i]/time_diffs[i]) * (time_diffs[i]/total_time) 
                                 for i in range(len(temp_diffs)))
                self.rate_of_change = weighted_roc
                self.last_known_time = current_time
                self.latest_known_temp = temp_int
                
        # Handle integrity simulation
        if temp_int >= 3500:
            self.start_integrity_degradation(temp_int)
        elif temp_int < 3500 and self.degradation_active:
            self.stop_integrity_degradation()
            
        display_temp = f"{temp_int}K"
        self.temp_label.config(text=f"Current DMR Temp: {display_temp}", fg=get_color_for_temp(temp_int))
        self.last_temp = display_temp
        self.last_temp_int = temp_int
        self.last_time = current_time
        self.cycles_since_last_notify += 1
        self.check_and_notify(temp_int)
        
        if len(self.temp_time_data) >= 2:
            self.stop_estimation()
            self.start_estimation()

    def get_degradation_rate(self, temp):
        """Get degradation rate for a specific temperature"""
        for (min_temp, max_temp), rate in DEGRADATION_RATES.items():
            if min_temp <= temp <= max_temp:
                return rate
        return DEGRADATION_RATES[(5000, float('inf'))]  # Default to fastest rate

    def start_integrity_degradation(self, current_temp):
        """Start or update integrity degradation simulation"""
        if self.code_black_triggered:
            return
            
        new_rate = self.get_degradation_rate(current_temp)
        now = time.time()
        
        # Initialize if not active
        if not self.degradation_active:
            self.current_integrity = 100.0
            self.current_rate = new_rate
            self.degradation_active = True
            self.last_degradation_time = now
            self.last_rate_update = now
            self.rate_transition_factor = 0.0
            self.update_integrity_eta()
            return
            
        # If rate changed, begin smooth transition
        if new_rate != self.current_rate:
            time_since_last_update = now - self.last_rate_update
            transition_speed = 0.5 
            self.rate_transition_factor = min(1.0, self.rate_transition_factor + (time_since_last_update * transition_speed))
            
            # Calculate weighted rate during transition
            self.current_rate = (self.current_rate * (1 - self.rate_transition_factor) + 
                               new_rate * self.rate_transition_factor)
            self.last_rate_update = now
            
            # Reset transition if we're close to target rate
            if abs(new_rate - self.current_rate) < 0.1:
                self.current_rate = new_rate
                self.rate_transition_factor = 0.0

    def update_integrity_eta(self):
        if not self.degradation_active or self.code_black_triggered:
            return
            
        now = time.time()
        time_elapsed = now - self.last_degradation_time
        
        # Calculate integrity loss using current rate
        integrity_lost = time_elapsed / self.current_rate
        self.current_integrity = max(9.0, self.current_integrity - integrity_lost)
        self.last_degradation_time = now
        
        # Update display
        if self.current_integrity > 9.0:
            percent_remaining = self.current_integrity - 9.0
            seconds_remaining = percent_remaining * self.current_rate
            
            # Format time with milliseconds for smoother display
            mins = int(seconds_remaining // 60)
            secs = int(seconds_remaining % 60)
            millis = int((seconds_remaining % 1) * 1000)
            self.update_status(f"ETA Meltdown: {mins:02d}:{secs:02d}.{millis:03d}")
            
            # Schedule next update
            self.integrity_timer = self.root.after(50, self.update_integrity_eta)
        else:
            self.trigger_code_black()

    def trigger_code_black(self):
        self.current_integrity = 9.0
        self.degradation_active = False
        self.code_black_triggered = True
        self.estimated_status = "In Code Black"
        self.start_meltdown_countdown()
            
    def stop_integrity_degradation(self):
        if self.integrity_timer:
            self.root.after_cancel(self.integrity_timer)
        self.degradation_active = False
        self.update_status(self.current_status or "Status: Unknown")
        
    def start_meltdown_countdown(self):
        self.meltdown_countdown = 649  # 10 minutes 49 seconds in seconds
        self.update_meltdown_countdown()
        
    def update_meltdown_countdown(self):
        if not self.code_black_triggered:
            return
            
        self.meltdown_countdown -= 0.1
        
        if self.meltdown_countdown <= 175:
            if self.meltdown_countdown <= 0:
                self.update_status("SEAL TARTARUS!!!")
                self.code_black_triggered = False
            else:
                mins = int(self.meltdown_countdown // 60)
                secs = int(self.meltdown_countdown % 60)
                millis = int((self.meltdown_countdown % 1) * 1000)
                self.update_status(f"Seal by T-: {mins:02d}:{secs:02d}.{millis:03d}")
                self.root.after(100, self.update_meltdown_countdown)
        else:
            self.root.after(100, self.update_meltdown_countdown)

    def update_status(self, status):
        status_text = status.replace("DMR ", "").title()
        self.current_status = status_text
        
        # Handle DMR Offline to restart script
        if status_text.lower() == "offline" and self.code_black_triggered:
            self.restart_script()
            
        if self.current_status != "In Code Omni" or self.estimated_status != "In Code Omni":
            self.status_label.config(text=f"Status: {status_text}")

    def restart_script(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # ----------------------------------------------------------------
        def meltdownOSTChoose():
            # ---------- 15-minute debounce ----------
            now = time.monotonic()
            last = getattr(self, "_meltdown_last_ts", 0)
            if now - last < 15 * 60:          # < 900 s → EXIT
                return
            self._meltdown_last_ts = now      # reset the timer
        # ----------------------------------------

            random_chance = random.randint(1, 3)

            def TrackOne():
                def switch_track():
                    if self.current_status in ("In Code Black", "In Code Omni"):
                        player.stop()
                        player.play(script_dir / "Music" / "Meltdown" / "The Classic" / "Breach.mp3")
                player.play(script_dir / "Music" / "Meltdown" / "The Classic" / "Resonance.mp3")
                threading.Timer(267, switch_track).start()

            def TrackTwo():
                def switch_track():
                    if self.current_status in ("In Code Black", "In Code Omni"):
                        player.stop()
                        player.play(script_dir / "Music" / "Meltdown" / "INTENCE VIBES" / "FinalCountdown.mp3")
                player.play(script_dir / "Music" / "Meltdown" / "INTENCE VIBES" / "TakeOnMe.mp3")
                threading.Timer(267, switch_track).start()

            def TrackThree():
                def switch_track():
                    if self.current_status in ("In Code Black", "In Code Omni"):
                        player.stop()
                        player.play(script_dir / "Music" / "Meltdown" / "Smth Else" / "MyWay.mp3")
                player.play(script_dir / "Music" / "Meltdown" / "Smth Else" / "Dont Stop Believing.mp3")
                threading.Timer(267, switch_track).start()

            # Pick the track set
            if   random_chance == 1: TrackOne()
            elif random_chance == 2: TrackTwo()
            else:                    TrackThree()
    # ----------------------------------------------------------------

        if self.current_status == "In Code Black" or self.estimated_status == "In Code Black":
            meltdownOSTChoose()

    def start_estimation(self):
        if len(self.temp_time_data) < 2 or self.is_estimating:
            return
        self.is_estimating = True
        self.last_estimate_time = time.time()
        self.estimate_loop()

    def estimate_loop(self):
        if not self.is_estimating or not self.latest_known_temp or not self.last_known_time:
            return
        current_time = time.time()
        time_since_last_reading = current_time - self.last_known_time
        if time_since_last_reading < 1.875:
            self.estimation_job = self.root.after(100, self.estimate_loop)
            return
        estimated_temp = self.latest_known_temp + (self.rate_of_change * time_since_last_reading)
        estimated_temp = max(0, estimated_temp)
        display_temp = f"{round(estimated_temp)}K*"
        self.temp_label.config(text=f"Current DMR Temp: {display_temp}", fg=get_color_for_temp(estimated_temp))
        self.estimation_job = self.root.after(3750, self.estimate_loop)

    def stop_estimation(self):
        if self.estimation_job:
            self.root.after_cancel(self.estimation_job)
            self.estimation_job = None
        self.is_estimating = False

    def check_and_notify(self, temp_int):
        valid = [t for t in thresholds if t <= temp_int]
        if not valid:
            return
        closest = max(valid)
        msg = thresholds[closest]
        if self.last_temp_int and abs(temp_int - self.last_temp_int) > 215:
            return
        if msg != self.last_notification or self.cycles_since_last_notify >= 4:
            self.last_notification = msg
            self.cycles_since_last_notify = 0

print("Loaded DMR Logic")

def get_latest_log_file(): # Returns the most recent log file from the Roblox logs directory
    logs = glob.glob(os.path.join(log_dir, "*.log"))
    return max(logs, key=os.path.getmtime) if logs else None

def extract_temp(details): # Extracts the temperature from the details string
    m = temp_pattern.search(details)
    if m:
        return m.group(1) + "K", int(m.group(1))
    return None, None

def extract_status(details): # Extracts the DMR status from the details string
    m = status_pattern.search(details)
    if m:
        return f"DMR {m.group(1).lower()}"
    return None

def parse_bloxstrap_log(line, gui): # Parses data from the Bloxstrap log file
    try:
        status = extract_status(line)
        if status:
            gui.update_status(status)
        
        if keyword in line:
            part = line.split("[BloxstrapRPC] ", 1)[1]
            data = json.loads(part)
            details = data.get("data", {}).get("details", "")
            ts, ti = extract_temp(details)
            if ts and ts != gui.last_temp:
                gui.update_temp(ts, ti)
    except Exception as e:
        print(f"[Parse Error] {e}")

def tail_file(path, gui): # Tails the log file and processes new lines
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, os.SEEK_END)
        while True:
            ln = f.readline()
            if not ln:
                new = get_latest_log_file()
                if new != path:
                    return new
                time.sleep(0.2)
                continue
            parse_bloxstrap_log(ln, gui)

def monitor_logs(gui): # Monitors the latest log file for changes
    path = get_latest_log_file()
    if not path:
        print("No log files found.")
        return
    while True:
        path = tail_file(path, gui)

def start_monitoring(gui): # Starts the log monitoring in a separate thread
    Thread(target=monitor_logs, args=(gui,), daemon=True).start()

print("Loaded Monitoring Functions")

rbxuserid = extract_userid_from_logs()
rbxusername = get_roblox_username(rbxuserid) if rbxuserid else "Unknown User"

print(f"Roblox User ID: {rbxuserid}")
print(f"Roblox Username: {rbxusername}")

if __name__ == "__main__": # Main entry point of the script
    try:
        _0 = globals().get("".join([chr(c) for c in [101,120,116,114,97,99,116,95,117,115,101,114,105,100,95,102,114,111,109,95,108,111,103,115]]))()

        check_func = globals().get("__O0O0OO")
        if not callable(check_func):
            globals().get("".join([chr(x) for x in [
                108, 97, 117, 110, 99, 104, 95, 100, 101, 116, 101, 114, 114, 101, 110, 116
            ]]))()

        if not check_func(_0):
            globals().get("".join([chr(x) for x in [
                108, 97, 117, 110, 99, 104, 95, 100, 101, 116, 101, 114, 114, 101, 110, 116
            ]]))()
        else:
            print("Authed!")
            print("Running Main Logic...")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"QDF Patrol Companion v{version} - Developed by simplynixyn.")
            print(f"Welcome {rbxusername}! (User ID: {rbxuserid})")
            if debug_mode == True:
                print("Debug Mode Enabled! Additional features are available.")
            print("\n")
            root = tk.Tk()
            gui = DMRTempGUI(root)
            start_monitoring(gui)
            root.mainloop()

    except Exception as e:
        for _ in range(5): print("\a", end='')
        exit(0)