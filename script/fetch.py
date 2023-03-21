import requests
import json
import sys
import re


class RateLimited(Exception):
    pass


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
    

    def fetch(self, repo: str, app_name: str, index: int, app_type: str, current_ver, current_download_url: str):
        version = None
        changelog = None
        released_date = None
        size = None
        download_url = None
        current_name_no_version = None
        asset_name_no_version = None
        # FIXME: Handle uYou without any extra code
        if index == 3:
            version = "2.1"
            released_date = "2021-10-28"
            changelog = "Unknown - Ask to developer"
            size = 110100480
            download_url = "https://miro92.com/repo/depictions/com.miro.uyou/iPA/YouTube_16.42.3_uYou_2.1.ipa",
            self.logger(2, "uYou detected! using 2.1 instead of latest.")
        else:
            for i, releases in enumerate(self.release_source):
                if releases.replace("api.", "").replace("repos/", "") in current_download_url:
                    req = requests.get(self.release_source[i])
                    if req.status_code == 403:
                        self.logger(3, "Looks like github limited this ip.")
                        raise RateLimited("Rate limited")
                    req = requests.get(self.release_source[i]).json()
                    for release in req:
                        target_release = release["name"]
                        if not re.match(fr"^{app_name} (\d+)[\s()]+.*$", target_release):
                            current_filename = re.search(r"(?<=/)[^/]+$", current_download_url)
                            pattern = re.compile(r"^(.+?)[\-_\.]\d+[\-_\.](.+)\.([^.]+)$")
                            release_name_match = re.match(r"(.+)\s\(\w+\)$", target_release)
                            if release_name_match is not None:
                                continue
                            for asset in release["assets"]:
                                asset_name_match = pattern.match(asset["name"])
                                current_name_match = pattern.match(current_filename.group())
                                try:
                                    asset_name_no_version = asset_name_match.group(1) + "-" + asset_name_match.group(2) + "." + asset_name_match.group(3)
                                    current_name_no_version = current_name_match.group(1) + "-" + current_name_match.group(2) + "." + current_name_match.group(3)
                                except AttributeError:
                                    pass
                                if asset_name_match and current_name_match:
                                    if asset_name_no_version is not None and current_name_no_version is not None and asset_name_no_version == current_name_no_version:
                                        if version is None: version = release["name"].strip(app_name).strip("v").strip()
                                        if changelog is None: changelog = release["body"]
                                        if released_date is None: released_date = ''.join(asset["created_at"].split('T')[:-1])
                                        if size is None: size = asset["size"]
                                        if download_url is None: download_url = asset["browser_download_url"]
                                else:
                                        if version is None: version = release["name"].strip(app_name).strip("v").strip()
                                        if changelog is None: changelog = release["body"]
                                        if released_date is None: released_date = ''.join(asset["created_at"].split('T')[:-1])
                                        if size is None: size = asset["size"]
                                        if download_url is None: download_url = asset["browser_download_url"]
        self.logger(1, f"index: {index}, current: {current_ver}, new: {version}")
        if version > current_ver:
            self.logger(0, f"New version available: {version}, Parsing to rw...")
            self.rw(repo, "../altstore_repo.json" if repo == "altstore" else "../scarlet_repo.json", current_ver, version, download_url, int(index), app_type, changelog, released_date, size)
        else:
            self.logger(0, "Up to date. Nothing to do.")

    
    def rw(self, repo_type, path, current_ver, version, download_url: str, index, app_type, version_description, release_date, size):
            self.logger(0, "Loading repo file... this may take a while")
            with open(path, "r") as repo_path:
                self.json_data = json.load(repo_path)
                self.logger(0, "Modifying loaded data...")
                if repo_type == "scarlet":
                    self.json_data[app_type][index]["version"] = version
                    self.json_data[app_type][index]["down"] = download_url
                
                elif repo_type == "altstore":
                    self.json_data[app_type][index]["version"] = version
                    self.json_data[app_type][index]["downloadURL"] = download_url
                    self.json_data[app_type][index]["versionDescription"] = version_description
                    self.json_data[app_type][index]["versionDate"] = release_date
                    try:
                        self.json_data[app_type][index]["versions"].insert(0, {"version": version,
                                                                        "date": release_date,
                                                                        "localizedDescription": version_description,
                                                                        "downloadURL": download_url,
                                                                        "size": size})
                    except KeyError:
                        self.logger(2, "Looks like this app doesn't have versions key. Skipping...")

                else:
                    raise Exception("Unexpected mode! - Try submit issue.")
     
                with open("../README.md", "r") as file:
                    self.logger(0, "Loading readme.md data...")
                    data = file.read()
                
                with open("../README.md", "w") as file:
                    file.write(data.replace(current_ver, version))
                    self.logger(0, f"Writed to: ../README.md successfully.")

                with open(path, "w") as repo_path:
                    json.dump(self.json_data, repo_path, indent=2)
                    self.logger(0, f"Writed to: {path} successfully.")
            

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
                        elif path == "../README.md":
                            self.fetch("readme", key["name"], i, item, key["version"], key["downloadURL"])
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
        try:
            if sys.argv[1] == "--production" and sys.argv[2] == "altstore":
                Fetch().automate("../altstore_repo.json")
            elif sys.argv[1] == "--production" and sys.argv[2] == "scarlet":
                Fetch().automate("../scarlet_repo.json")
        except IndexError:
            if sys.argv[1] == "--production":
                Fetch().automate("../altstore_repo.json")
                Fetch().automate("../scarlet_repo.json")
        if sys.argv[1] == "--test":
            Fetch().fetch(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    except IndexError:
        print("ERROR: Needed argument not found. example: --production")