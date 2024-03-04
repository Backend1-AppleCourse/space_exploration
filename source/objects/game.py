

import json
import os
import random
import requests
from datetime import datetime

# local imports
from objects.space_ship import Spaceship

class SpaceGame:
    def _load_spaceship_data(self):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..','..', 'db', 'spaceship_data.json')

        with open(file_path) as file:
            data = json.load(file)

        return data

    def _load_events_data(self):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..','..', 'db', 'events_and_options.json')

        with open(file_path) as file:
            data = json.load(file)

        return data

    def __init__(self):
        spaceship_data = self._load_spaceship_data()
        self.space_ship = Spaceship(spaceship_data['name'], spaceship_data['fuel'], spaceship_data['health'], spaceship_data['credits'])
        self.events = self._load_events_data()

    def launch_spacecraft(self):
        print("Launching spacecraft")
        


    def explore_galaxy(self):
        print("Exploring galaxy")
        while True:
            event = random.choice(self.events)
            print(f"Encountering event: {event['name']}")
            if not self.handle_space_event(event):
                break
        

    def handle_space_event(self, event):
        print("Handling space event")
        print("Options: ")
        for index, option in enumerate(event['options']):
            print(f"{index + 1}. {option['name']}")
        user_input = int(input("Enter the option number: "))
        if user_input < 1 or user_input > len(event['options']):
            print("Invalid option number")
            return True
        option = event['options'][user_input - 1]
        print(f"Selected option: {option['name']}")

        self.space_ship.fuel += option['cost'] if option['consequence']=='fuel' else 0
        self.space_ship.health += option['cost'] if option['consequence']=='health' else 0
        self.space_ship.credit_points += option['cost'] if option['consequence']=='credits' else 0
        print(f"Updated fuel: {self.space_ship.fuel}")
        print(f"Updated health: {self.space_ship.health}")
        print(f"Updated credits: {self.space_ship.credit_points}")
        if self.space_ship.health <= 0 :
            print(f"spcaeship health has been fully compromised: {self.space_ship.health}")
            return False
        elif self.space_ship.fuel <= 0 :
            print(f"fuel tank has been emptied: {self.space_ship.fuel}")
            return False
        if input(f"Do you want to continue exploring? (y/n):") == "n":
            print("Back to game menu")
            return False
        return True
        


    def save_game(self):
        print("Saving game")
        def edit_json_value():
            try:
                current_dir = os.path.dirname(__file__)
                file_path = os.path.join(current_dir, '..','..', 'db', 'spaceship_data.json')
                with open(file_path, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                print(f"Error: The file {file_path} was not found.")
                return
            except json.JSONDecodeError:
                print(f"Error: The file {file_path} is not a valid JSON file.")
                return
            
            
            data['fuel'] = self.space_ship.fuel
            data['health'] = self.space_ship.health
            data['credits'] = self.space_ship.credit_points
                
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Updated spcae_ship.json.")

        edit_json_value()

    def fetch_weather(self):
        print("Fetching weather")
        def fetch_concise_space_weather_summary(date):
            api_url = 'https://api.nasa.gov/DONKI/notifications'
            params = {
                'startDate': date,
                'endDate': date,
                'api_key': 'DEMO_KEY'  # Use 'DEMO_KEY' or replace with your actual API key
            }
            
            try:
                response = requests.get(api_url, params=params)
                response.raise_for_status()  # Check for HTTP errors
                
                events = response.json()
                if events:
                    print(f"Space Weather Summary for {date}:")
                    for event in events[:1]:  # Limit to the first event for brevity
                        event_type = event.get('messageType', 'No event type specified')
                        start_time = event.get('messageIssueTime', 'No start time specified').split('T')[0]  # Just the date
                        
                        # Printing a concise summary
                        print(f"- An event of type '{event_type}' started on {start_time}.")
                else:
                    print(f"No space weather events found for {date}.")
            except requests.RequestException as e:
                print(f"Error fetching space weather data: {e}")

        # Example usage for today's date
        date = datetime.now().strftime('%Y-%m-%d')
        fetch_concise_space_weather_summary(date)

    def play_game(self):
        while True:
            print("Menu:")
            print("1. Launch spacecraft")
            print("2. Explore galaxy")
            print("3. Save game")
            print("4. Fetch weather")
            print("5. Exit game")
            user_input = int(input("Enter the option number: "))
            if user_input < 1 or user_input > 5:
                print("Invalid option number")
                continue
            if user_input == 1:
                self.launch_spacecraft()
            elif user_input == 2:
                self.explore_galaxy()
            elif user_input == 3:
                self.save_game()
            elif user_input == 4:
                self.fetch_weather()
            else:
                print("Exiting game")
                break
        