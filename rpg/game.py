from rpg.room.room import Room
from rpg.player import Player
from rpg.room.door import Door
from rpg.io_utils import Scanner, Saver
from rpg.npcs.npc import NPC
from rpg.npcs.enemy import Enemy
from rpg.npcs.healer import Healer
from tests.jsontest import JsonSerializable
import sys
from typing import Dict, Optional


class Game(JsonSerializable):
    """Main class to manage game state and handle gameplay mechanics."""

    def __init__(self) -> None:
        """Initializes the Game class with
        scanner, saver, and initial settings."""
        self.scanner: Scanner = Scanner()
        self.saver: Saver = Saver()
        self.reset_game()
        self.enemies_defeated: int = 0

    def reset_game(self) -> None:
        """Resets the game state by initializing
        rooms, NPCs, and player settings."""
        self.enemies_defeated = 0
        self.rooms: Dict[str, Room] = {}
        self.start_room: Room = Room(
            description="Practice room of boy group BTS. "
                        "The room is fully empty, "
                        "but you see a lot of mirrors."
        )

        self.rooms["Start Room"] = self.start_room
        self.room_2: Room = Room(
            description="Jungkook's vocal room. You see "
                        "several musical instruments, "
                        "a microphone, a camera, and a music sheet."
        )
        self.rooms["Room 2"] = self.room_2

        self.room_3: Room = Room(
            description="Jin's videogame room. The room is "
                        "a complete mess, with "
                        "clothes, food, and videogame cases "
                        "spread everywhere."
        )
        self.rooms["Room 3"] = self.room_3

        self.room_4: Room = Room(description="Taehyung's jazz room.")
        self.rooms["Room 4"] = self.room_4

        self.room_5: Room = Room(
            description="Recording studio. This is where "
                        "all the art is produced. "
                        "You see all sorts of music equipment."
        )
        self.rooms["Room 5"] = self.room_5

        self.room_6: Room = Room(
            description="Jimin's dance studio. All his "
                        "trophies and gold medals "
                        "are on display."
        )
        self.rooms["Room 6"] = self.room_6

        self.start_room.add_door(
            Door(description="A black soundproof iron door",
                 leads_to=self.room_2)
        )
        self.start_room.add_door(
            Door(description="A door with childish paintings, with a small "
                             "see-through gap. Has a 'DO NOT ENTER' sign",
                 leads_to=self.room_3)
        )
        self.start_room.add_npc(
            NPC(description="Bang PD",
                interact_message="Hello there! You must "
                                 "be here for the auditions. "
                                 "All I can say is, good luck. "
                                 "Feel free to explore the building.")
        )

        self.room_2.add_door(
            Door(description="A black soundproof iron door",
                 leads_to=self.start_room)
        )
        self.room_2.add_npc(
            NPC(description="Jungkook",
                interact_message="Hi! My name is Jungkook. "
                                 "This is my personal practice "
                                 "studio, but I'm letting the "
                                 "contestants in to get some rest.")
        )
        self.room_2.add_npc(
            Enemy(description="Vlad",
                  interact_message="I will obliterate you!")
        )

        self.room_3.add_door(
            Door(description="A door with childish paintings, with a small "
                             "see-through gap. Has a 'DO NOT ENTER' sign",
                 leads_to=self.start_room)
        )
        self.room_3.add_door(
            Door(description="A beautiful velvet colored door",
                 leads_to=self.room_4)
        )
        self.room_3.add_npc(
            NPC(description="Jin",
                interact_message="Oh, another one? Ugh. I guess "
                                 "no one takes the 'DO NOT ENTER' "
                                 "sign seriously. I'm busy with "
                                 "Mario Kart, and I'm tired of "
                                 "being interrupted.")
        )

        self.room_5.add_door(
            Door(description="A purple door with handwritten signatures",
                 leads_to=self.room_4)
        )
        self.room_5.add_door(
            Door(description="A fully mirrored door", leads_to=self.room_6)
        )
        self.room_5.add_npc(
            Healer(description="J-Hope",
                   interact_message="I'm your hope, you're my hope, "
                                    "I'm J-Hope! Let me help you "
                                    "with your next dance battle.")
        )
        self.room_5.add_npc(
            NPC(description="RM",
                interact_message="Glad to have you here! I'm RM. "
                                 "Wishing you good luck with the audition.")
        )
        self.room_5.add_npc(
            NPC(description="SUGA",
                interact_message="I'm working on this new song, "
                                 "but I can't seem to get it right.")
        )

        self.room_4.add_door(
            Door(description="A beautiful velvet colored door",
                 leads_to=self.room_3)
        )
        self.room_4.add_door(
            Door(description="A purple door with handwritten signatures",
                 leads_to=self.room_5)
        )
        self.room_4.add_npc(
            Healer(description="Taehyung",
                   interact_message="I see Jin bullied another "
                                    "kid in here. You look tired... "
                                    "I can help with that!")
        )
        self.room_4.add_npc(
            Enemy(description="Lisa", interact_message="Bring it on!")
        )

        self.room_6.add_door(
            Door(description="A fully mirrored door", leads_to=self.room_5)
        )
        self.room_6.add_npc(
            Enemy(description="Jimin",
                  interact_message="Hi! My name is Jimin. Congrats on making "
                  "it into the final stage! Wishing you good luck.")
        )
        self.room_6.add_npc(
            Enemy(description="Momo", interact_message="You're cooked!")
        )

        self.player: Player = Player(name="Jojo Siwa")
        self.player.enter_room(self.start_room)
        self.player._health = 100

    def play(self) -> None:
        """Handles the main game loop where player choices are managed."""
        while True:
            print("\nWhat do you want to do?")
            print("  (0) Look around")
            print("  (1) Look for a way out")
            print("  (2) Look for company")
            print("  (3) QuickSave")
            print("  (4) QuickLoad")
            print("  (5) Quit game")

            choice: int = self.scanner.read_int("> ")

            if choice == 0:
                self.player.inspect_room()
            elif choice == 1:
                self.player.look_for_way_out(self.scanner)
            elif choice == 2:
                self.player.look_for_company()
                current_room = self.player._current_room
                if current_room.npcs:
                    self.npc_option()
            elif choice == 3:
                self.saver.quick_save(self)
            elif choice == 4:
                loaded_game: Optional[Game] = self.saver.quick_load()
                if loaded_game:
                    self.__dict__.update(loaded_game.__dict__)
            elif choice == 5:
                sys.exit()
            elif choice == -1:
                print("Invalid input. Please enter a positive integer.")
            else:
                print("Invalid option. Try again.")

    def npc_option(self) -> None:
        """Handles interactions with NPCs based on player choices."""
        current_room: Room = self.player._current_room

        if not current_room.npcs:
            print("There is no one else here to interact with.")
            return

        npc_choice: int = self.scanner.read_int(
            "Select an NPC to interact with by index (-1: do nothing): "
        )

        if npc_choice == -1:
            return

        if 0 <= npc_choice < len(current_room.npcs):
            selected_npc: NPC = current_room.npcs[npc_choice]

            if isinstance(selected_npc, Enemy):

                if selected_npc._health <= 0:
                    current_room.npcs.remove(selected_npc)
                    print(f" You have already defeated "
                          f"{selected_npc.description}.")
                    return

                else:
                    print(f"You encountered an enemy: "
                          f"{selected_npc.description}!")
                    print(f"{selected_npc.description} says: "
                          f"{selected_npc.interact_message}")
                    print("Do you want to:")
                    print("  (0) Fight")
                    print("  (1) Go back")

                    action_choice: int = self.scanner.read_int("> ")

                    if action_choice == 0:
                        selected_npc.interact(self.player, self.scanner, self)
                    elif action_choice == 1:
                        print("You chose to go back.")
                    else:
                        print("Invalid choice.")

            elif isinstance(selected_npc, Healer):
                print(f"You encountered a healer: {selected_npc.description}!")
                print(f"{selected_npc.description} says: "
                      f"{selected_npc.interact_message}")
                print("Do you want to:")
                print("  (0) Restore full health")
                print("  (1) Go back")

                action_choice: int = self.scanner.read_int("> ")

                if action_choice == 0:
                    selected_npc.interact(self.player)
                elif action_choice == 1:
                    print("You chose to go back.")
                else:
                    print("Invalid choice.")
            else:
                print(f'"{selected_npc.description}" says: '
                      f'"{selected_npc.interact_message}."')
        else:
            print("Invalid NPC selection.")

    def enemy_defeated(self) -> None:
        """Increments the counter when an enemy is defeated."""
        self.enemies_defeated += 1
        if self.enemies_defeated >= 3:
            self.win()

    def win(self) -> None:
        """Displays the winning message and restarts the game."""
        print("\nCongratulations! You have defeated all the contestants and "
              "were selected to join BTS!")
        print("The game will now restart.")
        self.reset_game()
        self.play()

    def toJSON(self) -> Dict[str, Optional[dict]]:
        """Converts the game state to a JSON-compatible dictionary."""
        return {
            "player": self.player.toJSON(),
            "rooms": {name: room.toJSON() for name, room in
                      self.rooms.items()},
            "current_room": (self.player._current_room.description
                             if self.player._current_room else None)
        }

    @classmethod
    def fromJSON(cls, data: dict) -> "Game":
        """Creates a Game instance from a JSON-compatible dictionary."""
        game: Game = cls()
        game.rooms = {
            name: Room.fromJSON(room_data) for name, room_data in
            data.get("rooms", {}).items()
        }
        game.player = Player.fromJSON(data.get("player"))

        current_room_desc: Optional[str] = data.get("current_room")
        for room in game.rooms.values():
            if room.description == current_room_desc:
                game.player.enter_room(room)
                break

        return game
