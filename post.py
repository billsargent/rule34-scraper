import requests
from bs4 import BeautifulSoup
import sqlite3
import zlib
import urllib3
import os

urllib3.disable_warnings()


def get_page(url):
    # Send a GET request to the URL and store the response in a variable
    response = requests.get(url, verify=False)

    # Parse the response using Beautiful Soup and store it in a variable
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section with the ID "Imagemain"
    section_imagemain = soup.find('section', id='Imagemain')

    # Find the URL inside the class "shm-main-image" in section "Imagemain"
    try:
        image_url = section_imagemain.find('img', class_='shm-main-image')['src']
        #return image_url
        pass
    except:
        print("An error occurred while trying to get the image URL.")
        return
    filename =  filename = os.path.basename(image_url)

    # Clean up the filename
    filename = os.path.splitext(filename)[0]
    filename, extension = os.path.splitext(filename)
    filename = filename.replace('%20', '_')
    filename = filename.replace(' ', '_')


    # Find the section with the ID "ImageInfo"
    section_imageinfo = soup.find('section', id='ImageInfo')

    # Find the link text inside the class "username" in section "ImageInfo"
    username = section_imageinfo.find('a', class_='username').text

    # Find the time element inside the class "username" in section "ImageInfo"
    time_elem = section_imageinfo.find('a', class_='username').find_next_sibling('time')

    # Get the value of the datetime attribute
    datetime_val = time_elem['datetime']

    tag_input = section_imageinfo.find('input', attrs={'name': 'tag_edit__tags'})

    # Get the value of the text input box
    tag_value = tag_input['value']

    # Find the next URL within the "ImageInfo" section that starts with "http"
    next_url = section_imageinfo.find('a', href=lambda href: href and href.startswith('http'))
    
        # Get the href value of the next URL, if it exists
    if next_url:
        next_url_value = next_url['href']
    else:
        next_url_value = None

    # Open a connection to the SQLite database
    conn = sqlite3.connect('images.db')

    # Create a table for the images if it doesn't exist already
    conn.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 url TEXT NOT NULL,
                 image BLOB NOT NULL,
                 crc INTEGER NOT NULL,
                 uploader TEXT NOT NULL,
                 dateuploaded TEXT NOT NULL,
                 tags TEXT NOT NULL,
                 filename TEXT NOT NULL,
                 origin TEXT)''')

    # Check if the image data already exists in the database based on the CRC value
    cursor = conn.execute('SELECT id FROM images WHERE url = ?', (url,))
    row = cursor.fetchone()

    if row is not None:
        print('Image already exists in database with ID:', row[0])
    else:
        # Fetch the image data
        image_data = requests.get(image_url, verify=False).content

        # Compute the CRC value of the image data
        crc_value = zlib.crc32(image_data)
        # Insert the image data into the database
        conn.execute('INSERT INTO images (url, image, crc, uploader, dateuploaded, tags, filename, origin) VALUES (?, ?, ?, ?, ?, ?, ?,?)',
                     (url, image_data, crc_value, username, datetime_val, tag_value, filename, next_url_value))
        print('Image inserted into database\n')
        print("   ")
        print("Image URL: ", image_url)
        print("Uploader: ", username)
        print("Date uploaded: ", datetime_val)
        print("Tags: ", tag_value)
        print("Origin: ", next_url_value)
        print("CRC: ", crc_value)
        print("Filename: ", filename)

    # Commit the
    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()



for i in range(1, 5660876):
    l = open('complete-urls.txt', 'a')
    # Loop through the URLs and write each one to the file

    url = f"http://rule34.paheal.net//post/view/{i}"
    print(url)
    get_page(url)
    l.write(url + '\n')

    l.close()
