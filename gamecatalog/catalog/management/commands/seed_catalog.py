from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Game, License, Platform, Tag

LICENSES = [
    ("GPL-2.0", True, "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html"),
    ("GPL-3.0", True, "https://www.gnu.org/licenses/gpl-3.0.html"),
    ("MIT", False, "https://opensource.org/license/mit"),
    ("Apache-2.0", False, "https://www.apache.org/licenses/LICENSE-2.0"),
    ("Zlib", False, "https://opensource.org/license/zlib"),
    ("CC0-1.0", False, "https://creativecommons.org/publicdomain/zero/1.0/"),
]

PLATFORMS = ["Windows", "macOS", "Linux", "Android", "Web"]

TAGS = [
    "Strategy", "RTS", "Racing", "Shooter", "Roguelike", "RPG",
    "Sandbox", "Simulation", "Platformer", "Arcade", "Multiplayer",
    "Turn-based", "Tower Defense", "Open World",
]

GAMES = [
    {
        "title": "0 A.D.",
        "summary": "A free real-time strategy game of ancient warfare.",
        "description": "0 A.D. is a historically grounded real-time strategy game spanning the rise and fall of ancient civilizations. Build a settlement, manage an economy, and lead armies across land and sea.",
        "license": "GPL-2.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Strategy", "RTS", "Multiplayer"],
        "homepage_url": "https://play0ad.com/",
        "source_url": "https://github.com/0ad/0ad",
        "stars": 3900,
    },
    {
        "title": "SuperTuxKart",
        "summary": "A 3D kart racer with a wide roster and battle modes.",
        "description": "A cartoon-style 3D racing game featuring open-source mascots. Race across varied tracks, play split-screen locally, or join online servers.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "tags": ["Racing", "Arcade", "Multiplayer"],
        "homepage_url": "https://supertuxkart.net/",
        "source_url": "https://github.com/supertuxkart/stk-code",
        "stars": 4700,
    },
    {
        "title": "The Battle for Wesnoth",
        "summary": "A turn-based tactical fantasy strategy game.",
        "description": "Command your troops across a deep fantasy campaign. Wesnoth pairs turn-based tactics with an enormous library of community-made campaigns.",
        "license": "GPL-2.0",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "tags": ["Strategy", "Turn-based", "RPG"],
        "homepage_url": "https://www.wesnoth.org/",
        "source_url": "https://github.com/wesnoth/wesnoth",
        "stars": 5400,
    },
    {
        "title": "Xonotic",
        "summary": "A fast-paced arena first-person shooter.",
        "description": "A fully free arena shooter descended from Nexuiz. Xonotic is built for twitch movement, rocket jumps, and competitive online play.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Shooter", "Arcade", "Multiplayer"],
        "homepage_url": "https://xonotic.org/",
        "source_url": "https://gitlab.com/xonotic",
        "stars": 2100,
    },
    {
        "title": "Mindustry",
        "summary": "A tower-defense game about factories and logistics.",
        "description": "Build supply chains that feed your turrets and survive escalating waves. Mindustry blends factory automation with tower defense and co-op play.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "tags": ["Tower Defense", "Simulation", "Strategy"],
        "homepage_url": "https://mindustrygame.github.io/",
        "source_url": "https://github.com/Anuken/Mindustry",
        "stars": 24000,
    },
    {
        "title": "OpenTTD",
        "summary": "A transport business simulation you can build for years.",
        "description": "Grow a transport empire of trains, trucks, ships, and planes. OpenTTD is a faithful open-source remake of Transport Tycoon Deluxe with heavy modding support.",
        "license": "GPL-2.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Simulation", "Strategy", "Open World"],
        "homepage_url": "https://www.openttd.org/",
        "source_url": "https://github.com/OpenTTD/OpenTTD",
        "stars": 6600,
    },
    {
        "title": "Luanti",
        "summary": "An open-source voxel game engine and sandbox.",
        "description": "Formerly Minetest, Luanti is a voxel sandbox and engine. Play community games, build worlds, or write your own game in Lua.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "tags": ["Sandbox", "Open World", "Multiplayer"],
        "homepage_url": "https://www.luanti.org/",
        "source_url": "https://github.com/luanti-org/luanti",
        "stars": 11000,
    },
    {
        "title": "Endless Sky",
        "summary": "A space trading and combat sandbox.",
        "description": "Trade, explore, and fight your way across a living galaxy. Endless Sky is an open-ended 2D space game with a sprawling story and modding scene.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Simulation", "RPG", "Open World"],
        "homepage_url": "https://endless-sky.github.io/",
        "source_url": "https://github.com/endless-sky/endless-sky",
        "stars": 6200,
    },
    {
        "title": "Veloren",
        "summary": "A multiplayer voxel RPG in active development.",
        "description": "Veloren is an open-world, open-source multiplayer RPG inspired by Cube World and Dwarf Fortress. Explore a procedurally generated world with friends.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["RPG", "Open World", "Multiplayer"],
        "homepage_url": "https://veloren.net/",
        "source_url": "https://gitlab.com/veloren/veloren",
        "stars": 3800,
    },
    {
        "title": "Cataclysm: Dark Days Ahead",
        "summary": "A deep turn-based survival roguelike.",
        "description": "Survive a post-apocalyptic world of the undead and worse. Cataclysm: DDA is famous for its staggering simulation depth and crafting systems.",
        "license": "CC0-1.0",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "tags": ["Roguelike", "Simulation", "Turn-based"],
        "homepage_url": "https://cataclysmdda.org/",
        "source_url": "https://github.com/CleverRaven/Cataclysm-DDA",
        "stars": 10000,
    },
    {
        "title": "Shattered Pixel Dungeon",
        "summary": "A polished traditional roguelike dungeon crawler.",
        "description": "Descend a deadly dungeon one floor at a time. Shattered Pixel Dungeon is an approachable, endlessly replayable roguelike with regular updates.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "Linux", "Android"],
        "tags": ["Roguelike", "RPG", "Turn-based"],
        "homepage_url": "https://shatteredpixel.com/",
        "source_url": "https://github.com/00-Evan/shattered-pixel-dungeon",
        "stars": 4600,
    },
    {
        "title": "FreeCiv",
        "summary": "A turn-based empire-building strategy game.",
        "description": "Lead a civilization from antiquity to the space age. FreeCiv is a long-running open-source take on the classic 4X strategy formula.",
        "license": "GPL-2.0",
        "platforms": ["Windows", "macOS", "Linux", "Web"],
        "tags": ["Strategy", "Turn-based", "Multiplayer"],
        "homepage_url": "https://www.freeciv.org/",
        "source_url": "https://github.com/freeciv/freeciv",
        "stars": 3200,
    },
    {
        "title": "Hedgewars",
        "summary": "A turn-based artillery game with hedgehogs.",
        "description": "A worms-style turn-based artillery game. Take turns lobbing wacky weapons at rival hedgehog teams, locally or online.",
        "license": "GPL-2.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Arcade", "Turn-based", "Multiplayer"],
        "homepage_url": "https://www.hedgewars.org/",
        "source_url": "https://github.com/hedgewars/hw",
        "stars": 900,
    },
    {
        "title": "Teeworlds",
        "summary": "A fast, cartoonish 2D multiplayer shooter.",
        "description": "A retro 2D online shooter built around grappling hooks and tight platforming. Teeworlds is quick to pick up and built for chaotic team play.",
        "license": "Zlib",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Shooter", "Platformer", "Multiplayer"],
        "homepage_url": "https://www.teeworlds.com/",
        "source_url": "https://github.com/teeworlds/teeworlds",
        "stars": 4300,
    },
    {
        "title": "Unvanquished",
        "summary": "A team shooter blending FPS and RTS play.",
        "description": "Two asymmetric teams, aliens and humans, fight while building and upgrading their base. Unvanquished fuses first-person shooting with real-time strategy.",
        "license": "GPL-3.0",
        "platforms": ["Windows", "macOS", "Linux"],
        "tags": ["Shooter", "RTS", "Multiplayer"],
        "homepage_url": "https://unvanquished.net/",
        "source_url": "https://github.com/Unvanquished/Unvanquished",
        "stars": 1000,
    },
]


class Command(BaseCommand):
    help = "Populate the catalog with a curated set of open-source games."

    @transaction.atomic
    def handle(self, *args, **options):
        licenses = {
            name: License.objects.update_or_create(
                name=name, defaults={"is_copyleft": copyleft, "url": url}
            )[0]
            for name, copyleft, url in LICENSES
        }
        platforms = {
            name: Platform.objects.get_or_create(name=name)[0] for name in PLATFORMS
        }
        tags = {name: Tag.objects.get_or_create(name=name)[0] for name in TAGS}

        for entry in GAMES:
            game, _ = Game.objects.update_or_create(
                title=entry["title"],
                defaults={
                    "summary": entry["summary"],
                    "description": entry["description"],
                    "license": licenses[entry["license"]],
                    "homepage_url": entry["homepage_url"],
                    "source_url": entry["source_url"],
                    "stars": entry["stars"],
                    "is_published": True,
                },
            )
            game.platforms.set(platforms[name] for name in entry["platforms"])
            game.tags.set(tags[name] for name in entry["tags"])

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {len(GAMES)} games successfully.")
        )
