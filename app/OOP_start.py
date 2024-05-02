from OOP_config import Client 

def main():
    frasers_group = Client('FrasersGroup') #instance creation of the client class
    rank_group = Client('TheRankGroup') #instance creation of the client class
    accor_hotels = Client('AccorHotel') #instance creation of the client class
    wsh_group = Client('WSHGroup') #instance creation of the client class
    rogue_group = Client('RogueGroup') #instance creation of the client class

    clients = [frasers_group, rank_group, accor_hotels, wsh_group]

    for client in clients:
        # client.save(
        #     client.process_data(
        #         client.refine_endpoint_data(
        #             client.get_endpoint_url(

        #             )
        #         )
        #     )
        # )
        print(client)

if __name__ == "__main__":
    main()