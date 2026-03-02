import os
import requests
import json

def send_weather():
    # 1. ดึงค่าความลับจาก GitHub Secrets
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')

    # 2. ตั้งค่าชื่อเมือง
    city = "Bangkok"

    # 3. แก้ไข URL ให้ถูกต้อง ✅
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=th"

    try:
        # 4. ดึงข้อมูลสภาพอากาศ
        response = requests.get(url)
        res = response.json()

        # 5. ตรวจสอบว่าดึงข้อมูลสำเร็จไหม (รหัส 200 คือสำเร็จ)
        if res.get("cod") == 200:
            temp = res['main']['temp']
            desc = res['weather']['description']
            message = (
                f"📢 **รายงานอากาศวันนี้**\n"
                f"📍 เมือง: {city}\n"
                f"🌡️ อุณหภูมิ: {temp}°C\n"
                f"☁️ สภาพอากาศ: {desc}"
            )

            # 6. ส่งเข้า Discord ผ่าน Webhook
            requests.post(webhook_url, json={"content": message})
            print("✅ สำเร็จ! ส่งข้อมูลเข้า Discord เรียบร้อย")

        else:
            # ถ้า API ส่งข้อความผิดพลาดกลับมา
            print(f"⚠️ API Error: {res.get('message')}")

    except Exception as e:
        print(f"💥 เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# แก้ไข **name** → __name__ ✅
if __name__ == "__main__":
    send_weather()
