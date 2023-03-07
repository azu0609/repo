import requests
import json
import sys

class Fetch:
    def __init__(self):
        self.release_source = ["https://api.github.com/repos/acquitelol/rosiecord/releases",
                               "https://api.github.com/repos/enmity-mod/tweak/releases",
                               "https://api.github.com/repos/qnblackcat/uYouPlus/releases",
                               "https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases",
                               "https://api.github.com/repos/leminlimez/Cowabunga/releases",
                               "https://api.github.com/repos/haxi0/KillMyOTA/releases"]
        self.Tweaked = ["https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/enmity-mod/tweak/releases",
                        "https://api.github.com/repos/qnblackcat/uYouPlus/releases"]
        self.Sideloaded = ["https://api.github.com/repos/AnimeNow-Team/AnimeNow/releases"]
        self.Macdirtycow = ["https://api.github.com/repos/leminlimez/Cowabunga/releases",
                            "https://api.github.com/repos/haxi0/KillMyOTA/releases"]


    def logger(self, type: int, message):
        if type == 0:
            print("INFO: " + message)
        elif type == 1:
            print("DEBUG: " + message)
        elif type == 2:
            print("WARN: " + message)
        elif type == 3:
            print("ERROR: " + message)
        else:
            print(message)
    

    def fetch(self, repo, index, app_type, current_ver, download_url):
        if index == 3:
            version = "v2.1"
            self.logger(2, "uYou detected! using 2.1 instend of latest.")
        else:
            version = None
            changelog = None
            released_date = None
            for i, releases in enumerate(self.release_source):
                if releases.replace("api.", "").replace("repos/", "") in download_url:
                    self.logger(0, "Found url.")
                    try:
                        version = requests.get(self.release_source[i]).json()[0]["name"]
                        changelog = requests.get(self.release_source[i]).json()[0]["body"]
                        released_date = requests.get(self.release_source[i]).json()[0]["assets"][0]["created_at"]
                    except KeyError:
                        raise("Rate limited")
            """
            if app_type == "Macdirtycow":
                version = requests.get(self.Macdirtycow[index]).json()[0]["name"]
                changelog = requests.get(self.Macdirtycow[index]).json()[0]["body"]
                released_date = requests.get(self.Macdirtycow[index]).json()[0]["assets"][0]["created_at"]
            elif app_type == "Sideloaded":
                version = requests.get(self.Sideloaded[index]).json()[0]["name"]
                changelog = requests.get(self.Sideloaded[index]).json()[0]["body"]
                released_date = requests.get(self.Sideloaded[index]).json()[0]["assets"][0]["created_at"]
            elif app_type == "Tweaked":
                version = requests.get(self.Tweaked[index]).json()[0]["name"]
                changelog = requests.get(self.Tweaked[index]).json()[0]["body"]
                released_date = requests.get(self.Tweaked[index]).json()[0]["assets"][0]["created_at"]
            """
        version = version.strip("v")
        # released_date = released_date.find("T")[:released_date] # Disabled due to error. available in soon
        self.logger(1, f"index: {index}, current: {current_ver}, new: {version}") # Disabled due to error
        if version > current_ver:
            self.logger(0, f"New version available: {version}, updating...")
            self.rw(repo, "../altstore_repo.json", "../scarlet_repo.json", version, index, app_type, current_ver, changelog, released_date)
        else:
            self.logger(0, "Up to date.")

    
    def rw(self, repo_type, altstore_path, scarlet_path, version, index, app_type, current_ver, version_description, release_date):
            if repo_type == "scarlet":
                with open(scarlet_path, "r") as scarlet_repo:
                    self.logger(0, "Loading data...")
                    json_data = json.load(scarlet_repo)
                    self.logger(0, "Modifying loaded data...")
                    json_data[app_type][index]["version"] = version
                    json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver, version)
                    if index == 2:
                        json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver.replace("-", "_"), version.replace("-", "_"))
                with open(scarlet_path, 'w') as scarlet_repo:
                    json.dump(json_data, scarlet_repo, indent=2)
                    self.logger(0, f"Writed to: {scarlet_path} successfully.")
            
            elif repo_type == "altstore":
                with open(altstore_path, "r") as altstore_repo:
                    self.logger(0, "Loading json manifest... this may take a while")
                    json_data = json.load(altstore_repo)
                    self.logger(0, "Modifying loaded data...")
                    print(type(index))
                    print(type(app_type))
                    print(type(version))
                    json_data[app_type][index]["version"] = version
                    json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver, version)
                    json_data[app_type][index]["versionDescription"] = version_description
                    json_data[app_type][index]["versionDate"] = release_date
                    if index == 2:
                        json_data[app_type][index]["down"] = json_data[app_type][index]["down"].replace(current_ver.replace("-", "_"), version.replace("-", "_"))
                with open(altstore_path, "w") as altstore_repo:
                    json.dump(json_data, altstore_repo, indent=2)
                    self.logger(0, f"Writed to: {altstore_path} successfully.")
            
            else:
                raise("Unexpected mode")
            """
            # Modify readme
            with open("../README.md", "r") as file:
                self.logger(0, "Loading readme.md data...")
                file_data = file.readlines()
                for line in file_data:
                    print(line)
                    if [app_type][index]["name"] in line and current_ver in line:
                        print(line)
                data = file.read()
            with open("../README.md", "w") as file:
                self.logger(0, "Writing modified data...")
                file.write(data.replace(current_ver, version))
            """
    

    def automate(self, path: str):
        with open(path, 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                for i, key in enumerate(json_data[item]):
                    try:
                        if path == "../altstore_repo.json":
                            self.fetch("altstore", i, item, key["version"], key["downloadURL"])
                        elif path == "../scarlet_repo.json":
                            self.fetch("scarlet", i, item, key["version"], key["down"])
                        else:
                            raise("Unexpected repo!")
                    except TypeError as e:
                        if str(e) == "string indices must be integers":
                            self.logger(2, f"{e}, this seems caused by metadata.")
                        else:
                            raise(e)
        self.logger(0, f"All done! may take 1~2m(Page build time) to apply.")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--production":
            Fetch().automate("../scarlet_repo.json")
        if sys.argv[1] == "--test":
            # try:
            Fetch().fetch("altstore", sys.argv[3], "apps", sys.argv[2], "https://github.com/enmity-mod/tweak/releases")
            # except IndexError:
                # print("ERROR: Needed argument not found. example: 2.1.4 Enmity")
    except IndexError:
        print("ERROR: Needed argument not found. example: --production")