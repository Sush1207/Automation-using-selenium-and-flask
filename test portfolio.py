import threading
import time
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Flask App Setup
app = Flask(__name__)

USER_DATA = {"testuser": "testpassword"}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in USER_DATA and USER_DATA[username] == password:
        return "<h1 id='welcome-message'>Welcome, {}!</h1>".format(username)
    else:
        return "<h1 id='error-message'>Login Failed</h1>", 401

def run_flask():
    app.run(debug=False, port=5000, use_reloader=False)

# Selenium Tests
driver = webdriver.Chrome()

def test_youtube_play():
    """Automated test to open YouTube and play the Gata song"""
    try:
        driver.get("https://www.youtube.com/")  # Open YouTube
        time.sleep(3)  # Wait for YouTube to load

        # Find the search bar and search for 'Gata only song'
        search_bar = driver.find_element(By.NAME, "search_query")
        search_bar.send_keys("gata only song")
        search_bar.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for search results to load

        # Click on the first video in the search results
        first_video = driver.find_element(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
        first_video.click()
        time.sleep(50)

        print("YouTube Play Test Passed!")
    except Exception as e:
        print(f"YouTube Play Test Failed: {e}")

def test_ecommerce_search():
    try:
        driver.get("https://www.amazon.in/")
        search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.send_keys("laptop")
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)

        results = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
        assert len(results) > 0, "Test Failed: No search results found."
        print("E-commerce Search Test Passed!")
    except Exception as e:
        print(f"E-commerce Search Test Failed: {e}")

def test_login_functionality():
    try:
        driver.get("http://127.0.0.1:5000")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("testpassword")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        success_message = driver.find_element(By.ID, "welcome-message").text
        assert "Welcome" in success_message, "Test Failed: Login was unsuccessful."
        print("Login Functionality Test Passed!")
    except Exception as e:
        print(f"Login Functionality Test Failed: {e}")

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Wait a moment for Flask to initialize
    time.sleep(1)

    try:
        test_youtube_play()  # Replace calculator test with playing YouTube Gata song
        test_ecommerce_search()
        test_login_functionality()
    finally:
        driver.quit()
