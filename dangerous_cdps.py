#!/usr/bin/env python3

# TODO: discount calculation, unusual minimum collateral ratio

import argparse
from collections import namedtuple
import datetime
import json
import urllib.request

opt_parser = argparse.ArgumentParser(
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description = 'You can liquidate under-collateralized cdps\n'
                ' by running `mirrorcli exec mint auction <id> <asset>`.')
opt_parser.add_argument('-m', '--maxRatio', default = '1.7',
                        help = 'list cdps under this threshold (default: 1.7)')
opts = opt_parser.parse_args()

query = json.dumps({
  "query": '''query {
    cdps(maxRatio: %s) {
      id
      address
      token
      mintAmount
      collateralToken
      collateralAmount
      collateralRatio
    }
  }'''.replace('\n','') % opts.maxRatio
}).encode('utf-8')

with urllib.request.urlopen('https://whitelist.mirror.finance/columbus.json') as f:
  meta_infos = json.load(f)
token2symbol = {k: v['symbol'] for (k, v) in meta_infos['whitelist'].items()}

req = urllib.request.Request('https://graph.mirror.finance/graphql',
                             data = query,
                             headers = {'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as f:
  cdp_infos = json.load(f)

CDP = namedtuple('CDP', 'id address symbol mintAmount '
                          'collateralToken collateralAmount collateralRatio')
cdps = [CDP(id = x['id'],
            address = x['address'],
            symbol = token2symbol[x['token']],
            mintAmount = int(x['mintAmount']),
            collateralToken = x['collateralToken'],
            collateralAmount = int(x['collateralAmount']),
            collateralRatio = float(x['collateralRatio']))
         for x in cdp_infos['data']['cdps']]

cdps = sorted(cdps, key = lambda x: x.collateralRatio)

print('UTC time', datetime.datetime.utcnow().isoformat())
print('   id    ratio      minted asset          collateral')
print('----- -------- -----------------          -------------------')
for cdp in cdps:
  print('%5s %8.6f %10.6f %-6s based on %12.6f %-6s' % (
          cdp.id, cdp.collateralRatio, cdp.mintAmount / 1000000, cdp.symbol,
          cdp.collateralAmount / 1000000, cdp.collateralToken))
  print(' ' * 28, 'owner %s' % cdp.address)

