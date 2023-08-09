from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import asyncio
from files import del_video


# Uploading videos
async def upload_video(driver, video):
    print('#' * 5 + "  Uploading...  " + '#' * 5)
    wait = WebDriverWait(driver, 20)
    element = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".e18d3d942.tiktok-2gvzau-ALink-StyledLink.er1vbsz1")))

    ref = element.get_attribute("href")
    driver.get(ref)
    await asyncio.sleep(5)

    frame = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(frame)
    await asyncio.sleep(5)

    try:
        file = driver.find_element(By.XPATH, "//input[@type='file']")
        file.send_keys(video)
        await asyncio.sleep(5)
    except Exception:
        return

    driver.switch_to.window(driver.window_handles[0])
    await asyncio.sleep(5)

    frame = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(frame)
    await asyncio.sleep(5)

    span = driver.find_element(By.CSS_SELECTOR, "span[data-text='true']")
    span.clear()
    span.send_keys("Ссылка в шапке профиля ")
    await asyncio.sleep(5)

    driver.find_element(By.CLASS_NAME, "css-y1m958").click()
    await asyncio.sleep(5)

    # Delete video from dir
    del_video(video)
