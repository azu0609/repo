import requests
import json
import sys

class Fetch:
    def __init__(self):
        
        self.Tweaked = ["https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/qnblackcat/uYouPlus/releases"]
        self.Sideloaded = ["https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases"]
        self.Macdirtycow = ["https://api.github.com/repos/leminlimez/Cowabunga/releases",
                            "https://api.github.com/repos/haxi0/KillMyOTA/releases"]


    def logger(self, type, message):
        if type == "info":
            print("INFO: " + message)
        elif type == "warn":
            print("WARN: " + message)
        elif type == "error":
            print("ERROR: " + message)
        else:
            print(message)
    

    def fetch(self, app, current_ver):
        index, app_type = self.app_handler(app)
        if index == 3:
            version = "v2.1"
            self.logger("info", "uYou detected! using 2.1 instend of latest.")
        else:
            version = None
            try:
                if app_type == "Macdirtycow":
                    version = requests.get(self.Macdirtycow[index]).json()[0]["name"]
                elif app_type == "Sideloaded":
                    version = requests.get(self.Sideloaded[index]).json()[0]["name"]
                elif app_type == "Tweaked":
                    version = requests.get(self.Tweaked[index]).json()[0]["name"]
            except KeyError:
                self.logger("error", "Rate limited by github. can't use github api for a while.\nERROR: try again later.")
                raise(KeyError)
        version = version.strip("v")
        self.logger("info", f"app: {app}(index: {index}), current: {current_ver}, new: {version}")
        if version > current_ver:
            self.logger("info", f"New version available: {version}, updating...")
            self.rw("../scarlet_repo.json", version, index, app_type, current_ver)
        else:
            self.logger("info", "Up to date.")

    
    def rw(self, path, version, index, app_type, current_ver):
            with open(path, "r") as file:
                self.logger("info", "Loading data...")
                json_data = json.load(file)
                self.logger("info", "Modifying loaded data...")
                json_data[app_type][index]["version"] = version
                json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver, version)
                if index == 2:
                    json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver.replace("-", "_"), version.replace("-", "_"))
            with open(path, 'w') as file:
                json.dump(json_data, file, indent=2)
                self.logger("info", f"Writed to: {path} successfully.")

            """
            # Modify readme
            with open("../README.md", "r") as file:
                self.logger("info", "Loading readme.md data...")
                file_data = file.readlines()
                for line in file_data:
                    print(line)
                    if [app_type][index]["name"] in line and current_ver in line:
                        print(line)
                data = file.read()
            with open("../README.md", "w") as file:
                self.logger("info", "Writing modified data...")
                file.write(data.replace(current_ver, version))
            """
            
        
    
    def app_handler(self, app):
        self.logger("info", f"Recived: {app}")
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
        if app == "KillMyOTA":
            return 1, "Macdirtycow"
        else:
            self.logger("error", f"Unexpected value: {app}")
            raise
    

    def automate(self):
        with open("../scarlet_repo.json", 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                for key in json_data[item]:
                    try:
                        self.fetch(key["name"], key["version"])
                    except TypeError as e:
                        self.logger("warn", f"{e}, this seems caused by metadata.")
        self.logger("info", f"All done! may take 1~2m(Page build time) to apply.")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--production":
            Fetch().automate()
        if sys.argv[1] == "--test":
            try:
                Fetch().fetch(sys.argv[3], sys.argv[2])
            except IndexError:
                print("ERROR: Needed argument not found. example: 2.1.4 Enmity")
    except IndexError:
        print("ERROR: Needed argument not found. example: --production")