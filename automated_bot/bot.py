import json
import random

import requests


BASE_URL = "http://127.0.0.1:8000/api"


class Bot:
    def __init__(self, config_file):
        self.config = self.parse_config(config_file)

    def get_jwt(self, username, password):
        response = requests.post(
            f"{BASE_URL}/user/token/", data={"username": username, "password": password}
        )
        if response.status_code == 200:
            access_token = response.json()["access"]
            return access_token
        else:
            print(f"Failed to get JWT for user {username}.")
            return None

    def signup_users(self):
        for i in range(self.config["number_of_users"]):
            username = f"user{i}"
            password = f"password{i}"

            response = requests.post(
                f"{BASE_URL}/user/register/",
                json={"username": username, "password": password},
            )

            if response.status_code == 201:
                print(f"User {username} signed up successfully")
            else:
                print(response)
                print(f"Error with {response.status_code} status code.")

    def create_post(self, user, token):
        headers = {
            "Authorize": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        num_posts = random.randint(1, self.config["max_posts_per_user"])

        for i in range(num_posts):
            content = f"Automated post by {user}. Post number: #{i}"
            response = requests.post(
                f"{BASE_URL}/post/posts/",
                json={"content": content},
                headers=headers,
            )
            print(response)

            if response.status_code == 201:
                print(f"{user} created a post {content.split(':')[1]}")
            else:
                print(f"Something went wrong while creating a post #{i} by {user}")

    def like_posts(self, username, token):
        headers = {
            "Authorize": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        posts = requests.get(f"{BASE_URL}/post/posts", headers=headers)
        num_likes = random.randint(1, self.config["max_likes_per_user"])

        for _ in range(num_likes):
            post_id = random.randint(1, len(posts.json()))

            response = requests.get(
                f"{BASE_URL}/post/posts/{post_id}/like", headers=headers
            )
            print(
                f"{username} tried to like a post #{post_id}.\n"
                f"Result: {response.status_code} - {response.json()}"
            )

    def parse_config(self, config_file):
        with open(config_file, "r") as input_file:
            return json.load(input_file)


if __name__ == "__main__":
    config_file = "config.json"
    bot = Bot(config_file)
    bot.signup_users()

    for i in range(0, bot.config["number_of_users"]):
        token = bot.get_jwt(f"user{i}", f"password{i}")

        bot.create_post(f"user{i}", token)

    for i in range(0, bot.config["number_of_users"]):
        token = bot.get_jwt(f"user{i}", f"password{i}")
        bot.like_posts(f"user{i}", token)
