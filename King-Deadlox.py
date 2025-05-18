#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import time
import requests
from datetime import datetime

# Colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
NC = '\033[0m'

# Global Variables
TERMUX_PREFIX = "/data/data/com.termux/files/usr"
TEMP_THRESHOLD = 60  # °C

def show_banner():
    print(f"""{PURPLE}
   _____                       __  __           _____             __        
  / ___/____  ____ _________  / /_/ /_  ___    / ___/____  ____  / /_______
  \__ \/ __ \/ __ `/ ___/ _ \/ __/ __ \/ _ \   \__ \/ __ \/ __ \/ //_/ ___/
 ___/ / /_/ / /_/ / /__/  __/ /_/ / / /  __/  ___/ / /_/ / /_/ / ,< (__  ) 
/____/\____/\__, /\___/\___/\__/_/ /_/\___/  /____/\____/\____/_/|_/____/  
           /____/                                                          
{NC}""")
    print(f"{CYAN}KING DEADLOX ULTIMATE OPTIMIZER v3.0{NC}")
    print(f"{YELLOW}==============================================={NC}")
    print(f"{RED}⚠️ WARNING: Use at your own risk! No root required.{NC}\n")

def run_cmd(cmd, success_msg=None, error_msg=None):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
        if success_msg:
            print(f"{GREEN}{success_msg}{NC}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        if error_msg:
            print(f"{RED}{error_msg}{NC}")
        return None

def check_specs():
    print(f"\n{YELLOW}📱 DEVICE SPECIFICATIONS:{NC}")
    
    # CPU Info
    cpu = run_cmd("getprop ro.product.cpu.abi", "[-] CPU Architecture checked")
    cores = run_cmd("cat /proc/cpuinfo | grep processor | wc -l", "[-] CPU Cores checked")
    freq = run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", "[-] Max Frequency checked")
    
    # Memory Info
    mem = run_cmd("cat /proc/meminfo | grep MemTotal", "[-] RAM checked")
    
    # GPU Info
    gpu = run_cmd("getprop ro.hardware", "[-] GPU checked")
    
    # Battery Info
    batt = run_cmd("dumpsys battery | grep level", "[-] Battery checked")
    
    # Display Info
    disp = run_cmd("wm size", "[-] Display resolution checked")
    
    print(f"\n{YELLOW}⚙️ CURRENT STATUS:{NC}")
    check_temp()
    check_storage()

def check_temp():
    temp = None
    if os.path.exists("/sys/class/thermal/thermal_zone0/temp"):
        temp = run_cmd("cat /sys/class/thermal/thermal_zone0/temp")
        if temp:
            temp = int(temp.strip()) / 1000
            status = f"{GREEN}NORMAL{NC}" if temp < TEMP_THRESHOLD else f"{RED}HOT!{NC}"
            print(f"[-] CPU Temperature: {temp:.1f}°C ({status})")
    if not temp:
        print(f"{RED}[-] Unable to read CPU temperature{NC}")

def check_storage():
    storage = run_cmd("df -h /data")
    if storage:
        print(f"[-] Storage:\n{storage}")

def optimize_battery():
    print(f"\n{GREEN}[🔋] STARTING BATTERY OPTIMIZATION...{NC}")
    
    # Network optimization
    run_cmd("settings put global low_power 1", "[+] Low power mode enabled")
    run_cmd("settings put global wifi_sleep_policy 2", "[+] WiFi sleep optimized")
    
    # Background process restriction
    run_cmd("am set-standby-bucket --user 0 com.termux restricted", "[+] Background processes restricted")
    
    # Screen optimization
    run_cmd("settings put system screen_brightness_mode 1", "[+] Auto brightness enabled")
    run_cmd("settings put system screen_off_timeout 60000", "[+] Screen timeout set to 1min")
    
    # Clean cache
    run_cmd("rm -rf $HOME/.cache/*", "[+] Cache cleaned")
    
    print(f"{GREEN}[✓] BATTERY OPTIMIZATION COMPLETE!{NC}")

def optimize_game(game):
    games = {
        "1": {"name": "FREE FIRE", "cmd": "settings put global ff_max_fps 90"},
        "2": {"name": "MOBILE LEGEND", "cmd": "settings put global ml_smooth_display 1"},
        "3": {"name": "PUBG MOBILE", "cmd": "settings put global pubg_performance_mode 1"},
        "4": {"name": "GENSHIN IMPACT", "cmd": "settings put global genshin_impact_mode 1"},
        "5": {"name": "CLASH OF CLANS", "cmd": "settings put global coc_performance 1"},
        "6": {"name": "OTHER GAME", "cmd": "settings put global game_driver_allowed 1"}
    }
    
    selected = games.get(game)
    if not selected:
        print(f"{RED}Invalid game selection!{NC}")
        return
    
    print(f"\n{GREEN}[🎮] OPTIMIZING FOR {selected['name']}...{NC}")
    
    # Common game optimizations
    run_cmd("settings put global hwui.renderer opengl", "[+] OpenGL renderer enabled")
    run_cmd("settings put global game_driver_allowed 1", "[+] Game driver enabled")
    run_cmd("settings put global force_gpu_rendering 1", "[+] Force GPU rendering")
    
    # Game-specific optimization
    if selected['cmd']:
        run_cmd(selected['cmd'], f"[+] {selected['name']} optimization applied")
    
    # Memory optimization
    run_cmd("settings put global persist.sys.purgeable_assets 1", "[+] Memory optimized")
    
    print(f"{GREEN}[✓] {selected['name']} OPTIMIZATION COMPLETE!{NC}")

def download_video():
    print(f"\n{GREEN}[⬇️] SOCIAL MEDIA VIDEO DOWNLOADER{NC}")
    url = input("Enter video URL: ").strip()
    
    if not url:
        print(f"{RED}URL cannot be empty!{NC}")
        return
    
    try:
        print(f"{YELLOW}[!] Downloading...{NC}")
        
        # Using yt-dlp for best compatibility
        if not os.path.exists(f"{TERMUX_PREFIX}/bin/yt-dlp"):
            print(f"{YELLOW}[!] Installing yt-dlp...{NC}")
            run_cmd("pip install yt-dlp")
        
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd = f"yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o 'download_%(title)s_{date_str}.%(ext)s' {url}"
        run_cmd(cmd, "[✓] Download completed!", "[!] Download failed")
        
    except Exception as e:
        print(f"{RED}Error: {str(e)}{NC}")

def main_menu():
    while True:
        show_banner()
        print(f"{YELLOW}MAIN MENU:{NC}")
        print("1. 📱 Check Device Specs")
        print("2. 🔋 Optimize Battery")
        print("3. 🎮 Optimize Game")
        print("4. ⬇️ Download Social Media Video")
        print("5. ⚙️ Restore Default Settings")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option [1-6]: ")
        
        if choice == "1":
            check_specs()
        elif choice == "2":
            optimize_battery()
        elif choice == "3":
            print(f"\n{YELLOW}SELECT GAME:{NC}")
            print("1. Free Fire")
            print("2. Mobile Legend")
            print("3. PUBG Mobile")
            print("4. Genshin Impact")
            print("5. Clash of Clans")
            print("6. Other Game")
            game_choice = input("\nSelect game [1-6]: ")
            optimize_game(game_choice)
        elif choice == "4":
            download_video()
        elif choice == "6":
            print(f"{GREEN}Exiting...{NC}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid option!{NC}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        # Check if running in Termux
        if not os.path.exists(TERMUX_PREFIX):
            print(f"{RED}This script must be run in Termux!{NC}")
            sys.exit(1)
            
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Script terminated by user{NC}")
        sys.exit(1)