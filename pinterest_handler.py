import os
import io
import config
import requests
import imagehash
from time import sleep
from PIL import Image
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class PHandler():


    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable_encoding')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(path=config.CHROMEDRIVER_PATH).install()), options=chrome_options)


    def download_images(self, words: str, total: int) -> list:
        """
        This method is responsible for downloading the amount of results specified in the 'total' argument,
        that match the search string specified in the 'words' argument
        """
        print("Downloading images...")
        self.driver.get(f'https://www.pinterest.pt/search/pins/?q={words}')
        sleep(3)

        # Get the image links
        images_found = []
        if not os.path.exists(config.FOLDERPATH_IMAGES):
            os.mkdir(path=config.FOLDERPATH_IMAGES)
        while True:
            self._load_images_on_page(1)
            for request in self.driver.requests:
                if 'i.pinimg.com' in request.url:
                    new_image = requests.get(request.url).content
                    if self._is_image_duplicated(images_found,new_image):
                        continue
                    images_found.append(new_image)
                    with open(file=os.path.join(config.FOLDERPATH_IMAGES,f"{str(len(images_found))}.jpg"), mode='wb') as f:
                        f.write(new_image)
                if len(images_found) == total:
                    break
            if len(images_found) == total:
                break

    
    def _is_image_duplicated(self,list_of_images: list, new_image):
        """
        This method is responsible for checking if the new image obtained has already been downloaded
        """
        for image in list_of_images:
            image1 = Image.open(io.BytesIO(image))
            image2 = Image.open(io.BytesIO(new_image))
            hash1 = imagehash.phash(image1)
            hash2 = imagehash.phash(image2)
            similarity_threshold = 10
            hamming_distance = hash1 - hash2
            if hamming_distance <= similarity_threshold:
                return True
        return False


    def _load_images_on_page(self, loads: int):
        """
        This method is responsible for loading more images dynamically into the page
        """
        for i in range(0, loads):
            images = self.driver.find_elements(By.CSS_SELECTOR,'.Yl-.MIw.Hb7')
            self.driver.execute_script('arguments[0].scrollIntoView();', images[-1])
            sleep(3)