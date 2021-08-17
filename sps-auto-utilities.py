from beem import Hive
from beem.account import Account
from datetime import datetime
import requests
import sys
import yaml
from yaml.loader import SafeLoader

APP_NAME = 'sps-auto-utilities'

if len(sys.argv) != 2:
    print('ERROR: Invalid usage - please only supply exactly one config file path', file=sys.stderr)
    exit(1)
  
with open(sys.argv[1]) as config_file:
  config = yaml.load(config_file, Loader=SafeLoader)
  hive_node = config['hive-node']
  for account in config['accounts']:
    # Wallet Setup
    hive_name = account['name']
    hive = Hive(keys=[account['posting-key']], node=hive_node)
    hive_account = Account(hive_name, blockchain_instance=hive)

    # Find how much SPS is claimable
    # This does NOT include airdrops
    balances = []
    try:
      balances = requests.get(f'https://api.splinterlands.io/players/balances?username={hive_name}').json()
    except:
      print(f"ERROR: Could not fetch Splinterlands balances for {hive_name}", file=sys.stderr)
      continue
    sps = 0 # Defaulting to 0 to claim only
    for balance in balances:
      if balance['token'] == 'SPS':
        sps = balance['balance']
        break

    if account['action'] is None or account['action'] == 'stake':
      # Execute transaction
      hive.custom_json("sm_stake_tokens", required_posting_auths=[hive_name],
                        json_data=f"{{\"token\":\"SPS\",\"qty\":{sps},\"app\":\"{APP_NAME}\"}}")

      # Log amount staked
      timestamp = datetime.now()
      print(str(timestamp) + ' | ' + hive_name + ' | Staked ' + str(sps))

    else:
      print(f"ERROR: Invalid action supplied for {hive_name}", file=sys.stderr)