import time
import random
from collections import defaultdict, Counter

class MurderMysteryGame:
    def __init__(self):
        self.players = ["Player" + str(i+1) for i in range(12)]
        self.roles = ["Investigator", "Lookout", "Sheriff", "Potion Master", 
                      "Whisperer", "Escort", "Mafiaso", "Framer", "Disguiser", 
                      "Serial Killer", "Survivor", "Jester"]
        self.player_roles = {}
        self.phase = "day"  # start at daytime
        self.day_count = 1
        self.alive_players = set(self.players)
        self.actions = defaultdict(list)  # stores night actions
    
    def assign_roles(self):
        random.shuffle(self.roles)
        self.player_roles = {self.players[i]: self.roles[i] for i in range(len(self.players))}
        print("Roles assigned:", self.player_roles)  # For debug

    def process_night_actions(self):
        deaths = []
        # Process night actions based on roles, e.g.:
        for player, role in self.player_roles.items():
            if player not in self.alive_players:
                continue
            action = self.receive_from_server(player, "action")  # Placeholder
            self.actions[role].append(action)

        # Example death resolution logic (specifics depend on game rules)
        # Implement role-specific interactions here
        deaths = [player for player, role in self.player_roles.items() if random.choice([True, False])]
        
        if deaths:
            self.announce(f"The following players died tonight: {', '.join(deaths)}")
            self.alive_players.difference_update(deaths)
        else:
            self.announce("It was a peaceful night.")

    def day_phase(self):
        self.announce(f"Day {self.day_count} begins!")
        if self.day_count == 1:
            self.assign_roles()

        self.chat_time()
        self.voting_phase()

    def chat_time(self):
        self.announce("Chat time! Players may talk for 1 minute.")
        time.sleep(60)  # Simulate chat duration

    def voting_phase(self):
        self.announce("Voting time! Players have 45 seconds to vote.")
        time.sleep(45)  # Simulate voting duration
        suspect = self.receive_from_server(None, "suspect_vote")  # Placeholder
        self.trial_phase(suspect)

    def trial_phase(self, suspect):
        self.announce(f"{suspect} is on trial. Plead your case!")
        self.receive_from_server(suspect, "plea")  # Placeholder for plea
        verdict = self.receive_from_server(None, "guilty_vote")  # Placeholder for group vote
        if verdict.count("guilty") > verdict.count("not guilty"):
            self.announce(f"{suspect} was found guilty and has been hanged.")
            self.alive_players.remove(suspect)
        else:
            self.announce(f"{suspect} was found not guilty and is spared.")

    def night_phase(self):
        self.announce("Night falls, and players take actions.")
        self.process_night_actions()

    def check_win_conditions(self):
        role_counts = Counter(self.player_roles[player] for player in self.alive_players)
        if role_counts["Mafiaso"] == 0 and role_counts["Framer"] == 0:
            self.announce("Town wins! All mafia members are dead.")
            return True
        elif all(role not in role_counts for role in ["Investigator", "Lookout", "Sheriff"]):
            self.announce("Mafia wins! All town members are dead.")
            return True
        return False

    def game_loop(self):
        while True:
            if self.phase == "day":
                self.day_phase()
                self.phase = "night"
            elif self.phase == "night":
                self.night_phase()
                self.phase = "day"
                self.day_count += 1

            if self.check_win_conditions():
                break

    def announce(self, message):
        print(message)  # Replace with actual server announcement logic
        self.send_to_server("announce", message)  # Placeholder

    def send_to_server(self, message_type, message):
        # Placeholder for server communication
        pass

    def receive_from_server(self, player, request_type):
        # Placeholder for receiving data from server
        return "example_response"

# Instantiate and run the game
game = MurderMysteryGame()
game.game_loop()
