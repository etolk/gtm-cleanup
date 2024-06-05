import os
from ratelimit import limits, sleep_and_retry
from gtm_gear import Service, Container, Workspace
from helpers import delete_unused_triggers, delete_unused_variables
import time
from config import config

# Rate limit settings
CALLS = 15
PERIOD = 60

# Set the GTM API config folder environment variable
os.environ["GTM_API_CONFIG_FOLDER"] = config["GTM_API_CONFIG_FOLDER"]

# Initialize the GTM service
service = Service()

# Retrieve settings from configuration
delete_paused_tags = config["delete_paused_tags"]
workspace_name = config["workspace_name"]

# Get the list of accounts
def get_accounts_list():
    if "all" in config["account_ids"]:
        return [a['accountId'] for a in service.get_accounts()['account']]
    return config["account_ids"]

# Get the list of containers for a given account
def get_containers_list(account_id):
    if "all" in config["containers_list"]:
        return [c['publicId'] for c in service.get_containers(account_id)['container']]
    return config["containers_list"]

# Process each container
def process_container(account_id, container):
    print("-" * 30)
    print(f'Account: {account_id}, Container: {container}')
    source_container = Container(service, account_id, container)
    
    # Create workspace if it does not exist
    if not source_container.get_workspace_by_name(workspace_name):
        source_container.create_workspace(workspace_name)
        
    source_workspace = Workspace(source_container, workspace_name)
    
    # Optionally delete paused tags
    if delete_paused_tags:
        print("Delete paused tags")
        for tag in [tag for tag in source_workspace.tags if tag.isPaused()]:
            tag.delete()
            print(f"Deleted tag: {tag.name}")
        print("Delete paused tags DONE")
        
    # Delete unused triggers and variables
    print("Deleting unused triggers")
    delete_unused_triggers(source_workspace)
    print("Deleting unused triggers DONE")
    print("Deleting unused variables")
    delete_unused_variables(source_workspace)
    print("Deleting unused variables DONE")

# Process containers for a given account
def process_containers(account_id):
    containers_list = get_containers_list(account_id)
    for container in containers_list:
        process_container(account_id, container)
        print(f'Account: {account_id}, Container: {container} - Cleanup DONE')
        time.sleep(60)

@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def main():
    accounts_list = get_accounts_list()
    for account_id in accounts_list:
        process_containers(account_id)
        time.sleep(60)

# Run the main function
if __name__ == "__main__":
    main()