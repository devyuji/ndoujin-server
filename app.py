from bs4 import BeautifulSoup
import requests as rq
import base64
import io

def image_to_base64(image):
    image = rq.get(image)
    image_byte = io.BytesIO(image.content)
    img_base64 = str(base64.b64encode(image_byte.read()))
    img_base = img_base64.split('\'')[1]
    return img_base

def nhentai(id):
    URL = f'https://nhentai.net/g/{id}'
    html = rq.get(URL)

    if html.status_code != 200:
        print('something went wrong')
        return {"error": True}

    html_parser = BeautifulSoup(html.text, 'html.parser')

    try:
        # images
        image_container = html_parser.find(id='cover')
        image_cover = image_container.find('img').get('data-src')
        image_cover = image_to_base64(image_cover)

        # title
        title = html_parser.find(class_='title').get_text()
        
        # tags 
        tags_main_container = html_parser.find(id='tags')
        tag_container = tags_main_container.find_all('div')

        tags = []

        for tag in tag_container:
            tag_name = tag.get_text().strip().split("\n")[0]
            if tag_name == 'Tags:':
                a = tag.find_all(class_='name')
                for name in a:
                    tags.append(name.get_text())
            
            elif tag_name == 'Pages:':
                page = tag.find(class_='name').get_text() if tag.find(class_='name') else 'N/A'
            
            elif tag_name == 'Languages:':
                lang = tag.find_all(class_='name')[-1].get_text() if tag.find_all(class_='name') else 'N/A'

            elif tag_name == 'Artists:':
                artist = tag.find(class_='name').get_text() if tag.find(class_='name') else 'N/A'

        send = {"error": False, "image_cover" : image_cover, "title" : title, "tags": tags, 'page': page, "language": lang, "artist" : artist, "id" : id} 
        return send
    
    except Exception as err:
        print(err)
        return {"error" : True}

if __name__ == '__main__':
    id = 365317
    nhentai(id)
