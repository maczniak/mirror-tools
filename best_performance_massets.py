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

def make_request(url, query):
  if query:
    query = query.encode('utf-8')
  return urllib.request.Request(url,
                                data = query,
                                headers = {
                                  'Content-Type': 'application/json',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
                                })

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
})

#now = time.gmtime()
#seconds_since_midnight = now.tm_hour * 60 * 60 + now.tm_min * 60 + now.tm_sec
#volume_fraction = seconds_since_midnight / (24 * 60 * 60)
volume_fraction = 1

with urllib.request.urlopen(make_request('https://whitelist.mirror.finance/columbus.json', None)) as f:
  meta_infos = json.load(f)
token2symbol = {k: v['symbol'] for (k, v) in meta_infos['whitelist'].items()}

req = make_request('https://graph.mirror.finance/graphql', query)
with urllib.request.urlopen(req) as f:
  masset_infos = json.load(f)

Masset = namedtuple('Masset', 'symbol liquidity volume apr')
massets = [Masset(symbol = token2symbol[x['token']],
                  liquidity = int(x['statistic']['liquidity']),
                  volume =    int(x['statistic']['volume']),
                  apr =     float(x['statistic']['apr']))
            for x in masset_infos['data']['assets']
            if x['token'] in token2symbol]

def masset_perf_comparator(masset):
  # trading commission + lp stake reward
  return masset.volume / volume_fraction * 0.003 / masset.liquidity * 365 + masset.apr

massets = sorted(massets, key = masset_perf_comparator, reverse = True)

print('UTC time', datetime.datetime.utcnow().isoformat())
print('symbol  total =  trade + stake')
print('------ ------   ------   ------')
for masset in massets:
  # trading commission (as percentage)
  tc = masset.volume / volume_fraction * 0.003 / masset.liquidity * 365 * 100
  # lp stake reward (as percentage)
  ls = masset.apr * 100
  print('%6s %6.2f = %6.2f + %6.2f' % (masset.symbol, tc + ls, tc, ls))

