import time
from selenium import webdriver

def init_selenium(driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox') #以最高權限運行
    # chrome_options.add_argument('--headless') #hide the window 
    chrome_options.add_argument('--disable-dev-shm-usage')#以防crash
    prefs = {"profile.default_content_setting_values.notifications" : 2}    
    chrome_options.add_experimental_option("prefs",prefs) # turn of notification window\
    driver = webdriver.Chrome(driver_path,chrome_options=chrome_options)
    return driver   

def login_version1(driver):
    '''
    sometimes fail,need robot verification
    url can be anyone in https://seekingalpha.com/
    '''
    driver.get('https://seekingalpha.com/earnings/earnings-call-transcripts')
    time.sleep(0.2)
    driver.find_element_by_id('sign-in').click()
    time.sleep(0.2)
    driver.find_element_by_id('authentication_login_email').send_keys('YOUR_EMAIL')
    driver.find_element_by_id('authentication_login_password').send_keys('YOUR_PASSWORD')
    driver.find_element_by_id('log-btn').click()
    return driver

def login_version2(driver):
    '''
    my portfolio login page
    '''
    driver.get('https://seekingalpha.com/account/login?rt=%2Faccount%2Fportfolio')
    driver.find_element_by_id('login_user_email').send_keys('YOUR_EMAIL')
    driver.find_element_by_id('login_user_password').send_keys('YOUR_PASSWORD')
    time.sleep(7)
    driver.find_element_by_xpath('/html/body/div[2]/div/div[6]/form/div[5]/input').click()
    return driver

def login_v3(driver):
    driver.get('https://seekingalpha.com/account/login  ')
    driver.find_element_by_name('email').send_keys('YOUR_EMAIL')
    driver.find_element_by_name('password').send_keys('YOUR_PASSWORD')
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/main/div[2]/form/button').click()
    time.sleep(2)
    return driver