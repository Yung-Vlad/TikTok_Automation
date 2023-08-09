import asyncio
import os
import time
import platform

from database import connect_db, sorted_by_likes
from files import read_file, check_count_videos
from download import parsing_data
from upload import upload_video
from help_funcs import del_hash
from auth import authentication


async def process_download(tags, indexes):
    tasks = []
    for tag, acc in zip(tags, indexes):
        driver = await authentication(index=acc)
        tasks.append(asyncio.create_task(parsing_data(tag=tag, driver=driver)))

    await asyncio.gather(*tasks)


async def process_upload(tags, indexes):
    while True:
        tasks = []
        try:
            for tag, acc in zip(tags, indexes):
                if not check_count_videos(tag):  # If videos with this tag ended
                    index = tags.index(tag)
                    tags.pop(index)
                    indexes.pop(index)
                    continue

                driver = await authentication(use_proxy=True, index=acc)
                if platform.system() == "Windows":
                    tasks.append(asyncio.create_task(upload_video(driver, os.path.join(os.path.dirname(__file__),
                                                                    f"videos\\{del_hash(tag)}\\{sorted_by_likes(tag)}"))))
                else:
                    tasks.append(asyncio.create_task(upload_video(driver, os.path.join(os.path.dirname(__file__),
                                                                                       f"videos/{del_hash(tag)}/{sorted_by_likes(tag)}"))))

            await asyncio.gather(*tasks)
            time.sleep(3600)
        except Exception as ex:
            print(ex)


async def main():
    connect_db()  # Database connection
    tags, indexes = read_file()

    await process_download(tags, indexes)
    await process_upload(tags, indexes)


if __name__ == '__main__':
    asyncio.run(main())
