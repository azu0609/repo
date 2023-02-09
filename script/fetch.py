import requests
import json

class Fetch:
    def __init__(self):
        self.src = ["https://api.github.com/repos/enmity-mod/tweak/releases/latest"]
        self.current_ver = ["2.1.3"]

    def fetch(self, index):
        version = requests.get(self.src[index]).json()["name"]
        version = version.strip("v")
        if version > self.current_ver[index]:
            print(f"{self.current_ver} >>> {version}")
            print("New version found! - Replacing...")
            self.read("/home/azuki/Documents/repo/scarlet_repo.json", version, index)
        else:
            print("Latest.")

    
    def read(self, path, version, index):
        """
        print(version)
        with open(path, "r") as target:
            data = json.load(target)
        
        data["version"] = version
        with open(path, "w") as w:
            json.dump(data, w, indent=4)
        """
        # with open(path, "r") as file:
            # json_data = json.load(file)
            # print("a" + json_data["Tweaked"][0]["version"])
        # print()
        
        with open(path, 'r') as file:
            json_data = json.load(file)
            if json_data["Tweaked"][index]["version"] == self.current_ver:
                json_data["Tweaked"][index]["version"] = version
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
        
        

if __name__ == "__main__":
    Fetch().fetch(0)