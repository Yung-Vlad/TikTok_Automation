from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import asyncio
from database import insert_data, existence_check, VIDEOS_TABLE
from files import create_dir, rename_file
from help_funcs import change_likes


# Downloading videos
async def download_video(name, url):
    print('#' * 5 + "  Downloading...  " + '#' * 5)

    # Creating dir for hashtag
    path = create_dir(name)
    chrome_options = Options()

    # Setting boot options
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get("https://ssstik.io/ru")
        await asyncio.sleep(1)

        input_field = driver.find_element(By.ID, "main_page_text")
        input_field.send_keys(url)
        await asyncio.sleep(3)

        driver.find_element(By.CLASS_NAME, "pure-button-primary").click()
        await asyncio.sleep(3)

        try:
            download_link = driver.find_element(By.XPATH, "/html/body/main/section[1]"
                                                          "/div/div/div[3]/div/div/div[2]/a[1]")
            ref = download_link.get_attribute("href")
            driver.get(ref)
            await asyncio.sleep(20)
            return True
        except Exception:
            return False


# Parsing required data
async def parsing_data(tag, driver):
    input_field = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/form/input")
    input_field.send_keys(tag)
    await asyncio.sleep(1)

    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/form/button").click()
    await asyncio.sleep(2)

    # Scrolling page for search 500 or max videos
    last_height = 0
    for i in range(42):
        page_height = driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight,"
            " document.documentElement.clientHeight, document.documentElement.scrollHeight,"
            " document.documentElement.offsetHeight );")

        if page_height == last_height:
            break

        driver.execute_script(f"window.scrollTo(0, {page_height});")
        last_height = page_height
        await asyncio.sleep(2)

    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")

    videos = soup.find_all("div", class_="tiktok-c83ctf-DivWrapper e1cg0wnj1")
    video_urls = []
    for video in videos:
        video_urls.append(video.next_element["href"])

    # Parsing data
    for url in video_urls:
        print('#' * 5 + "  Parsing  " + '#' * 5)
        if existence_check(url):
            print("Already exists...")
            continue

        response = requests.get(url)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        hashes = []

        try:
            hashtags = soup.find_all('a', attrs={"data-e2e": "search-common-link"})

            for hashtag in hashtags:
                hashes.append(hashtag.text)
        except Exception:
            try:
                hashtags = soup.find_all("strong", class_="tiktok-1p6dp51-StrongText ejg0rhn2")

                for hashtag in hashtags:
                    hashes.append(hashtag.text)

            except Exception:
                hashes = None

        try:
            date_of_publish = soup.find("span", class_="tiktok-hswmbs-SpanOtherInfos evv7pft3") \
                .find_all("span")[-1].text
        except Exception:
            date_of_publish = None

        try:
            song = soup.find("div", class_="tiktok-pvx3oa-DivMusicText epjbyn3").text
        except Exception:
            song = None

        try:
            count_of_likes = change_likes(soup.find("strong", attrs={"data-e2e": "like-count"}).text)
        except Exception:
            count_of_likes = None

        if not count_of_likes and not song and not date_of_publish:
            continue

        if not await download_video(tag, url):
            continue

        hashes = ''.join(hashes)

        try:
            file_name = rename_file(tag, hashes)
        except Exception:
            continue

        insert_data(VIDEOS_TABLE, url, file_name, hashes, count_of_likes, date_of_publish, song)

    driver.close()
    driver.quit()
