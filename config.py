config = {
    "GTM_API_CONFIG_FOLDER": "/path-to-client-secrets-json-file", # Path to client-secrets.json file excluding file name itself 
    "account_ids": ["1234567890"], # Use ["all"] for all accounts
    "containers_list": ["GTM-AAAAAAA"], # Use ["all"] for all containers in account
    "delete_paused_tags": False, # Use True if you want to also delete the paused Tags
    "workspace_name": "Clean up GTM container"
}