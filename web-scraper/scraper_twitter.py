"""
This file contains code for scraping Twitter data.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# change the working directory to the current file's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_driver()->WebElement:
    """
    Initialize the browser driver
    """
    options: webdriver.ChromeOptions  = webdriver.ChromeOptions()

    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #options .add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    driver: WebElement = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

"""
def get_tweets(ticker: str="tsla",n: int=40):
    driver=init_driver()
    # login to twitter
    URL="https://twitter.com/i/flow/login"
    driver.get(URL)
    driver.implicitly_wait(60)

    input("Press enter once login is done... ")

    original_window=driver.current_window_handle

    # Accept cookies to make the banner disappear
    try:
        accept_cookies_btn = driver.find_element(
        "xpath", "//span[text()='Refuse non-essential cookies']/../../..")
        accept_cookies_btn.click()
    except NoSuchElementException:
        pass

    ticker = ticker.upper()
    driver.get(f"https://twitter.com/search?q=%24{ticker}")
    driver.implicitly_wait(10)

    df = pd.DataFrame({'date':[], 'tweet':[]})

    for _ in range(5):  # Retry loop
        try:
            time.sleep(1)
            for i in range(n):
                tweet_text_xpath=f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[{i+10}]/div/div/article/div/div/div[2]/div[2]/div[2]/div"
                tweet_element = driver.find_element(by=By.XPATH, value=tweet_text_xpath)
                tweet_text = tweet_element.text

                tweet_date="2021-09-30"

                df.loc[len(df.index)] = [tweet_date, tweet_text]

            df.to_csv(f'{ticker}_tweets.csv', index=False)
        except Exception:
            print("\nError while fetching.\nRetrying...\n\n")
            continue
"""

def get_tweets_df(ticker: str="tsla",n: int=40):
    """
    gets the tweets for a ticker
    """
    driver=init_driver()
    # login to twitter
    URL="https://twitter.com/i/flow/login"
    driver.get(URL)
    driver.implicitly_wait(60)

    input("Press enter once login is done... ")

    original_window=driver.current_window_handle

    # Accept cookies to make the banner disappear
    try:
        accept_cookies_btn = driver.find_element(
        "xpath", "//span[text()='Refuse non-essential cookies']/../../..")
        accept_cookies_btn.click()
    except NoSuchElementException:
        pass

    ticker = ticker.upper()
    driver.get(f"https://twitter.com/search?q=%24{ticker}")
    driver.implicitly_wait(10)

    df = pd.DataFrame({'date':[], 'tweet':[]})

    for _ in range(5):  # Retry loop
        try:
            time.sleep(1)
            for i in range(n):
                tweet_text_xpath=f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[{i+10}]/div/div/article/div/div/div[2]/div[2]/div[2]/div"
                tweet_element = driver.find_element(by=By.XPATH, value=tweet_text_xpath)
                tweet_text = tweet_element.text

                tweet_date="2021-09-30"

                df.loc[len(df.index)] = [tweet_date, tweet_text]

            # df.to_csv(f'{ticker}_tweets.csv', index=False)
            return df
        except Exception:
            print("\nError while fetching.\nRetrying...\n\n")
            continue


if __name__ == "__main__":
    df=get_tweets_df("TSLA")
    input("Press enter to quit... ")
