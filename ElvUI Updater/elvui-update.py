import urllib.request
import wget
from zipfile import ZipFile
import shutil
import os
import sys
import json
from html.parser import HTMLParser

def getCache():
    try:
        with open('elvui-update-cache.txt') as f:
            data = json.load(f)
            location = data['location']
            version = data['version']
    except IOError:
        while True:
            print("No cache found, input wow folder location: ")
            x = input()
            x = x + "\_retail_\Interface\AddOns"
            if os.path.exists(x):
                location = x
                version = None
                break
            else:
                print("WoW folder not found")
    
    return location,version


def getVersionInfo():
    try:
        fp = urllib.request.urlopen("https://www.tukui.org/download.php?ui=elvui&changelog")
        ecb = fp.read()

        ecs = ecb.decode("utf8")
        fp.close()

    except:
        print ("Failed opening webpage to retrieve version info")
        sys.exit(1)
    
    return ecs

def getFileAndUpdateElvUI(loc):
    try:
        print ("Attempting to download file at: %s" % url)
        wget.download(url, "elvui.zip")
        print ("\nSuccessfully downloaded version %s" % version) 
    except:
        print ("Failed downloading file.")
        sys.exit(1)

    print("Deleting old version")
    try: 
        shutil.rmtree(loc + "\ElvUI")
        shutil.rmtree(loc + "\ElvUI_OptionsUI")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    try:
        with ZipFile("elvui.zip", "r") as zipObj:
            zipObj.extractall(loc)
    except:
        print("Failed to unzip file.")

    try:
        os.remove("elvui.zip")
        print("Successfully updated and deleted old files.")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
        sys.exit(1)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    

if __name__ == "__main__":
    cacheLocation,cacheVersion = getCache()

    splits = getVersionInfo().split("<u><b>Version ",2)
    secondsplit = splits[1].split(None,2)
    version = secondsplit[0].strip()

    print ("Successfully found version number")

    url = "https://www.tukui.org/downloads/elvui-"
    url = url + version + ".zip"

    if cacheVersion == None or float(version) > float(cacheVersion):
        getFileAndUpdateElvUI(cacheLocation)
        print("Changelog:\nVersion: ", strip_tags(splits[1]).strip())
        updated = True
    else:
        print("Already have latest version of ElvUI\nVersion: %s" % cacheVersion)
        updated = False
    
    if updated:
        with open('elvui-update-cache.txt', 'w') as f:
            data = {
                'version': version,
                'location': cacheLocation
            }
            json.dump(data, f)

    input("Press any key to continue.")