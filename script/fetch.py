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


    def logger(self, type: int, message: str):
        if type == 0:
            print('\033[92m' + "INFO: " + message)
        elif type == 1:
            print('\033[96m' + "DEBUG: " + message)
        elif type == 2:
            print('\033[93m' + "WARN: " + message)
        elif type == 3:
            print('\033[91m' + "ERROR: " + message)
        else:
            print(message)
    

    def fetch(self, repo, app_name, index, app_type, current_ver, download_url):
        version = None
        changelog = None
        released_date = None
        # FIXME: Handle uYou and rosiecord without any extra code
        if index == 3:
            version = "v2.1"
            released_date = "2021-10-28"
            changelog = "Unknown - Ask to developer"
            self.logger(2, "uYou detected! using 2.1 instead of latest.")
        else:
            for i, releases in enumerate(self.release_source):
                if releases.replace("api.", "").replace("repos/", "") in download_url:
                    try:
                        req = requests.get(self.release_source[i]).json()
                        if index == 0 and app_type == "Tweaked" or index == 0 and app_type == "apps":
                            version = req[1]["name"]
                            changelog = req[1]["body"]
                            released_date = req[1]["assets"][10]["created_at"]
                            size = req[1]["assets"][10]["size"]
                        else:
                            version = req[0]["name"]
                            changelog = req[0]["body"]
                            released_date = req[0]["assets"][0]["created_at"]
                            size = req[0]["assets"][0]["size"]
                    except KeyError:
                        raise Exception("Rate limited by github. can't use github api for a while")
        try:
            version = version.strip(app_name).strip("v").strip()
            released_date = ''.join(released_date.split('T')[:-1])
        except AttributeError:
            raise Exception("Something went wrong, please ask to developer.")
        self.logger(1, f"index: {index}, current: {current_ver}, new: {version}")
        if version > current_ver:
            self.logger(0, f"New version available: {version}, updating...")
            self.rw(repo, "../altstore_repo.json", "../scarlet_repo.json", version, int(index), app_type, current_ver, changelog, released_date, size)
        else:
            self.logger(0, "Up to date.")

    
    def rw(self, repo_type, altstore_path, scarlet_path, version, index, app_type, current_ver, version_description, release_date, size):
            if repo_type == "scarlet":
                with open(scarlet_path, "r") as scarlet_repo:
                    self.logger(0, "Loading data...")
                    json_data = json.load(scarlet_repo)
                    self.logger(0, "Modifying loaded data...")
                    json_data[app_type][index]["version"] = version.strip(" " + json_data[app_type][index]["name"])
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
                    json_data[app_type][index]["version"] = version.strip(" " + json_data[app_type][index]["name"])
                    json_data[app_type][index]["downloadURL"] = json_data[app_type][index]["downloadURL"].replace(current_ver, version)
                    json_data[app_type][index]["versionDescription"] = version_description
                    json_data[app_type][index]["versionDate"] = release_date
                    json_data[app_type][index]["versions"].insert(0, {"version": version.strip(" " + json_data[app_type][index]["name"]),
                                                                      "date": release_date,
                                                                      "localizedDescription": version_description,
                                                                      "downloadURL": json_data[app_type][index]["downloadURL"].replace(current_ver, version),
                                                                      "size": size})
                    if index == 2:
                        json_data[app_type][index]["downloadURL"] = json_data[app_type][index]["downloadURL"].replace(current_ver.replace("-", "_"), version.replace("-", "_"))
                with open(altstore_path, "w") as altstore_repo:
                    json.dump(json_data, altstore_repo, indent=2)
                    self.logger(0, f"Writed to: {altstore_path} successfully.")
            
            else:
                raise Exception("Unexpected mode")
            
            """
            FIXME: Edit readme
            with open("../README.md", "r") as file:
                self.logger(0, "Loading readme.md data...")
                for line in file.readlines():
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
                            self.fetch("altstore", key["name"], i, item, key["version"], key["downloadURL"])
                        elif path == "../scarlet_repo.json":
                            self.fetch("scarlet", key["name"], i, item, key["version"], key["down"])
                        else:
                            raise Exception("Unexpected repo!")
                    except TypeError as e:
                        if str(e) == "string indices must be integers, not 'str'" or "string indices must be integers":
                            pass
                        else:
                            raise TypeError(e)
        self.logger(0, f"All done! may take 1~2m(Page build time) to apply.")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--production":
            Fetch().automate("../scarlet_repo.json")
            Fetch().automate("../altstore_repo.json")
        if sys.argv[1] == "--test":
            Fetch().fetch(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    except IndexError:
        print("ERROR: Needed argument not found. example: --production")
