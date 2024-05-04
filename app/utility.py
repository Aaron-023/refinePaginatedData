import argparse
from client_manager import ClientManager

def parse():
    """
    Argparse enables CLI from the CLI.
    """
    parser = argparse.ArgumentParser(description='Manage clients')
    parser.add_argument('action', choices=['add', 'remove', 'list', 'run'], help='Action to perform')
    parser.add_argument('--name', help='Name of the client (required for add/remove)')
    args = parser.parse_args()

    manager = ClientManager()

    if args.action == 'add':
        if args.name:
            manager.add_client(args.name)
            print(f'{args.name} has been added.')
        else:
            print('Name is required for "add" action.')


    elif args.action == 'remove':
        if args.name:
            manager.remove_client(args.name)
            print(f'{args.name} has been removed.')
        else:
            print('Name is required for "remove" action.')


    elif args.action == 'run':
        if args.name:
            print(f'Running "{args.name}"...')
            manager.run(args.name)
            print('Run complete')

        

    elif args.action == 'list':
            manager.list_clients()

if __name__ == "__main__":
    parse()