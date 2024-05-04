import schedule
import time

def job(task):
    schedule.every().monday.to().friday.at("07:15").do(task)
    schedule.every().monday.to().friday.at("19:15").do(task)

def run_scheduler(task):
    job(task)
        
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    from process_all_clients import main as process_clients_main
    run_scheduler(process_clients_main)