from flask import Flask, request, jsonify
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

app = Flask(__name__)

def initialize_driver():
    """Initialize Selenium Chrome WebDriver"""
    chromedriver_autoinstaller.install()  # Auto-install ChromeDriver if not found

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=options)

def scroll_to_load_comments(driver):
    """Scroll down the page to load more comments"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(5):  # Adjust scrolling attempts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_comments(url):
    """Scrape comments from the given Facebook post URL"""
    driver = None
    try:
        driver = initialize_driver()
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        scroll_to_load_comments(driver)

        comments = []
        elements = driver.find_elements(By.CSS_SELECTOR, "div[dir='auto']")
        
        for i, element in enumerate(elements[:20]):  # Limit to 20 comments
            text = element.text.strip()
            if text:
                comments.append(text)
        
        return {"comments": comments}
    
    except WebDriverException as e:
        return {"error": f"Failed to scrape comments: {str(e)}"}
    
    finally:
        if driver:
            driver.quit()

@app.route('/api/comments', methods=['GET'])
def get_comments():
    """API endpoint to fetch comments"""
    fb_url = request.args.get('url')  # Get URL from query parameters
    
    if not fb_url:
        return jsonify({"error": "URL parameter is required"}), 400
    
    try:
        comments = extract_comments(fb_url)
        return jsonify(comments)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
