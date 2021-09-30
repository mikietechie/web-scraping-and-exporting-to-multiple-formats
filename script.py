import requests, bs4
import xml.etree.ElementTree as ET


class App(object):
    def __init__(self, title, desc, image, stars, os, downloads):
        self.title = title
        self.desc = desc
        self.image = image
        self.stars = stars
        self.os = os
        self.downloads = downloads
    
    def __str__(self):
        return f"{self.image}"
        

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
    with open("apps.xml", "wb") as file:
        file.write(str_data)


if __name__ == '__main__':
    to_xml()
    print("done")
    
        