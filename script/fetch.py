import requests
import json

class Fetch:
    def __init__(self):
        self.release = ["https://api.github.com/repos/enmity-mod/tweak/releases/latest",
                    "https://api.github.com/repos/enmity-mod/tweak/releases/latest",
                    "https://api.github.com/repos/qnblackcat/uYouPlus/releases/latest",
                    "https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases/latest"]
        self.current_ver = ["2.1.3"]

    def fetch(self, app, current_ver):
        index, type = self.app_handler(app)
        if index == 2:
            version = "v2.1"
        else:
            version = requests.get(self.release[index]).json()["name"]
        version = version.strip("v")
        print(f"INFO: app={app}(index={index}), current={current_ver}, new={version}")
        if version > current_ver[index]:
            print(f"{current_ver} >>> {version}")
            print("New version found! - Updating...")
            self.rw("/home/azuki/Documents/repo/scarlet_repo.json", version, index, type)
        else:
            print("Up to date")

    
    def rw(self, path, version, index, type):
        with open(path, 'r') as file:
            json_data = json.load(file)
            json_data[type][index]["version"] = version
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
        
    
    def app_handler(self, app):
        if app == "Enmity":
            return 0, "Tweaked"
        if app == "Enmity (Dev)":
            return 1, "Tweaked"
        if app == "uYou":
            return 2, "Tweaked"
        if app == "uYou+":
            return 3, "Tweaked"
        if app == "Anime Now!":
            return 4, "Sideloaded"
        if app == "Cowabunga":
            return 5, "Macdirtycow"
        else:
            print(f"unexpected value! input: {app}")
            return
    

    def automate(self):
        with open("/home/azuki/Documents/repo/scarlet_repo.json", 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                for key in json_data[item]:
                    try:
                        print(key["name"])
                        self.fetch(key["name"], key["version"])
                    except:
                        pass

if __name__ == "__main__":
    Fetch().automate()
    # Fetch().fetch("enmity")