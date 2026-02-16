import requests
import time

# URL of your local app
URL = "http://127.0.0.1:5000/"


def check_speed(username):
    start = time.perf_counter()
    # We send a wrong password. We only care about how long the "No" takes.
    requests.post(URL, data={"username": username, "password": "wrong_password"})
    return time.perf_counter() - start


print("--- ⏱️ MEASURING RESPONSE TIMES ---")

# 'admin' exists in your database
time_valid = check_speed("admin")
print(f"Valid User (admin):   {time_valid:.4f} seconds")

# 'ghost' does not exist
time_invalid = check_speed("ghost")
print(f"Invalid User (ghost): {time_invalid:.4f} seconds")

if time_valid > time_invalid * 5:
    print("\n🚨 RESULT: VULNERABLE! Significant timing leak detected.")
else:
    print("\n✅ RESULT: SECURE. Responses are consistent.")
