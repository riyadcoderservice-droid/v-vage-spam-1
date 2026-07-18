# ======================== IMPORTS =======================
import asyncio
import os
import sys
import ssl
import random
import time
import aiohttp
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# আপনার প্রজেক্টের ফাইল ইম্পোর্ট
try:
    from xC4 import CrEaTe_ProTo, GeneRaTePk, EnC_Uid, DecodE_HeX, xBunnEr
    from xHeaders import Ua
    from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
except ModuleNotFoundError as e:
    print(f"\n❌ [ERROR] প্রয়োজনীয় ফাইল খুঁজে পাওয়া যায়নি: {e}")
    print("দয়া করে নিশ্চিত করুন xC4.py, xHeaders.py এবং Pb2 ফোল্ডারটি একই ডিরেক্টরিতে আছে।\n")
    sys.exit(1)

app = FastAPI(title="Free Fire Badge Spam API")

# =================== CONFIGURATION & HEADERS ===================
Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB54"
}

BADGE_VALUES = {
    "s1": 1048576,  # Craftland
    "s2": 32768,    # V-Badge
    "s3": 2048,     # Moderator
    "s4": 64,       # Small V-Badge
    "s5": 262144    # Pro Badge
}

# =================== UTILITY FUNCTIONS ===================
def load_accounts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "account.txt")
    accounts = []
    
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Format: uid:password\n")
        return accounts
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    uid, password = line.split(":", 1)
                    accounts.append((uid.strip(), password.strip()))
    except Exception as e:
        print(f"[DEBUG] ফাইল পড়তে সমস্যা হয়েছে: {str(e)}")
        
    return accounts

# =================== CRYPTO & HANDSHAKE HELPER FUNCTIONS ===================
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    return cipher.encrypt(padded_message)

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    return cipher.encrypt(padded_packet).hex()

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    headers = Hr.copy()
    headers["User-Agent"] = await Ua()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                return None, None
            resp_data = await response.json()
            return resp_data.get("open_id"), resp_data.get("access_token")

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.2"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30"
    major_login.system_hardware = "Handheld"
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_operator_a = "Verizon"
    major_login.network_type = "WIFI"
    major_login.network_type_a = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2"
    major_login.graphics_api = "OpenGLES3"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.login_open_id_type = 4
    major_login.access_token = access_token
    major_login.login_by = 3
    major_login.platform_sdk_id = 2
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.external_storage_total = 128512
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = 110731
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_total = 26628
    major_login.game_disk_storage_available = random.randint(18000, 25000)
    major_login.external_sdcard_total_storage = 119234
    major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
    major_login.library_path = "/data/app/base.apk"
    major_login.library_token = "hash|base.apk"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.supported_astc_bitset = 16383
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.channel_type = 3
    major_login.reg_avatar = 1
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.android_engine_init_flag = 110009
    
    return await encrypted_proto(major_login.SerializeToString())

