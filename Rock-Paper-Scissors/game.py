import random
import os.path as path
import sys


class RPS:
    
    def __init__(self, file_name='rating.txt'):
        self.game_rules = {'paper' : 0, 'rock' : 2, 'scissors' : 1}
        self.player_name = ''
        self.player_choice = ''
        self.player_rating = 0
        self.file_name = file_name

    def record_points(self):
        a_file = open(self.file_name, 'r+')
        list_of_lines = a_file.readlines()
        for line in list_of_lines:
            if self.player_name in line:
                line = f'{self.player_name} {self.player_rating}'
                a_file.writelines(list_of_lines)
                a_file.close()
    
    def read_ratings(self):
        players = {}
        if path.isfile(self.file_name):
            ratings = open(self.file_name, 'r+')
            for i in ratings:
                players[i.split()[0]] = i.split()[1]
            ratings.close()
        else:
            with open('rating.txt', 'w') as new:
                new.close()
        if not(self.player_name in players.keys()):
            self.player_rating = 0
        return players

    def new_game_rules(self, inp):
        if bool(inp) == True:
            inp = inp.replace(' ','').lower().split(',')
            self.game_rules = {option : i for i, option in enumerate(inp)}
        print("Okay, let's start!")

    def game_input_processor(self, input_type=None):
        if input_type == 'name':
            input_message = 'Enter your name:'
            inp = input(input_message).title()
            print('Hello, ' ,inp)
            self.player_name = inp
        elif input_type == 'game_variables':
            inp = input('Enter New Game Variables Seperates with Comma or Skip to Use Deafult: ')
            self.new_game_rules(inp)
        elif input_type == 'player_choice':
            inp = str(input()).lower()
            if inp == '!exit':
                print('Bye!')
                self.record_points()
                sys.exit(0)
            elif inp == '!rating':
                print(f'Your rating: {self.player_rating}')
            elif not(inp in list(self.game_rules.keys())):
                print('Invalid input')
            else:
                self.player_choice = inp
                self.game_rules_processor()
        return inp
    
    def game_rules_processor(self):
        cpu_choice = random.choice(list(self.game_rules.keys()))
        result = (self.game_rules[self.player_choice] - self.game_rules[cpu_choice]) % len(self.game_rules)
        if result == 0:
            print(f"There is a draw ({cpu_choice})")
            self.player_rating += 50
        elif result > len(self.game_rules) / 2:
            print(f"Sorry, but computer chose {cpu_choice}")
        else:
            print(f"Well done. Computer chose {cpu_choice} and failed")
            self.player_rating += 100
        
    def run_all(self):
        self.game_input_processor(input_type='name')
        self.read_ratings()
        self.game_input_processor(input_type='game_variables')
        while True:
            self.game_input_processor(input_type='player_choice')
            

if __name__ == '__main__':
    RPS().run_all()


    
