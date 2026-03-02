import os
import requests

def send_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    city = "Bangkok"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=th"

    if not api_key:
        print("❌ ไม่พบ WEATHER_API_KEY")
        return
    if not webhook_url:
        print("❌ ไม่พบ DISCORD_WEBHOOK")
        return

    try:
        response = requests.get(url, timeout=10)
        res = response.json()

        # ✅ พิมพ์ดู Structure จริงๆ ก่อน
        print(f"📦 Response ทั้งหมด: {res}")

        # ✅ ตรวจสอบ cod (API คืนค่าเป็น int หรือ string ก็ได้)
        cod = res.get("cod")
        if str(cod) == "200":  # ✅ แปลงเป็น string ก่อนเปรียบเทียบ

            # ✅ ตรวจสอบว่า key มีอยู่จริงก่อนดึงค่า
            main = res.get("main", {})
            weather_list = res.get("weather", [])

            temp = main.get("temp", "ไม่มีข้อมูล")
            feels_like = main.get("feels_like", "ไม่มีข้อมูล")
            humidity = main.get("humidity", "ไม่มีข้อมูล")

            # ✅ ตรวจสอบว่า weather เป็น list และมีข้อมูลก่อน
            if isinstance(weather_list, list) and len(weather_list) > 0:
                desc = weather_list.get("description", "ไม่มีข้อมูล")
            else:
                desc = "ไม่มีข้อมูล"
                print(f"⚠️ weather_list ผิดปกติ: {weather_list}")

            message = (
                f"📢 **รายงานอากาศวันนี้**\n"
                f"📍 เมือง: {city}\n"
                f"🌡️ อุณหภูมิ: {temp}°C\n"
                f"🤔 รู้สึกเหมือน: {feels_like}°C\n"
                f"💧 ความชื้น: {humidity}%\n"
                f"☁️ สภาพอากาศ: {desc}"
            )

            discord_res = requests.post(
                webhook_url,
                json={"content": message},
                timeout=10
            )

            if discord_res.status_code == 204:
                print("✅ สำเร็จ! ส่งข้อมูลเข้า Discord เรียบร้อย")
            else:
                print(f"⚠️ Discord Error: {discord_res.status_code} → {discord_res.text}")

        else:
            print(f"⚠️ API Error cod={cod}: {res.get('message')}")

    except requests.exceptions.ConnectionError:
        print("💥 ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้")
    except requests.exceptions.Timeout:
        print("💥 หมดเวลาการเชื่อมต่อ (Timeout)")
    except TypeError as e:
        print(f"💥 TypeError: {e}")
        print(f"📦 ข้อมูลที่ได้รับ: {res}")  # ✅ ดูว่า res หน้าตาเป็นยังไง
    except Exception as e:
        print(f"💥 เกิดข้อผิดพลาด: {type(e).__name__} → {e}")

if __name__ == "__main__":
    send_weather()
