import os
import requests
import json

def send_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    city = "Bangkok"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=th"

    # ✅ ตรวจสอบว่า Environment Variables มีค่าไหม
    if not api_key:
        print("❌ ไม่พบ WEATHER_API_KEY - กรุณาตั้งค่า Environment Variable")
        return
    if not webhook_url:
        print("❌ ไม่พบ DISCORD_WEBHOOK - กรุณาตั้งค่า Environment Variable")
        return

    print(f"🔗 กำลังเชื่อมต่อ URL: {url}")

    try:
        response = requests.get(url, timeout=10)  # ✅ เพิ่ม timeout

        # ✅ แสดง Status Code จริงๆ
        print(f"📡 Status Code: {response.status_code}")

        res = response.json()
        print(f"📦 Response: {res}")  # ✅ ดู Response เต็มๆ

        if res.get("cod") == 200:
            temp = res['main']['temp']
            desc = res['weather']['description']
            message = (
                f"📢 **รายงานอากาศวันนี้**\n"
                f"📍 เมือง: {city}\n"
                f"🌡️ อุณหภูมิ: {temp}°C\n"
                f"☁️ สภาพอากาศ: {desc}"
            )

            # ✅ ตรวจสอบผล Discord ด้วย
            discord_res = requests.post(webhook_url, json={"content": message}, timeout=10)
            print(f"📨 Discord Status: {discord_res.status_code}")

            if discord_res.status_code == 204:
                print("✅ สำเร็จ! ส่งข้อมูลเข้า Discord เรียบร้อย")
            else:
                print(f"⚠️ Discord Error: {discord_res.text}")
        else:
            print(f"⚠️ API Error: {res.get('message')}")

    except requests.exceptions.ConnectionError:
        print("💥 ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ - ตรวจสอบการเชื่อมต่อเน็ต")
    except requests.exceptions.Timeout:
        print("💥 หมดเวลาการเชื่อมต่อ (Timeout) - เซิร์ฟเวอร์ตอบสนองช้าเกินไป")
    except requests.exceptions.InvalidURL:
        print("💥 URL ไม่ถูกต้อง - ตรวจสอบ API Key หรือ URL อีกครั้ง")
    except Exception as e:
        print(f"💥 เกิดข้อผิดพลาด: {type(e).__name__} → {e}")  # ✅ แสดงประเภท Error ด้วย

if __name__ == "__main__":
    send_weather()
