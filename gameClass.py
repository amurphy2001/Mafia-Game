'''
gameClass.py
Description:
    This file contains the GameClass, which manages the primary gameplay mechanics for Mafia. 
    The GameClass includes methods for the day phase (voting phase), where players vote to 
    eliminate others, and the night phase, where actions specific to player roles occur. 
    It interacts with the Player class to handle individual player attributes and behaviors.
'''

from player import Player
import os

class GameClass:
    def __init__(self, players):
        self.num_players = players # Total number of players in the game
        self.num_mafia = 0 # Counter for mafia players
        self.num_doctors = 0 # Counter for doctor players
        self.num_villagers = 0 # Counter for villager players
        self.gameCompleted = False # Boolean value to indicate if the game has ended
        self.player_list = [] # List to store player objects

    # Method to add a new player to the game
    def add_player(self):
        # Prompt the user to enter the player's name and store it in lowercase
        player_name = input("Enter player name:").lower()
        print("\n")  # Print a new line
        
        # Prompt the user to assign a role to the player (mafia, villager, doctor)
        player_role = input("Enter role(mafia, villager, doctor):").lower()
        print("\n")  # Print a new line

        # Add the player as a Player, with a role and name
        self.player_list.append(Player(player_role, player_name))

        # Update the count of each role based on the player's assigned role
        if player_role == "mafia":
            self.num_mafia += 1  
        elif player_role == "doctor":
            self.num_doctors += 1  
        else:
            self.num_villagers += 1 

    def day_phase(self):
        # Initialize a dictionary to store vote counts for each player
        votes = {}
        
        # Start the day phase with a prompt for players to vote
        print("Day Phase: Time to vote!")
        # Halt execution until the user presses any key to continue
        input("Press any key to continue...")
        # Loop through each player in the game
        for player in self.player_list:
            # Check if the player is alive. Only alive players can vote
            if player.status == "alive":
                # Display the voting player's name
                print(f"\n{player.name} is voting...")
                # Generate a list of names of alive players except the current player
                alive_players = [p.name for p in self.player_list if p.status == "alive" and p.name != player.name]
                # Display alive players
                print("Players available to vote for:", ', '.join(alive_players)) 
                # Prompt the player to enter the name of the player they want to eliminate
                vote_for = input(f"{player.name}, who do you vote to eliminate? ")
                vote_for = vote_for.lower()  # Convert input to lowercase for consistency
                
                # Ensure the player does not vote for themselves
                if vote_for == player.name:
                    print("You cannot vote for yourself. Skipping vote.")  # Display message for invalid self-vote
                    continue  # Skip to the next player if they voted for themselves
                
                # Find the player who matches the voted name and is alive
                voted_player = next((p for p in self.player_list if p.name == vote_for and p.status == "alive"), None)
                
                # If the voted player is found and alive, record the vote
                if voted_player:
                    # Increment the vote count for the selected player
                    votes[vote_for] = votes.get(vote_for, 0) + 1
                else:
                    # Display a message if the vote was invalid (player not found or dead)
                    print(f"{vote_for} is either not found or not alive. Vote is skipped.")
            # Clear the console after each vote to keep input secret
            self.clear_console()  
        
        # Check if there are any votes recorded (skip if no one voted or votes were invalid)
        if votes:
            # Find the player with the most votes
            max_votes_player = max(votes, key=votes.get)
            
            # Retrieve the actual player object of the player with the most votes
            eliminated_player = next((p for p in self.player_list if p.name == max_votes_player), None)
            
            # If the player is found, update their status to "dead"
            if eliminated_player:
                eliminated_player.status = "dead"  # Set the player's status to dead
                print(f"{eliminated_player.name} has been eliminated.")  # Display elimination message
                
                # Adjust the player count for the eliminated player's role
                if eliminated_player.role == "mafia":
                    self.num_mafia -= 1  # Decrease mafia count if a mafia member is eliminated
                elif eliminated_player.role == "doctor":
                    self.num_doctors -= 1  # Decrease doctor count if a doctor is eliminated
                else:
                    self.num_villagers -= 1  # Decrease villager count if a villager is eliminated
        
        # Check win conditions after the voting phase
        self.check_win_conditions()

    def night_phase(self):

        #mafia choose someone to kill (maybe more than 1 for more players/mafia)

        #doctors choose someone to protect

        #villagers do nothing

        #dead players do not interact


       # Check win conditions after the voting phase
        self.check_win_conditions()

    def check_win_conditions(self):
        # Check if the village wins (all mafia members are eliminated)
        if self.num_mafia == 0:
            # Set the game completion flag to true, ending the game loop
            self.gameCompleted = True
            # Display the victory message for the village
            print("Village Wins!")

        # Check if the mafia wins (mafia outnumber or equal the villagers and doctors)
        elif self.num_mafia >= (self.num_villagers + self.num_doctors):
            # Set the game completion flag to true, ending the game loop
            self.gameCompleted = True
            # Display the victory message for the mafia
            print("Mafia wins!")

    def clear_console(self):
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For MacOS and Linux
        else:
            os.system('clear')







