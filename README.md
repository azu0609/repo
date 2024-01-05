<div align="center">
    <img src="https://azu0609.github.io/repo/repo.logo.png">
    <h1>azu0609's repo</h1>
    <p>Personalized repo for me. hosted in github pages.</p>
    <hr />
    <a href="https://azu0609.github.io/repo/url_handler.html">
        <img src="https://img.shields.io/badge/Altstore-Altstore.svg?label=Add%20To&logo=&style=for-the-badge&color=1B8085">
    </a>
</div>


> [!WARNING]
> This repository uses self-made update script, which is unstable and might cause some issues such as can't load repository.
> Most issues are resolved in ~24h

## Included IPA:

| String | Description |
|:------:|:-----------:|
| A | Altstore |
| S | Scarlet |

| Type | Application | Bundle | Base | Version | Author | Working? | Availability |
|:----:|:----------:|:------:|:------------:|:-------:|:------:|:------:|:------:|
| Tweaked app | [uYou](https://github.com/MiRO92/uYou-for-YouTube) | com.google.ios.youtube | 18.14.1 | 3.0 | [MIRO92](https://github.com/MiRO92) | Semi(A/S) | A/S |
| Tweaked app | [uYou+](https://github.com/qnblackcat/uYouPlus) | com.google.ios.youtube | 18.14.1-3.0 | 3.0 | [qnblackcat](https://github.com/qnblackcat) | Yes(any) | A/S |
| Tweaked app | [Enmity](https://enmity.app) | com.hammerandchisel.discord | 202.0 | v2.2.6-b6 | [enmity-mod](https://github.com/enmity-mod) | Yes(any) | A/S |
| Tweaked app | [Rosiecord (Plumpy - GGSans)](https://github.com/acquitelol/rosiecord) | com.hammerandchisel.discord | v2.1.4 | 209 | [acquitelol](https://github.com/acquitelol) | Semi(S) | S |
| Sideloaded | [Anime Now!](https://github.com/AnimeNow-Team/AnimeNow) | com.errorerrorerror.animenow | N/A | 3.0 | [errorerrorerror](https://github.com/errorerrorerror) | Yes(any) | A/S |
| MacDirtycow | [Cowabunga](https://github.com/leminlimez/Cowabunga) | com.leemin.Cowabunga | N/A | 10.3.2 | [leminlimez](https://github.com/leminlimez) | Yes(any) | A/S |
| MacDirtycow | [KillMyOTA](https://github.com/haxi0/KillMyOTA) | org.haxi0.KillMyOTA | N/A | 1.1 | [haxi0](https://github.com/haxi0) | Yes(any) | A/S |
| MacDirtyCow | [ControlConfig](https://github.com/BomberFish/ControlConfig) | com.f1shy-dev.ControlConfig | N/A | 0.1.0-alpha | [BomberFish](https://github.com/BomberFish) | Yes(any) | A/S |
| MacDirtycow | [SantanderEscaped](https://github.com/haxi0/SantanderEscaped) | org.haxi0.santanderescaped | N/A | 0.4 | [SerenaKit](https://github.com/SerenaKit/Santander) / [haxi0](https://github.com/haxi0) | Yes(any) | A/S |
| MacDirtyCow | [AppCommander](https://github.com/BomberFish/AppCommander) | ca.bomberfish.AppCommander | N/A | 1.0.0 | [BomberFish](https://github.com/BomberFish) | Yes(any) | A/S |
| MacDirtyCow | [Whitelist](https://github.com/BomberFish/Whitelist) | ca.bomberfish.Whitelist | N/A | 1.1.0 | [BomberFish](https://github.com/BomberFish) | Yes(any) | A/S |

## Add apps to repo
1. Add json data:
    Scarlet:
    ```
    {
        "name": "Name of application",
        "version": "0.1",
        "down": "link_to_file",
        "dev": "Cool developer name",
        "icon": "link_to_app_icon",
        "category": "category",
        "description": "Description of application",
        "bundleID": "app.bundle.id",
        "screenshots" [
            "link_to_screenshot1",
            "link_to_screenshot2",
            "link_to_screenshot3"
        ],
        "contact": {
            "web": "developer_website",
            "twitter": "https://twitter.com/developer"
        }
    }
    ```
    For more value in scarlet json manifest, see [Scarlet official repo](https://usescarlet.com/scarlet.json).
    
    Altstore:
    ```
    {
        "name": "Name of app",
        "bundleIdentifier": "app.bundle.id",
        "developerName": "Cool developer name",
        "subtitle": "Subtitle (Shows on below of title, 0~15 recommend)",
        "version": "0.2",
        "versionDate": "date-of-release",
        "versionDescription": "Description of version (like what's changed, this part replaced with release body)",
        "downloadURL": "link_to_file",
        "versions": [
            {
                "version": "0.2",
                "date": "yyyy-mm-dd",
                "localizedDescription": "Description of version (like what's changed, this part replaced with release body)",
                "downloadURL": "link_to_file_of_this_release",
                "size": 1
            },
            {
                "version": "0.1",
                "date": "yyyy-mm-dd",
                "localizedDescription": "Description of version (like what's changed, this part replaced with release body)",
                "downloadURL": "link_to_file_of_this_release",
                "size": 1
            }
        ],
        "localizedDescription": "Long description of this app. Show off how cool is!",
        "iconURL": "link_to_app_icon",
        "size": 1,
        "beta": false
    }
    ```
    For more infomation about altstore json manifest, see [Make a Source (Altstore FAQ)](https://faq.altstore.io/sources/make-a-source).


2. Check if working correctly by running script:  
`python3 fetch.py --production`  
Script should show current version, latest version and current json index then try to update if working correctly.
