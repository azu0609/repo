import requests
import json

class Fetch:
    def __init__(self):
        self.src = ["https://api.github.com/repos/enmity-mod/tweak/releases/latest".strip("v")]
        self.current_ver = ["2.1.3"]

    def fetch(self, app):
        version = requests.get(self.src[app]).json()["name"]
        if version > self.current_ver[app]:
            print(f"{self.current_ver} >>> {version}")
            print("New version found! - Replacing...")
            self.read("../scarlet_repo.json", version)
        else:
            print("Latest.")

    
    def read(self, path, version):
        with open(path, "r") as target:
            data = json.load(target)
        
        data["version"] = version
        with open(path, "w") as w:
            json.dump(data, w)

        """
        with open(path, "r") as target:
            data = json.load(target)
            for item in data:
                if item["version"] in [str(self.current_ver[0])]:
                    item["version"] = version
        
        with open(path, "w") as w:
            json.dump(data, w, indent=2)
        """

if __name__ == "__main__":
    Fetch().fetch(0)