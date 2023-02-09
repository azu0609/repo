import requests
import json

class Fetch:
    def __init__(self):
        self.src = ["https://api.github.com/repos/enmity-mod/tweak/releases/latest"]
        self.current_ver = ["2.1.3"]

    def fetch(self, app):
        index, type = self.app_selector(app)
        version = requests.get(self.src[index]).json()["name"]
        version = version.strip("v")
        if version > self.current_ver[index]:
            print(f"{self.current_ver} >>> {version}")
            print(f"INFO: app={app}(index={index}), current={self.current_ver}, new={version}")
            print("New version found! - Updating...")
            self.rw("/home/azuki/Documents/repo/scarlet_repo.json", version, index, type)
        else:
            print("Up to date")

    
    def rw(self, path, version, index, type):
        with open(path, 'r') as file:
            json_data = json.load(file)
            json_data[type][index]["version"] = version
            print("ci:" + json_data[type][index]["version"])
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
        
        print(f"current ver: {self.current_ver}, new ver: {version}, index: {index}")
    
    def app_selector(self, app):
        if app == "enmity":
            return 0, "Tweaked"
        elif app == "enmity_dev":
            return 1, "Tweaked"
        elif app == "uyou":
            return 2, "Tweaked"
        elif app == "uyouplus":
            return 3, "Tweaked"
        elif app == "anime_now":
            return 4, "Sideloaded"
        else:
            print("unexpected value.")
            return
        

if __name__ == "__main__":
    Fetch().fetch("enmity")