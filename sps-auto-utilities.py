from beem import Hive
from beem.account import Account
import beemgraphenebase.ecdsasig
from binascii import hexlify
from datetime import datetime
from time import time
import requests
import sys
import yaml
from yaml.loader import SafeLoader

APP_NAME = 'sps-auto-utilities'

def stake(hive: Hive, hive_name: str, sps: float):
  # Stake SPS
  hive.custom_json("sm_stake_tokens", required_posting_auths=[hive_name],
                   json_data=f"{{\"token\":\"SPS\",\"qty\":{sps},\"app\":\"{APP_NAME}\"}}")

  # Log amount staked
  timestamp = datetime.now()
  print(f"{timestamp} | {hive_name} | Staked {sps}")

def claim_hive_sps_airdrop(hive_name: str, posting_key: str):
  # Login to Splinterlands to get token
  timestamp = int(time() * 1000)
  sig_bytes = beemgraphenebase.ecdsasig.sign_message(f"{hive_name}{timestamp}", posting_key)
  signature = hexlify(sig_bytes).decode("ascii")
  token = None
  try:
    login_response = requests.get(f"https://api2.splinterlands.com/players/login?name={hive_name}&ts={timestamp}"
                                  f"&sig={signature}").json()
    token = login_response['token']
  except:
    print(f"ERROR: Could not log in to Splinterlands for token with account {hive_name}",file=sys.stderr)
    return

  # Claim Airdrop
  try:
    claim_sig_bytes = beemgraphenebase.ecdsasig.sign_message(f"hive{hive_name}{timestamp}", posting_key)
    claim_signature = hexlify(claim_sig_bytes).decode("ascii")
    result = requests.get(f"https://ec-api.splinterlands.com/players/claim_sps_airdrop?platform=hive&address={hive_name}"
                 f"&sig={claim_signature}&token={token}&username={hive_name}&ts={timestamp}")
    if result.json()['success'] is True:
      print(f"{timestamp} | {hive_name} | Claimed SPS Airdrop from HIVE Assets", file=sys.stderr)

  except:
    print(f"ERROR: Could not claim HIVE SPS airdrop with account {hive_name}", file=sys.stderr)
    return

if len(sys.argv) != 2:
    print('ERROR: Invalid usage - please only supply exactly one config file path', file=sys.stderr)
    exit(1)
  
with open(sys.argv[1]) as config_file:
  config = yaml.load(config_file, Loader=SafeLoader)
  hive_node = config['hive-node']
  for account in config['accounts']:
    # Wallet Setup
    hive_name = account['name']
    keys = []
    has_active_key = False
    if 'posting-key' in account.keys():
      keys.append(account['posting-key'])
    if 'active-key' in account.keys():
      has_active_key = True
      keys.append(account['active-key'])

    if len(keys) == 0:
      print(f"ERROR: No keys for {hive_name}", file=sys.stderr)
      continue

    hive = Hive(keys=keys, node=hive_node)
    hive_account = Account(hive_name, blockchain_instance=hive)

    # Find how much SPS is liquid
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

    for action in account['actions']:
      if action == 'stake':
        stake(hive, hive_name, sps)
      elif action == 'claim-hive-sps-airdrop':
        claim_hive_sps_airdrop(hive_name, account['posting-key'])
      else:
        print(f"ERROR: Invalid action ({action}) supplied for {hive_name}", file=sys.stderr)

