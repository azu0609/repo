import requests
import json

class Fetch:
    def __init__(self):
        
        self.Tweaked = ["https://api.github.com/repos/enmity-mod/tweak/releases/latest",
                        "https://api.github.com/repos/enmity-mod/tweak/releases/latest",
                        "https://api.github.com/repos/qnblackcat/uYouPlus/releases/latest"]
        self.Sideloaded = ["https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases/latest"]
        self.Macdirtycow = ["https://api.github.com/repos/leminlimez/Cowabunga/releases/latest"]

    def fetch(self, app, current_ver):
        index, type = self.app_handler(app)
        print(f"got: {app}({index})")
        if index == 2:
            version = "v2.1"
            print("INFO: uYou detected.")
        else:
            if type == "Macdirtycow":
                version = requests.get(self.Macdirtycow[index]).json()["name"]
            elif type == "Sideloaded":
                version = requests.get(self.Sideloaded[index]).json()["name"]
            elif type == "Tweaked":
                version = requests.get(self.Tweaked[index]).json()["name"]
            print("INFO: Non-uYou detected.")
        version = version.strip("v")
        print(f"INFO: app: {app}(index: {index}), current: {current_ver}, new: {version}")
        if version > current_ver[index]:
            print(f"{current_ver} >>> {version}")
            print(f"New version found. updating to: {version}, current: {current_ver}")
            self.rw("/home/azuki/Documents/repo/scarlet_repo.json", version, index, type)
        else:
            print("Up to date")

    
    def rw(self, path, version, index, type):
        with open(path, 'r') as file:
            json_data = json.load(file)
            json_data[type][index]["version"] = version
            print(f"Writed to: {path} successfully")
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
        return
        
    
    def app_handler(self, app):
        if app == "Enmity":
            print("Enmity detected. passing...")
            return 0, "Tweaked"
        if app == "Enmity (Dev)":
            print("Enmity (Dev) detected. passing...")
            return 1, "Tweaked"
        if app == "uYou":
            print("uYou detected. passing...")
            return 2, "Tweaked"
        if app == "uYou+":
            print("uYou+ detected. passing...")
            return 3, "Tweaked"
        if app == "Anime Now!":
            print("Anime Now! detected. passing...")
            return 0, "Sideloaded"
        if app == "Cowabunga":
            print("Cowabugna detected. passing...")
            return 0, "Macdirtycow"
        else:
            print(f"unexpected value! input: {app}")
            return
    

    def automate(self):
        with open("/home/azuki/Documents/repo/scarlet_repo.json", 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                for key in json_data[item]:
                    try:
                        self.fetch(key["name"], key["version"])
                    except Exception as e:
                        print(e)


if __name__ == "__main__":
    Fetch().automate()
    # Fetch().fetch("Cowabunga", "7.0.3")