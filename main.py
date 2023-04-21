import requests
from tqdm import tqdm
import json
import os
import math


def scrap_pexels(query=''):
    headers = {"Authorization": f'{os.getenv"API_KEY"}}
    query_str = f'https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=landscape'

    # use this, if you have some access problems
    #proxies = {
    #   'https': f'your_proxy'
    #}

    response = requests.get(url=query_str, headers=headers) #proxies=proxies if proxy

    if response.status_code != 200:
        return f'Error: Status Code - {response.status_code}, {response.json()}'

    img_dir_path = '_'.join(i for i in query.split(' ') if i.isalnum()) #making directory name
    
    if not os.path.exists(img_dir_path):  
        os.makedirs(img_dir_path) #making directory

    json_data = response.json()

    images_count = json_data.get('total_results')

    if not json_data.get('next_page'):
        img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
        download_images(img_list=img_urls, img_dir_path=img_dir_path)
    else:
        print(f'[INFO] Total images: {images_count}. Saving may take some time.')
  
        #loop for processing pages and tags
        images_list_urls = []
        for page in range(1, math.ceil(images_count/80)+1):
            query_str = f'{query_str}&page={page}'
            response = requests.get(url=query_str, headers=headers, proxies=proxies)
            json_data = response.json()
            img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
            images_list_urls.extend(img_urls)
        download_images(img_list=images_list_urls, img_dir_path=img_dir_path)


#function for img download
def download_images(img_list=[], img_dir_path=''):
    for item_url in tqdm(img_list):
        response = requests.get(url=item_url)

        if response.status_code == 200:
            with open(f'./{img_dir_path}/{item_url.split("-")[-1]}', 'wb') as file:
                file.write(response.content)
        else:
            print('Something went wrong while downloading the image!')


def main():
    query = input('Enter a keyword to search: ')
    scrap_pexels(query=query)



if __name__ == '__main__':
    main()
