from process_single_client import main as process_single_client
import json
import os

class ClientManager:
    """
    This file enables argparse usage from the CLI. 
    The methods below allow for various functionality from the CLI. 
    """
    def __init__(self, filename='credentials.json') -> None:
        self.filename = filename
        self.clients_vault = '../vault/'
        self.clients = self.load_clients()

    def load_clients(self):
        try:
            os.makedirs(f'{self.clients_vault}', exist_ok=True)
            with open(f'{self.clients_vault}{self.filename}', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f'{self.clients_vault}{self.filename} not found.')
            return {}
        
    def save_clients(self): 
        with open(os.path.join(self.clients_vault, self.filename), 'w') as file: 
            json.dump(self.clients, file)

    def add_client(self, name):
        self.clients[name] = {}
        self.save_clients()

    def remove_client(self, name): 
        if name in self.clients:
            del self.clients[name]
            self.save_clients()

    def list_clients(self):
        print('Clients:')
        for name in self.clients:
            print(name)

    def run(self, name):
        process_single_client(name)