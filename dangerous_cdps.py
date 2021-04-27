#!/usr/bin/env python3

# TODO: discount calculation, sort according to minimum collateral ratio
# TODO: mAsset collateral in uusd

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
    cdps(maxRatio: %s) {
      id
      address
      token
      mintAmount
      collateralToken
      collateralAmount
      collateralRatio
    }
  }'''.replace('\n', '') % maxRatio
})

with urllib.request.urlopen(make_request('https://whitelist.mirror.finance/columbus.json', None)) as f:
  meta_infos = json.load(f)
token2symbol = {k: v['symbol'] for (k, v) in meta_infos['whitelist'].items()}

mir_token = [k for (k, v) in token2symbol.items() if v == 'MIR'][0]

min_col_rate_query = '{"query":"{' + ''.join(["""
  %s: WasmContractsContractAddressStore(
    ContractAddress: \\\"terra1wfz7h3aqf4cjmjcvc6s8lxdhh7k30nkczyf0mj\\\"
    QueryMsg: \\\"{\\\\\\\"asset_config\\\\\\\":{\\\\\\\"asset_token\\\\\\\":\\\\\\\"%s\\\\\\\"}}\\\"
  ) {
    Result
  }
""" % (k, k) for k in set(token2symbol) if k != mir_token]).replace('\n', '') + '}"}'

req = make_request('https://mantle.terra.dev/', min_col_rate_query)
with urllib.request.urlopen(req) as f:
  min_col_rate_response = json.load(f)
token2min_col_rate = {k: float(json.loads(v['Result'])['min_collateral_ratio'])
                      for (k, v)
                      in min_col_rate_response['data'].items()}

req = make_request('https://graph.mirror.finance/graphql', query)
with urllib.request.urlopen(req) as f:
  cdp_infos = json.load(f)

CDP = namedtuple('CDP', 'id address symbol token mintAmount '
                          'collateralToken collateralAmount collateralRatio')
cdps = [CDP(id = x['id'],
            address = x['address'],
            token = x['token'],
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
  min_col_rate = token2min_col_rate[cdp.token]
  collateralToken = token2symbol[cdp.collateralToken] \
    if cdp.collateralToken != 'uusd' else cdp.collateralToken
  print('%5s %8.6f %10.6f %-6s based on %12.6f %-6s' % (
          cdp.id, cdp.collateralRatio, cdp.mintAmount / 1000000, cdp.symbol,
          cdp.collateralAmount / 1000000, collateralToken))
  if cdp.collateralRatio >= min_col_rate:
    print(' ' * 28, 'when %7.2f → %7.2f %-6s (%4.1f%%)' % (
            cdp.collateralAmount / cdp.mintAmount / cdp.collateralRatio,
            cdp.collateralAmount / cdp.mintAmount / min_col_rate, collateralToken,
            (cdp.collateralRatio - min_col_rate) / min_col_rate * 100))
  else:
    # mAsset amount / 0.8 * mAsset price / collateral price
    print(' ' * 28, 'can be margin called')
  print(' ' * 28, 'owner %s' % cdp.address)

