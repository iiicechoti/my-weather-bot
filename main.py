import os
import requests
import json

def send_weather():
    # 1. ดึงค่าความลับจาก GitHub Secrets
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    
    # 2. กำหนดค่าเมือง
    city = "Bangkok"
    
    # 3. สร้าง URL ที่ถูกต้อง (ตรวจสอบเส้นทาง /data/2.5/weather ให้ครบนะครับ)
    url = f"https://api.openweathermap.org{city}&appid={api_key}&units=metric&lang=th"
    
    # 4. ดึงข้อมูลสภาพอากาศ
    response = requests.get(url)
    res = response.json()

    # 5. ตรวจสอบสถานะการดึงข้อมูล (200 คือสำเร็จ)
    if res.get("cod") == 200:
        temp = res['main']['temp']
        # ดึงรายละเอียดสภาพอากาศ (ต้องระบุ [0] เพราะข้อมูลเป็นรายการ)
        desc = res['weather'][0]['description']
        
        message = f"📢 **รายงานอากาศวันนี้**\n📍 เมือง: {city}\n🌡️ อุณหภูมิ: {temp}°C\n☁️ สภาพอากาศ: {desc}"
        
        # 6. ส่งเข้า Discord ผ่าน Webhook
        requests.post(webhook_url, json={"content": message})
        print("ส่งข้อมูลเข้า Discord สำเร็จ!")
    else:
        # ถ้าพัง จะพิมพ์บอกว่าพังเพราะอะไร (ดูได้ในหน้า Actions ของ GitHub)
        print(f"เกิดข้อผิดพลาดจาก API: {res.get('message')}")

if __name__ == "__main__":
    send_weather()
