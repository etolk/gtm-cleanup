# GTM Clean Up Tool

## Overview

This tool is designed to clean up all triggers and variables in Google Tag Manager that don't have any dependencies, as well as paused tags, to maintain a clean container environment. It builds upon the excellent work done in the [gtm-gear project](https://github.com/ArtemKorneevGA/gtm-gear). Special thanks to [Artem Korneev](https://www.linkedin.com/in/artem-korneev/).

## Pre-requirements

- A Google Cloud Platform (GCP) account with the Tag Manager API activated. Activate it [here](https://console.cloud.google.com/apis/library/tagmanager.googleapis.com).

## Installation

To get a local copy up and running, follow these steps:

### Set Up Virtual Environment

1. **Create a Virtual Environment:**

    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment:**

    ```bash
    source .venv/bin/activate
    ```

### Install Dependencies

- **Install the gtm-gear module:**

    ```bash
    pip install -r requirements.txt
    ```

### OAuth Configuration

- **Get client secret using OAuth 2.0 client ID method:**

    Follow the steps from the [Google Cloud documentation](https://support.google.com/cloud/answer/6158849?hl=en). Download the JSON credentials and rename it to `client_secrets.json`.

- **Set path to credentials:**

    In `config.py`, set the path to the folder containing `client_secrets.json` and `tagmanager.dat`.

    ```python
    os.environ["GTM_API_CONFIG_FOLDER"] = 'path'
    ```

- **Execute `authorization.py` to grant access:**

    This will generate a `tagmanager.dat` file necessary for authentication.

## Usage

- Modify `config.py` and change all necessary variables.
- Run the following command:

    ```bash
    python main.py
    ```

