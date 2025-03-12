from flask import Flask, request, render_template, send_file
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Homepage with URL input
@app.route('/')
def home():
    return render_template('index.html')

# Check redirection status
@app.route('/check_redirects', methods=['POST'])
def check_redirects():
    urls = request.form['urls'].splitlines()

    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    results = []
    
    for url in urls:
        try:
            driver.get(url)
            if driver.current_url != url:
                status_code = "301" if "301" in driver.page_source else "302"
                results.append([url, driver.current_url, status_code])
            else:
                results.append([url, "No Redirection", "200"])
        except Exception as e:
            results.append([url, "Error", str(e)])
        time.sleep(2)
    
    driver.quit()

    # Save results to CSV
    csv_file = 'redirect_status.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Original URL", "Redirected URL", "Status Code"])
        writer.writerows(results)

    return send_file(csv_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)