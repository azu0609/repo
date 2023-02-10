import requests
import json

class Fetch:
    def __init__(self):
        
        self.Tweaked = ["https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/qnblackcat/uYouPlus/releases"]
        self.Sideloaded = ["https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases"]
        self.Macdirtycow = ["https://api.github.com/repos/leminlimez/Cowabunga/releases"]

    def fetch(self, app, current_ver):
        index, app_type = self.app_handler(app)
        if index == 3:
            version = "v2.1"
            print("INFO: uYou detected! using 2.1 instend of latest.")
        else:
            if app_type == "Macdirtycow":
                version = requests.get(self.Macdirtycow[index]).json()[0]["name"]
            elif app_type == "Sideloaded":
                version = requests.get(self.Sideloaded[index]).json()[0]["name"]
            elif app_type == "Tweaked":
                version = requests.get(self.Tweaked[index]).json()[0]["name"]
        version = version.strip("v")
        print(f"INFO: app: {app}(index: {index}), current: {current_ver}, new: {version}")
        if version > current_ver:
            print(f"{current_ver} >>> {version}")
            print(f"INFO: New version found. updating to: {version}, current: {current_ver}")
            self.rw("/home/azuki/Documents/repo/scarlet_repo.json", version, index, app_type, current_ver)
        else:
            print("Up to date")

    
    def rw(self, path, version, index, app_type, current_ver):
        with open(path, 'r') as file:
            json_data = json.load(file)
            json_data[app_type][index]["version"] = version
            json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver, version)
            print(f"INFO: Writed to: {path} successfully")
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
        return
        
    
    def app_handler(self, app):
        print(f"INFO: recived {app}")
        if app == "Enmity":
            return 0, "Tweaked"
        if app == "Enmity (Dev)":
            return 1, "Tweaked"
        if app == "uYou":
            return 3, "Tweaked"
        if app == "uYou+":
            return 2, "Tweaked"
        if app == "Anime Now!":
            return 0, "Sideloaded"
        if app == "Cowabunga":
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
                    except TypeError as e:
                        print(f"WARNING: {e}, this seems caused by metadata.")


if __name__ == "__main__":
    Fetch().automate()
    # Fetch().fetch("Cowabunga", "7.0.3")