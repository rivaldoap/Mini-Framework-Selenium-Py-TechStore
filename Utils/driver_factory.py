from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def start_browser():
    options = Options()
    options.add_argument("--incognito")             # membuka chrome dalam mode incognito
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")  # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    return driver