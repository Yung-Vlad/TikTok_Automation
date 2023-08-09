from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

import pickle
from config import accounts
from fake_useragent import UserAgent
import asyncio
import os
import zipfile


# Authentication in accounts
async def authentication(use_proxy=False, index=None):
    print('#' * 5 + "  Authentication...  " + '#' * 5)
    options = webdriver.ChromeOptions()

    # Use proxy to upload
    if use_proxy:
        manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                "scripts": ["background.js"]
                },
                "minimum_chrome_version": "76.0.0"
            }
            """

        background_js = """
            let config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                }
            };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
            chrome.webRequest.onAuthRequired.addListener(
                function(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                },
                {urls: ["<all_urls>"]},
                ["blocking"]
            );
            """ % (accounts[index]["proxy_data"][0], accounts[index]["proxy_data"][1], accounts[index]["proxy_data"][2],
                   accounts[index]["proxy_data"][3])

        plugin_file = f"proxies/proxy_auth_plugin{index}.zip"

        if not os.path.exists(plugin_file):
            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)

        options.add_extension(plugin_file)

    user_agent = UserAgent()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={user_agent.random}")
    driver = webdriver.Chrome(options=options)

    url = "https://www.tiktok.com/"
    driver.set_window_size(1920, 1080)
    driver.set_window_position(0, 0)

    driver.get(url)
    await asyncio.sleep(2)

    # If exists file cookies
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f"cookies/cookie{index}")):
        login_button = WebDriverWait(driver, 10) \
            .until(ec.element_to_be_clickable((By.XPATH, "//button[@data-e2e='top-login-button']")))
        login_button.click()
        await asyncio.sleep(2)

        google_login_button = WebDriverWait(driver, 10) \
            .until(
            ec.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div/div/div[1]")))
        google_login_button.click()
        await asyncio.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        await asyncio.sleep(2)

        email_field = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, "identifier")))
        email_field.send_keys(accounts[index]["email"])
        await asyncio.sleep(2)

        next_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Далее')]"))
        )
        next_button.click()
        await asyncio.sleep(2)

        pass_field = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, "Passwd")))
        pass_field.send_keys(accounts[index]["password"])
        await asyncio.sleep(2)

        next_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Далее')]"))
        )
        next_button.click()
        await asyncio.sleep(30)

        driver.switch_to.window(driver.window_handles[0])
        await asyncio.sleep(2)

        pickle.dump(driver.get_cookies(), open(f"cookies/cookie{index}", "wb"))
        await asyncio.sleep(3)

    # Using cookies
    else:
        for cookie in pickle.load(open(f"cookies/cookie{index}", "rb")):
            driver.add_cookie(cookie)

        await asyncio.sleep(3)
        driver.refresh()
        await asyncio.sleep(3)

    return driver
