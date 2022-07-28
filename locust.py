from locust import HttpUser, task, between


class AppUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def home_page(self):
        self.client.get("/")

    @task
    def candlestick(self):
        self.client.get("/candlestick")

    @task
    def filter_tables(self):
        self.client.get("/filter_tables")

    @task
    def tables(self):
        self.client.get("/tables")
