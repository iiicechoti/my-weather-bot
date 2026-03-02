import os
import requests
import json

def send_weather():
    # 1. ดึงค่าจาก GitHub Secrets (ต้องตั้งชื่อให้ตรงใน Settings)
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    
    # 2. ตั้งค่าเมือง
    city = "Bangkok"
    
    # 3. ลิงก์ API ที่ถูกต้องแม่นยำ (ห้ามแก้บรรทัดนี้)
    url = f"https://api.openweathermap.org{city}&appid={api_key}&units=metric&lang=th"
    
    # 4. ดึงข้อมูล
    try:
        response = requests.get(url)
        res = response.json()

        # 5. ตรวจสอบสถานะ (200 คือผ่าน)
        if res.get("cod") == 200:
            temp = res['main']['temp']
            # *** จุดสำคัญ: ต้องมี [0] เพราะข้อมูลอากาศมาเป็น List ***
            desc = res['weather'][0]['description']
            
            message = f"📢 **รายงานอากาศวันนี้**\n📍 เมือง: {city}\n🌡️ อุณหภูมิ: {temp}°C\n☁️ สภาพอากาศ: {desc}"
            
            # 6. ส่งเข้า Discord
            requests.post(webhook_url, json={"content": message})
            print("สำเร็จ! ส่งข้อมูลเข้า Discord เรียบร้อย")
        else:
            print(f"API Error: {res.get('message')} (เช็ก API Key ใน Secrets ว่าถูกต้องไหม)")
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    send_weather()
