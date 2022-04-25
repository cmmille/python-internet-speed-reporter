import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class InternetSpeedTwitterBot:
    def __init__(self):

        self.driver = self.init_webdriver()
        self.up_speed = ''
        self.down_speed = ''
        self.result_id = ''

    def init_webdriver(self):
        user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.002.127 Safari/537.36'
        service = Service("C:/Users/Chris/.wdm/drivers/chromedriver/win32/100.0.4896.60/chromedriver.exe")

        options = webdriver.ChromeOptions()
        options.add_argument("window-size=800,1000")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        options.add_argument(f"user-agent={user_agent}")

        return webdriver.Chrome(service=service, options=options)

    # Get internet speed from speedtest.net
    def get_internet_speed(self):
        url = "https://www.speedtest.net/"
        self.driver.get(url)

        # Run speed test
        print("Running speed test...")
        self.driver.find_element(By.CSS_SELECTOR, '.start-text').click()
        for i in range(45):
            print(i)
            time.sleep(1)

        # Get Results
        self.down_speed = float(self.driver.find_element(By.CSS_SELECTOR, '.result-item-download > .result-data > span').text)
        self.up_speed = float(self.driver.find_element(By.CSS_SELECTOR, '.result-item-upload > .result-data > span').text)
        self.result_id = self.driver.find_element(By.CSS_SELECTOR, '.result-data > a').text

        # Print results
        self.print_result()

    # Send tweet to internet provider with network details
    def tweet_at_provider(self, username, password, paid_speed):
        try:
            url = "https://twitter.com/i/flow/login"
            self.driver.get(url)

            # Username
            time.sleep(3)
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
            username_input.send_keys(username)
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]').click()
            time.sleep(3)

            # Password
            password_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password_input.send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div').click()

            # Compose Tweet
            time.sleep(3)
            tweet_box = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
            composed_tweet = self.compose_tweet()
            tweet_box.send_keys(composed_tweet)

            # Send Tweet
            self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]').click()
        finally:
            self.driver.quit()

    def print_result(self):
        print(f"ResultID: {self.result_id}")
        print(f"Down: {self.down_speed} mbps")
        print(f"Up: {self.up_speed} mbps")

    def compose_tweet(self, paid_speed):
        return f"Hey Internet_provider, why is my internet speed only {self.down_speed} mbps down/ {self.up_speed} mbps up? I pay for {paid_speed} mbps down. https://www.speedtest.net/'{self.result_id}"
