#!/usr/bin/env python3

# TODO: discount calculation, unusual minimum collateral ratio

import argparse
from collections import namedtuple
import datetime
import json
import urllib.request

opt_parser = argparse.ArgumentParser(
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description = 'You can liquidate under-collateralized CDPs\n'
                ' by running `mirrorcli exec mint auction <id> <asset>`.')
opt_group = opt_parser.add_mutually_exclusive_group()
opt_group.add_argument('-m', '--maxRatio', default = '1.7',
                   help = 'list CDPs under this ratio threshold (default: 1.7)')
opt_group.add_argument('--maxRise',
                       help = 'list CDPs under this percent threshold')
opts = opt_parser.parse_args()
maxRatio = float(opts.maxRise) * 1.5 / 100 + 1.5 if opts.maxRise \
                                                 else opts.maxRatio 

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
  }'''.replace('\n','') % maxRatio
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
  print(' ' * 28, 'when %7.2f → %7.2f %-6s (%4.1f%%)' % (
          cdp.collateralAmount / cdp.mintAmount / cdp.collateralRatio,
          cdp.collateralAmount / cdp.mintAmount / 1.5, cdp.collateralToken,
          (cdp.collateralRatio - 1.5) / 1.5 * 100))
  print(' ' * 28, 'owner %s' % cdp.address)

