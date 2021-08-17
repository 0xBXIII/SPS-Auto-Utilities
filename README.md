# SPS Auto Utilities

## Overview

This is a simple Python script that checks the amount of liquid in-game SPS from the Splinterlands API and then stakes it. A HIVE account and its posting key are required to use this script, and are configured via the config file (a sample is included) in the same directory as the script. 

The Docker image (buildable via the included Dockerfile, currently not hosted anywhere) expects the config file to be in `/app/`.

A Docker Compose config file is included for convenience.

It is worth noting that there is an impact to your HIVE resource credits through the use of the script. You should monitor the impact which may vary depending on network conditions and your amount of resource credits.

Currently, only the `stake` action is supported and requires a minimum of the Posting Key for the HIVE account.

## Usage

The easiest way to get a fully running instance is to have Docker installed, clone this repo, modify the configuration file with your accounts, then start the Docker Compose stack (`docker compose up -d`) which will mount the config file and restart the container on system boot.

Editing the `sps-auto-cron` file allows for customizing the frequency of the script, the default is every 15 minutes.

## Functionality

### Stake

The `stake` action checks the amount of liquid in-game SPS for a user's account and stakes the amount. As a result of this action, any claimable SPS is then claimed and will be in the liquid in-game balance. At a minimum, account's Posting Key is required for this action. This effectively allows auto compounding of the staked SPS.

## Limitations
This script is provided without warranty and may not work in all system configurations. A reliance on the Splinterlands API is needed to check the stakeable amount, and the script may not be able to function if the game is in maintenance mode. 

## Feedback / Contacts
Feel free to submit any feedback/feature requests/bugs via Github or to contact me on HIVE via @fwxiii account, or on Twitter @0x_BXIII.

## Donations
If this script is useful to you, or you want to support further development of this and/or future tools, please consider donating to any of the following accounts:

WAX: 5lsay.wam

HIVE: fwxiii