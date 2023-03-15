from utils import Singleton
from typing import Any, List, Callable, Optional


class BaseGameData:
    def loads(self, data):
        for key, value in data.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                print("Wrong key: ", key)


class Map(BaseGameData):
    match_id: str
    game_time: int
    clock_time: int
    daytime: bool
    nightstalker_night: bool
    radiant_score: int
    dire_score: int
    game_state: str
    paused: bool
    win_team: str
    customgamename: str
    ward_purchase_cooldown: int


class Ability(BaseGameData):
    name: str
    level: int
    can_cast: bool
    passive: bool
    ability_active: bool
    cooldown: int
    ultimate: bool


class Item(BaseGameData):
    slot_name: str
    name: str
    purchaser: int
    passive: bool
    can_cast: bool
    cooldown: int
    contains_rune: str
    charges: int


class Hero(BaseGameData):
    xpos: int
    ypos: int
    hero_id: int
    name: str
    level: int
    xp: int
    alive: bool
    respawn_seconds: int
    buyback_cost: int
    buyback_cooldown: int
    health: int
    max_health: int
    health_percent: int
    mana: int
    max_mana: int
    mana_percent: int
    silenced: bool
    stunned: bool
    disarmed: bool
    magicimmune: bool
    hexed: bool
    muted: bool
    breaked: bool
    aghanims_scepter: bool
    aghanims_shard: bool
    smoked: bool
    has_debuff: bool
    talent_1: bool
    talent_2: bool
    talent_3: bool
    talent_4: bool
    talent_5: bool
    talent_6: bool
    talent_7: bool
    talent_8: bool
    attributes_level: int
    abilities: List[Ability]
    items: List[Item]

    def loads(self, data):
        super().loads(data["hero"])

        self.abilities = []
        for ability in data["abilities"].values():
            ability_object = Ability()
            ability_object.loads(ability)
            self.abilities.append(ability_object)

        self.items = []
        for slot_name, item_data in data["items"].items():
            item = Item()
            item_data["slot_name"] = slot_name
            item.loads(item_data)
            self.items.append(item)


class Player(BaseGameData):
    steamid: str
    accountid: str
    name: str
    activity: str
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    kill_streak: int
    commands_issued: int
    kill_list: Any
    team_name: str
    gold: int
    gold_reliable: int
    gold_unreliable: int
    gold_from_hero_kills: int
    gold_from_creep_kills: int
    gold_from_income: int
    gold_from_shared: int
    gpm: int
    xpm: int
    hero = Hero()

    def loads(self, data):
        super().loads(data["player"])

        hero_data = {
            "hero": data["hero"],
            "abilities": data["abilities"],
            "items": data["items"],
        }
        self.hero.loads(hero_data)


class GameState(metaclass=Singleton):
    map = Map()
    player = Player()
    _on_update: Optional[Callable] = None

    def __init__(self) -> None:
        self.gamestates_with_data = [
            'DOTA_GAMERULES_STATE_PRE_GAME',
            'DOTA_GAMERULES_STATE_GAME_IN_PROGRESS'
        ]

    def loads(self, data):
        try:
            self.map.loads(data["map"])

            if self.map.game_state not in self.gamestates_with_data:
                return

            player_data = {
                "player": data["player"],
                "hero": data["hero"],
                "abilities": data["abilities"],
                "items": data["items"],
            }
            self.player.loads(player_data)

            if self._on_update is not None:
                self._on_update(self)
        except KeyError:
            # Waiting for players to load
            # Waiting for all players select hero
            # Waiting for strategy time ends
            pass

    def on_update(self, function: Callable):
        self._on_update = function
