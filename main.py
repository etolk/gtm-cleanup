import os
from gtm_gear import Service, Container, Workspace
from helpers import delete_unused_triggers, delete_unused_variables
from config import config


# Set the GTM API config folder environment variable
os.environ["GTM_API_CONFIG_FOLDER"] = config["GTM_API_CONFIG_FOLDER"]

# Retrieve settings from configuration
delete_paused_tags = config["delete_paused_tags"]
workspace_name = config["workspace_name"]
requests_per_minute = config["requests_per_minute"]

# Initialize the GTM service
service = Service()
service.set_ratelimit(requests_per_minute, 60)

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


def main():
    accounts_list = get_accounts_list()
    for account_id in accounts_list:
        process_containers(account_id)

# Run the main function
if __name__ == "__main__":
    main()