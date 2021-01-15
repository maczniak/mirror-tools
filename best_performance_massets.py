#!/usr/bin/env python3

# TODO: Uniswap LP staking reward

import argparse
from collections import namedtuple
import datetime
import json
import time
import urllib.request

opt_parser = argparse.ArgumentParser()
opt_group = opt_parser.add_mutually_exclusive_group()
opt_group.add_argument('--terra', dest = 'network',
                       action = 'store_const', const = 'TERRA',
                       help = 'collect Terra network only (default)')
opt_group.add_argument('--eth', dest = 'network',
                       action = 'store_const', const = 'ETH',
           help = 'collect Ethereum network only (stake reward is meaningless)')
opt_group.add_argument('--combine', dest = 'network',
                       action = 'store_const', const = 'COMBINE',
                       help = 'collect both Terra network and Ethereum network')
opts = opt_parser.parse_args()
network = opts.network if opts.network else 'TERRA'

query = json.dumps({
  "query": '''query {
    assets {
      token
      statistic {
        liquidity(network: %s)
        volume(network: %s)
        apr
      }
    }
  }'''.replace('\n','') % (network, network)
}).encode('utf-8')

now = time.gmtime()
seconds_since_midnight = now.tm_hour * 60 * 60 + now.tm_min * 60 + now.tm_sec
volume_fraction = seconds_since_midnight / (24 * 60 * 60)

with urllib.request.urlopen('https://whitelist.mirror.finance/columbus.json') as f:
  meta_infos = json.load(f)
token2symbol = {k: v['symbol'] for (k, v) in meta_infos['whitelist'].items()}

req = urllib.request.Request('https://graph.mirror.finance/graphql',
                             data = query,
                             headers = {'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as f:
  masset_infos = json.load(f)

Masset = namedtuple('Masset', 'symbol liquidity volume apr')
massets = [Masset(symbol = token2symbol[x['token']],
                  liquidity = int(x['statistic']['liquidity']),
                  volume =    int(x['statistic']['volume']),
                  apr =     float(x['statistic']['apr']))
            for x in masset_infos['data']['assets']]

def masset_perf_comparator(masset):
  # trading commission + lp stake reward
  return masset.volume / volume_fraction * 0.003 / masset.liquidity * 365 + masset.apr

massets = sorted(massets, key = masset_perf_comparator, reverse = True)

print('UTC time', datetime.datetime.utcnow().isoformat())
print('symbol  total = trade + stake')
print('------ ------   -----   ------')
for masset in massets:
  # trading commission (as percentage)
  tc = masset.volume / volume_fraction * 0.003 / masset.liquidity * 365 * 100
  # lp stake reward (as percentage)
  ls = masset.apr * 100
  print('%6s %6.2f = %5.2f + %6.2f' % (masset.symbol, tc + ls, tc, ls))

