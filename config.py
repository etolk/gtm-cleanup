config = {
    "GTM_API_CONFIG_FOLDER": "/path-to-gtm-api-config-folder", # Path to gtm config file (tagmanager.dat) excluding file name itself
    "account_ids": ["111111111"], # Use ["all"] for all accounts
    "containers_list": ["GTM-123456"], # Use ["all"] for all containers in account
    "include_paused_tags": False, # Use True if you want to also delete the paused Tags
    "include_expired_tags": False, # Use True if you want to also delete the Tags with expired firing schedule
    "workspace_name": "Clean up GTM container", # Workspace name. Change if needed
    "requests_per_minute": 15 # Number of requests per minute. Update this value if the quota limit has been increased
}