async def MajorLogin(payload):
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await encrypt_packet(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# =================== BADGE PACKET BUILDER ===================
async def request_join_with_badge(target_uid, badge_value, key, iv, region="IND"):
    try:
        avatar_id = int(await xBunnEr())
        fields = {
            1: 33,  
            2: {
                1: int(target_uid),
                2: region.upper(),
                3: 1,
                4: 1,
                5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                6: "TG:[C][B][FF0000] @Beotherjk",
                7: 330,
                8: 1000,
                10: region.upper(),
                11: bytes([
                    49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                    97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49,
                    50, 48, 102, 53
                ]),
                12: 1,
                13: int(target_uid),
                14: {
                    1: 2203434355,
                    2: 8,
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                },
                16: 1,
                17: 1,
                18: 312,
                19: 46,
                23: bytes([16, 1, 24, 1]),
                24: avatar_id,
                26: {},
                27: {
                    1: 11,
                    2: 12999994075,
                    3: 9999
                },
                28: {},
                31: {
                    1: 1,
                    2: int(badge_value)
                },
                32: int(badge_value),
                34: {
                    1: int(target_uid),
                    2: 8,
                    3: b"\x0F\x06\x15\x08\x0A\x0B\x13\x0C\x11\x04\x0E\x14\x07\x02\x01\x05\x10\x03\x0D\x12"
                }
            },
            10: "en",
            13: {
                2: 1,
                3: 1
            }
        }
        
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
            
        return await GeneRaTePk(packet_hex, packet_type, key, iv)
    except Exception as e:
        print(f"Error creating badge packet: {e}")
        return None

# =================== SEQUENTIAL TIMER CONTROL ===================
async def run_timer_spam(accounts, target_uid, duration_sec):
    """অ্যাকাউন্টগুলো একের পর এক সিরিয়ালে ৫টি করে ব্যাজ পাঠাতে থাকবে যতক্ষণ না সময় শেষ হয়"""
    start_time = time.time()
    account_idx = 0
    total_packets_sent = 0
    
    while time.time() - start_time < duration_sec:
        if not accounts:
            break
            
        # সিরিয়াল অনুযায়ী পরবর্তী অ্যাকাউন্ট সিলেক্ট করা
        bot_uid, password = accounts[account_idx % len(accounts)]
        account_idx += 1
        
        print(f"[ACTIVE] অ্যাকাউন্ট পরিবর্তন: {bot_uid}")
        
        try:
            # Garena অথেন্টিকেশন
            open_id, access_token = await GeNeRaTeAccEss(bot_uid, password)
            if not open_id or not access_token:
                print(f"[-] অথেন্টিকেশন ফেইল্ড: {bot_uid}")
                continue
                
            pyl = await EncRypTMajoRLoGin(open_id, access_token)
            login_resp = await MajorLogin(pyl)
            if not login_resp:
                continue
                
            auth_data = await DecRypTMajoRLoGin(login_resp)
            token = auth_data.token
            key = auth_data.key
            iv = auth_data.iv
            timestamp = auth_data.timestamp
            account_uid = auth_data.account_uid
            url = auth_data.url
            region = getattr(auth_data, 'region', 'IND')
            
            # সার্ভার সকেট ইনফো
            login_raw = await GetLoginData(url, pyl, token)
            if not login_raw:
                continue
                
            login_decoded = await DecRypTLoGinDaTa(login_raw)
            online_ports = login_decoded.Online_IP_Port
            online_ip, online_port = online_ports.split(":")
            
            auth_token = await xAuThSTarTuP(int(account_uid), token, int(timestamp), key, iv)
            
            # সকেট কানেকশন
            reader, writer = await asyncio.open_connection(online_ip, int(online_port))
            try:
                writer.write(bytes.fromhex(auth_token))
                await writer.drain()
                await asyncio.sleep(0.5)
                
                # একই অ্যাকাউন্ট থেকে s1 থেকে s5 পর্যন্ত ৫টি রিকোয়েস্ট পাঠানো হচ্ছে
                for badge_name, badge_value in BADGE_VALUES.items():
                    # সময় শেষ হয়ে গেলে লুপ থেকে বের হয়ে যাবে
                    if time.time() - start_time >= duration_sec:
                        break
                        
                    badge_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
                    if badge_packet:
                        writer.write(badge_packet)
                        await writer.drain()
                        total_packets_sent += 1
                        print(f"   [+] পাঠানো হয়েছে: {badge_name} (বট: {bot_uid})")
                        
                    # সার্ভার স্প্যাম প্রোটেকশন এড়াতে নিরাপদ বিরতি (১.৫ সেকেন্ড)
                    await asyncio.sleep(1.5)
                    
            finally:
                writer.close()
                await writer.wait_closed()
                
        except Exception as e:
            print(f"[-] অ্যাকাউন্ট {bot_uid} এ সমস্যা হয়েছে: {e}")
            
        # আরেকটি অ্যাকাউন্টে যাওয়ার পূর্বে ১ সেকেন্ডের নিরাপত্তা বিরতি
        await asyncio.sleep(1.0)
        
    return total_packets_sent

# =================== API ENDPOINTS ===================
@app.get("/spam")
async def trigger_spam(
    target: str = Query(..., description="টার্গেট প্লেয়ারের UID"),
    duration: int = Query(30, description="কত সেকেন্ড স্প্যাম চলবে (সর্বোচ্চ ১২০ সেকেন্ড)", ge=5, le=120)
):
    accounts = load_accounts()
    if not accounts:
        raise HTTPException(status_code=400, detail="No accounts loaded in account.txt.")

    print(f"\n[START] {duration} সেকেন্ডের জন্য সিকোয়েন্সিয়াল স্প্যাম শুরু হচ্ছে...")
    
    # টাইমার ব্যাকগ্রাউন্ডে কাজ করবে
    total_sent = await run_timer_spam(accounts, target, duration)
    
    return {
        "target": target,
        "duration_seconds": duration,
        "total_requests_sent": total_sent,
        "status": "completed"
    }

# =================== RUNNER ===================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)