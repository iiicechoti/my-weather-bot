import os, requests, json

def send_weather():
    # 1. ดึงค่าความลับที่เราตั้งไว้
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    
    # 2. ดึงข้อมูลสภาพอากาศ (เปลี่ยนชื่อเมืองเป็น Bangkok หรือเมืองที่คุณอยู่)
    url = f"http://api.openweathermap.org{api_key}&units=metric&lang=th"
    res = requests.get(url).json()

    # 3. จัดข้อความ
    temp = res['main']['temp']
    desc = res['weather'][0]['description']
    message = f"📢 **รายงานอากาศวันนี้**\nอุณหภูมิ: {temp}°C\nสภาพอากาศ: {desc}"

    # 4. ส่งเข้า Discord
    requests.post(webhook_url, json={"content": message})

if __name__ == "__main__":
    send_weather()
