"""
This script scraps news headlines for given ticker.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_driver()->WebElement:
    """
    Initialize the browser driver
    """
    # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
    options = webdriver.ChromeOptions()
    options .add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("--headless=new")


    driver: WebElement = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

"""
def get_nasdaq_headlines(ticker: str="tsla"):
    driver=init_driver()
    ticker = ticker.lower()
    driver.get(f"https://www.nasdaq.com/market-activity/stocks/{ticker}/news-headlines")
    driver.implicitly_wait(10)
    original_window=driver.current_window_handle

    df = pd.DataFrame({'headlines':[], 'datetime':[], 'link':[]})

    pages = 10
    c = 0

    for _ in range(5):  # Retry loop
        try:
            time.sleep(1)
            for _ in range(pages):
                for i in range(1, 8):  # 1 to 7
                    xpath = f'/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li[{i}]/a/p'
                    headline_element = driver.find_element(by=By.XPATH, value=xpath)
                    headline_text = headline_element.text

                    article_link_xpath = f"/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li[{i}]/a"
                    article_element = driver.find_element(by=By.XPATH, value=article_link_xpath)
                    href_value = article_element.get_attribute("href")

                    try:
                        driver.switch_to.new_window('tab')
                        driver.get(href_value)
                        driver.implicitly_wait(1)
                        datetime_xpath = "/html/body/div[2]/div/main/div[2]/article/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/p[1]"
                        datetime_element = driver.find_element(by=By.XPATH, value=datetime_xpath)
                    except Exception:
                        print("link does not exist")
                        driver.close()
                        driver.switch_to.window(original_window)
                        continue

                    datetime_text = datetime_element.text

                    print(f"headline {c+i}: {headline_text}", end=" ")
                    print(f"datetime: {datetime_text}")

                    # Go back to the previous page
                    driver.close()

                    driver.switch_to.window(original_window)

                    # Add to dataframe
                    df.loc[len(df.index)] = [headline_text, datetime_text, href_value]

                # Go to next set of headlines
                next_button = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]")
                next_button.click()

                time.sleep(2)

                c += 7
                print()
                print("Next page")
                print()

            # Save the df to csv file
            df.to_csv(f'{ticker}_headlines.csv', index=False)
            print("Headlines fetched successfully.")
            return True

        except Exception:
            print("\nError while fetching.\nRetrying...\n\n")
            continue
"""

def get_nasdaq_headlines_df(ticker: str="tsla")->pd.DataFrame:
    """
    gets the headlines from nasdaq
    """
    try:
        driver=init_driver()
        ticker = ticker.lower()
        driver.get(f"https://www.nasdaq.com/market-activity/stocks/{ticker}/news-headlines")
    except Exception:
        print("ERROR: INTERNET DISCONNECTED")
        exit()
    driver.implicitly_wait(10)
    original_window=driver.current_window_handle

    df = pd.DataFrame({'headlines':[], 'datetime':[], 'link':[]})

    pages = 10
    c = 0

    for _ in range(5):  # Retry loop
        try:
            time.sleep(1)
            for _ in range(pages):
                for i in range(1, 8):  # 1 to 7
                    xpath = f'/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li[{i}]/a/p'
                    headline_element = driver.find_element(by=By.XPATH, value=xpath)
                    headline_text = headline_element.text

                    article_link_xpath = f"/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li[{i}]/a"
                    article_element = driver.find_element(by=By.XPATH, value=article_link_xpath)
                    href_value = article_element.get_attribute("href")

                    try:
                        driver.switch_to.new_window('tab')
                        driver.get(href_value)
                        driver.implicitly_wait(1)
                        datetime_xpath = "/html/body/div[2]/div/main/div[2]/article/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/p[1]"
                        datetime_element = driver.find_element(by=By.XPATH, value=datetime_xpath)
                    except Exception:
                        print("link does not exist")
                        driver.close()
                        driver.switch_to.window(original_window)
                        continue

                    datetime_text = datetime_element.text

                    print(f"headline {c+i}: {headline_text}", end=" ")
                    print(f"datetime: {datetime_text}")

                    # Go back to the previous page
                    driver.close()

                    driver.switch_to.window(original_window)

                    # Add to dataframe
                    df.loc[len(df.index)] = [headline_text, datetime_text, href_value]

                # Go to next set of headlines
                next_button = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]")
                next_button.click()

                time.sleep(2)

                c += 7
                print()
                print("Next page")
                print()

            # Save the df to csv file
            # df.to_csv(f'{ticker}_headlines.csv', index=False)
            print("Headlines fetched successfully.")
            return df

        except Exception as e:
            print(e)
            print("\nError while fetching.\nRetrying...\n\n")
            continue
        
if __name__ == "__main__":
    # get_nasdaq_headlines("TSLA")
    df=get_nasdaq_headlines_df("TSLA")
    print(df.head(2))
    input("Press enter to quit... ")
