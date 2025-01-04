from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def send_request(self):
        self.client.get("/")  # Test qilinayotgan saytning URL'ini kiriting

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Har bir foydalanuvchi orasidagi kutish vaqti
