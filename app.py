# from locust import HttpUser, TaskSet, task, between

# class UserBehavior(TaskSet):
#     @task
#     def send_request(self):
#         self.client.get("/")  # Test qilinayotgan saytning URL'ini kiriting

# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     wait_time = between(1, 3)  # Har bir foydalanuvchi orasidagi kutish vaqti
import requests
import threading
import time

# Bloklangan IP manzillar ro'yxati
blocked_ips = set()

# IP manzillarni so'rovlarni kuzatish uchun limit
ip_request_count = {}
request_limit = 50  # Har bir IP uchun maksimal so'rovlar soni
time_window = 60  # Sekundlar ichida so'rovlar uchun vaqt oynasi

# So'rovni yuborish funksiyasi
def send_request(url, ip):
    if ip in blocked_ips:
        print(f"Bloklangan IP: {ip}")
        return

    # IP so'rovlarini kuzatish
    current_time = time.time()
    if ip not in ip_request_count:
        ip_request_count[ip] = []
    ip_request_count[ip] = [req_time for req_time in ip_request_count[ip] if current_time - req_time < time_window]
    ip_request_count[ip].append(current_time)

    if len(ip_request_count[ip]) > request_limit:
        print(f"IP {ip} bloklandi: juda ko'p so'rovlar")
        blocked_ips.add(ip)
        return

    # Asl so'rovni yuborish
    try:
        response = requests.get(url)
        print(f"IP: {ip}, Status code: {response.status_code}")
    except Exception as e:
        print(f"IP: {ip}, Error: {e}")

# Hujumni simulyatsiya qilish
def simulate_ddos(url, num_requests):
    threads = []
    for i in range(num_requests):
        ip = f"192.168.1.{i % 255}"  # Har bir foydalanuvchi uchun soxta IP manzil
        thread = threading.Thread(target=send_request, args=(url, ip))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

# URL va so'rovlar soni
url = "https://bitcoinbashorat.streamlit.app/"
simulate_ddos(url, 1000)
