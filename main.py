import os
import requests
import json

def send_weather():
    # 1. ดึงค่าความลับจาก GitHub Secrets
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    
    # 2. ลิงก์ที่ถูกต้อง (ห้ามมีดอกจันปน)
    city = "Bangkok"
    url = f"http://api.openweathermap.org{city}&appid={api_key}&units=metric&lang=th"
    
    # 3. ดึงข้อมูล
    res = requests.get(url).json()

    # 4. ตรวจสอบว่าดึงข้อมูลสำเร็จไหม
    if res.get("cod") == 200:
        temp = res['main']['temp']
        desc = res['weather'][0]['description']
        message = f"📢 **รายงานอากาศวันนี้**\nเมือง: {city}\nอุณหภูมิ: {temp}°C\nสภาพอากาศ: {desc}"
        
        # 5. ส่งเข้า Discord
        requests.post(webhook_url, json={"content": message})
    else:
        print(f"Error: {res.get('message')}")

if __name__ == "__main__":
    send_weather()
