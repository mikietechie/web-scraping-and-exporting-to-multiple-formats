import requests, bs4, sys
import xml.etree.ElementTree as ET

try:
    out_put_file_path = sys.argv[1]
except IndexError:
    out_put_file_path = ''

class App(object):
    def __init__(self, title, desc, image, stars, os, downloads):
        self.title = title
        self.desc = desc
        self.image = image
        self.stars = stars
        self.os = os
        self.downloads = downloads
    
    def __str__(self):
        return f"{self.title}"
    
    def __dict__(self):
        return dict(title = self.title, desc = 'self.desc', image = 'self.image', stars = self.stars, os = self.os, downloads = self.downloads)
        

def scrap():
    url = "https://www.downloadtome.com/"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    apps = []
    apps_elements_container = soup.find("div", class_="-mt-35")
    app_elements = apps_elements_container.find_all("div", class_="bg-blue-100")
    for app_element in app_elements:
        os_p = app_element.find("p")
        img_img = app_element.find("img", class_="object-contain")
        title_p = app_element.find("p", class_="text-gray-800")
        desc_p = app_element.find("p", class_="text-gray-600")
        stars_svgs = app_element.find_all("svg", class_="text-yellow-500")
        downloads_p = app_element.find("div", class_="text-gray-700").find("p")
        apps.append(App(
            title = title_p.text,
            desc = desc_p.text,
            image = img_img["src"],
            stars = len(stars_svgs),
            os = os_p.text,
            downloads = eval(downloads_p.text)
        ))
    return apps


def to_xml():
    import xml.etree.ElementTree as ET
    apps = ET.Element("apps")
    for app in scrap():
        item = ET.SubElement(apps, "app")
        item.set("title", app.title)
        item.set("desc", app.desc)
        item.set("image", app.title)
        item.set("stars", str(app.stars))
        item.set("os", app.os)
        item.set("downloads", str(app.downloads))
    str_data = ET.tostring(apps)
    with open(out_put_file_path, "wb") as file:
        file.write(str_data)

def to_csv():
    import csv
    with open(out_put_file_path, "w") as file:
        csv_writer = csv.DictWriter(file, ['title', 'desc', 'image', 'stars', 'os', 'downloads'])
        csv_writer.writeheader()
        for app in scrap():
            try:
                csv_writer.writerow(dict(app))
            except: # encoding error
                exit()
                pass
def to_json():
    import json
    with open(out_put_file_path, "w") as file:
        json.dump(
            file,
            {
                'apps': [app.__dict__() for app in scrap()]
            }
        )
    

if __name__ == '__main__':
    if out_put_file_path.endswith('csv'):
        to_csv()
    elif out_put_file_path.endswith("json"):
        to_json()
    elif out_put_file_path.endswith("xml"):
        to_xml()
    else:
        for app in scrap():
            print(app)
    print(f"Done please check:\t{out_put_file_path}")
    
        