# Game Caching

We want to cache game data in our PostgreSQL database so that we don't' have to use multiple API calls for recenlty displayed games. This should speed up page loads for frequently viewed games.

## Game Cache Table

```sql
TABLE: game_cache

COLUMNS:
steam_app_id: INT PRIMAY KEY    <-- Stores steam id for the game
last_updated: TIMESTAMP         <-- Allows us to only use recently cached games
title: TEXT
short_decription: TEXT
detailed_description: TEXT
header_img: TEXT                <-- URL to game picture
developers: TEXT
publishers: TEXT
platform_windows: BOOLEAN
platform_mac: BOOLEAN
platform_linux: BOOLEAN
pc_requirements_min: TEXT
pc_requirements_rec: TEXT
linux_requirements_min: TEXT
linux_requirements_rec: TEXT
mac_requirements_min: TEXT
mac_requirements_rec: TEXT
metacritic_score: VARCHAR(3)
metacritic_url: VARCHAR(3)
metacritic_color: VARCHAR(3)
legal_notice: TEXT
achievements_total: INT

```

* Add ```self.categories``` once it is implemnted in ```game_page.html```

## Categories Table

NOT YET DESIGNED

```bash
self.categories:  [{'id': 2, 'description': 'Single-player'}, {'id': 1, 'description': 'Multi-player'}, {'id': 49, 'description': 'PvP'}, {'id': 36, 'description': 'Online PvP'}, {'id': 9, 'description': 'Co-op'}, {'id': 38, 'description': 'Online Co-op'}, {'id': 22, 'description': 'Steam Achievements'}, {'id': 35, 'description': 'In-App Purchases'}, {'id': 18, 'description': 'Partial Controller Support'}, {'id': 41, 'description': 'Remote Play on Phone'}, {'id': 42, 'description': 'Remote Play on Tablet'}]
```

## Screenshot Table

NOT YET DESIGNED

```bash
self.screenshots:  [{'id': 0, 'path_thumbnail': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_66b553f4c209476d3e4ce25fa4714002cc914c4f.600x338.jpg?t=1720558643', 'path_full': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_66b553f4c209476d3e4ce25fa4714002cc914c4f.1920x1080.jpg?t=1720558643'}, {'id': 1, 'path_thumbnail': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_bac60bacbf5da8945103648c08d27d5e202444ca.600x338.jpg?t=1720558643', 'path_full': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_bac60bacbf5da8945103648c08d27d5e202444ca.1920x1080.jpg?t=1720558643'}, {'id': 2, 'path_thumbnail': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_668dafe477743f8b50b818d5bbfcec669e9ba93e.600x338.jpg?t=1720558643', 'path_full': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_668dafe477743f8b50b818d5bbfcec669e9ba93e.1920x1080.jpg?t=1720558643'}, {'id': 3, 'path_thumbnail': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_4ce07ae360b166f0f650e9a895a3b4b7bf15e34f.600x338.jpg?t=1720558643', 'path_full': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_4ce07ae360b166f0f650e9a895a3b4b7bf15e34f.1920x1080.jpg?t=1720558643'}, {'id': 4, 'path_thumbnail': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_d1a8f5a69155c3186c65d1da90491fcfd43663d9.600x338.jpg?t=1720558643', 'path_full': 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/ss_d1a8f5a69155c3186c65d1da90491fcfd43663d9.1920x1080.jpg?t=1720558643'}]
```

## Achievement Table

NOT YET DESIGNED

```bash
self.achievements:  {'total': 51, 'highlighted': [{'name': 'Back in the Mud', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/3f5b6b4295a58d39b7619e5723f94b8f475dd81e.jpg'}, {'name': 'Just a Scratch', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/1d0bdc25d376a74b0ee37355ee32f9eb308dd90c.jpg'}, {'name': 'To Greener Pastures', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/cede247d21de983c4d0d8aed8b75d1324cac9bf3.jpg'}, {'name': 'Settling Feuds', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/ab025f0eacc998f62125d7a7bb186e9fbdd95d24.jpg'}, {'name': 'Washed Ashore', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/a07e4dac160f638c24ac851ffc0aea19bc51f12d.jpg'}, {'name': 'No Traitors', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/79a6c1cb5ac1f88150802768ab8c6a7078d272c1.jpg'}, {'name': 'Third Time Lucky', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/70286589047c58568477e6ba124161d6047cd023.jpg'}, {'name': 'Redemption', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/94fa0722da3453c6cd222b97b77880c29f7dc97c.jpg'}, {'name': 'Cowboy Builder', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/d2fdc9461799c466b1ff7a9f3666cd2dbb4f61e3.jpg'}, {'name': 'Endless Summer', 'path': 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1174180/caca2e3bed70ec5ce18c7d7e9a261aef5cf55737.jpg'}]}

```