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
                               "https://api.github.com/repos/haxi0/KillMyOTA/releases",
                               "https://api.github.com/repos/BomberFish/ControlConfig/releases",
                               "https://api.github.com/repos/haxi0/SantanderEscaped/releases"]
        
        self.blacklist_release = [
            {
                "name": "uYou",
                "version": "2.1",
                "state": "invalid"
            },
            {
                "name": "Cowabunga",
                "version": "10",
                "state": "invalid"
            }
        ]


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


    def compare_versions(self, current_ver, new_ver):
        current_parts = current_ver.split('.')
        new_parts = new_ver.split('.')
        for i in range(len(new_parts)):
            if i >= len(current_parts):
                return True
            if new_parts[i] != current_parts[i]:
                return new_parts[i] > current_parts[i]
        if len(new_parts) > len(current_parts):
            return True
        elif len(new_parts) == len(current_parts):
            new_suffix = new_ver.split('.')[-1].split('-')[-1]
            current_suffix = current_ver.split('.')[-1].split('-')[-1]
            if new_suffix != '' and current_suffix != '':
                return new_suffix > current_suffix
            else:
                return new_ver > current_ver
        return False


    def fetch(self, repo: str, app_name: str, index: int, app_type: str, current_ver, current_download_url: str):
        version = None
        changelog = None
        released_date = None
        size = None
        download_url = None
        current_name_no_version = None
        asset_name_no_version = None
        if index == 3 and app_type == "Tweaked" and repo == "scarlet" or index == 3 and repo == "altstore":
            version = "2.1"
            released_date = "2021-10-28"
            changelog = "Unknown"
            size = 110100480
            download_url = "https://miro92.com/repo/depictions/com.miro.uyou/iPA/YouTube_16.42.3_uYou_2.1.ipa",
            self.logger(2, f"uYou detected in following index: {index}! using 2.1 instead of latest.")
        else:
            for i, releases in enumerate(self.release_source):
                if releases.replace("api.", "").replace("repos/", "") in current_download_url:
                    req = requests.get(self.release_source[i])
                    if req.status_code == 403:
                        self.logger(3, "Looks like Github limited this ip.")
                        raise RateLimited("Rate limited by Github")
                    req = req.json()
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
                                        if changelog is None: changelog = release["body"].replace('"', "'")
                                        if released_date is None: released_date = ''.join(asset["created_at"].split('T')[:-1])
                                        if size is None: size = asset["size"]
                                        if download_url is None: download_url = asset["browser_download_url"].replace("%2B", "+")
                                else:
                                        if version is None: version = release["name"].strip(app_name).strip("v").strip()
                                        if changelog is None: changelog = release["body"].replace('"', "'")
                                        if released_date is None: released_date = ''.join(asset["created_at"].split('T')[:-1])
                                        if size is None: size = asset["size"]
                                        if download_url is None: download_url = asset["browser_download_url"].replace("%2B", "+")
        self.logger(1, f"index: {index}, current: {current_ver}, new: {version}")
        if self.compare_versions(current_ver, version):
            self.logger(0, f"New version available: {version}, verifing compatibility...")
            for blocked in self.blacklist_release:
                if blocked["name"] == app_name and blocked["version"] == version and blocked["state"] == "valid":
                    self.logger(2, f"NG: {app_name}+{version} - In blacklist")
                    break
                else:
                    self.logger(0, f"OK - Parsing to rw")
                    self.rw(repo, "../altstore_repo.json" if repo == "altstore" else "../scarlet_repo.json", current_ver, version, download_url, int(index), app_type, changelog, released_date, size)
                    break
        else:
            self.logger(0, "Up to date. Nothing to do.")

    
    def rw(self, repo_type, path, current_ver, version, download_url: str, index, app_type, version_description, release_date, size):
            self.logger(1, "Fetching repo data...")
            with open(path, "r") as repo_path:
                self.json_data = json.load(repo_path)
                self.logger(1, "Modifying loaded data...")
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
                        self.logger(2, "Looks like this app doesn't have versions key. adding...")
                        self.json_data[app_type][index]["versions"] = [
                            {
                            "version": version,
                            "date": release_date,
                            "localizedDescription": version_description,
                            "downloadURL": download_url,
                            "size": size
                            }
                        ]

                else:
                    raise Exception("Unexpected mode!")
     
                with open("../README.md", "r") as file:
                    self.logger(0, "Fetching readme.md data...")
                    data = file.read()
                
                with open("../README.md", "w") as file:
                    file.write(data.replace(current_ver, version))

                with open(path, "w") as repo_path:
                    json.dump(self.json_data, repo_path, indent=2)
                
                self.logger(0, f"Writing process ended without any error")
            

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
        self.logger(0, f"Updating process ended successfully.")


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
        print('\033[92m' + f"All done! may take 1~2m(Page build time) to apply.")
        if sys.argv[1] == "--test":
            Fetch().fetch(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    except IndexError:
        print("ERROR: Needed argument not found. example: --production")