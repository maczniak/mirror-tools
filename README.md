# mirror-tools
educational Mirror Protocol utilities

These are for educational purposes only. We cannot guarantee correctness and
accuracy of these tools!

```
% ./best_performance_massets.py
UTC time 2021-01-15T11:31:55.310889
symbol  total = trade + stake
------ ------   -----   ------
 mVIXY 221.29 =  3.59 + 217.70
  mUSO 218.29 = 10.69 + 207.60
 mNFLX 215.68 =  7.82 + 207.87
 mTWTR 206.69 =  3.56 + 203.13
mGOOGL 200.68 =  2.56 + 198.12
 mBABA 200.54 =  1.40 + 199.14
  mSLV 200.01 = 12.58 + 187.43
 mMSFT 197.97 =  2.99 + 194.98
 mAMZN 196.85 =  2.53 + 194.32
  mQQQ 186.56 =  9.12 + 177.44
 mTSLA 183.98 =  0.11 + 183.86
  mIAU 179.43 =  1.44 + 177.99
 mAAPL 164.93 =  2.77 + 162.16
   MIR 157.13 =  3.70 + 153.43
% ./best_performance_massets.py -h

usage: best_performance_massets.py [-h] [--terra | --eth | --combine]

optional arguments:
  -h, --help  show this help message and exit
  --terra     collect Terra network only (default)
  --eth       collect Ethereum network only (stake reward is meaningless)
  --combine   collect both Terra network and Ethereum network
```

```
% ./dangerous_cdps.py
UTC time 2021-01-16T10:42:21.514336
   id    ratio      minted asset          collateral
----- -------- -----------------          -------------------
  575 1.582980   0.003804 mNFLX  based on     2.992764 uusd
                             when  497.00 →  524.49 uusd   ( 5.5%)
                             owner terra10my55ndyhpr7ww4r7hh4wyepdpzlxck7tj63m8
  484 1.585284 205.068588 mUSO   based on 11466.000000 uusd
                             when   35.27 →   37.28 uusd   ( 5.7%)
                             owner terra1a4395q65xl280z8fp9uzrtqkem5pe4wlqu7wcv
  115 1.610665   0.176031 mUSO   based on    10.000000 uusd
                             when   35.27 →   37.87 uusd   ( 7.4%)
                             owner terra1x87fla7nuws8ugwmjlwy3v85zf6z2a3e4lhvzj
  485 1.610943 145.253279 mUSO   based on  8252.999000 uusd
                             when   35.27 →   37.88 uusd   ( 7.4%)
                             owner terra1a4395q65xl280z8fp9uzrtqkem5pe4wlqu7wcv
  380 1.632389  23.261723 mGOOGL based on 65540.000000 uusd
                             when 1726.00 → 1878.34 uusd   ( 8.8%)
                             owner terra168z3l70phnj7df32fd3cq76nsa4kecepjwv7l2
  428 1.634880   6.350548 mGOOGL based on 17919.997000 uusd
                             when 1726.00 → 1881.20 uusd   ( 9.0%)
                             owner terra168z3l70phnj7df32fd3cq76nsa4kecepjwv7l2
  418 1.640658   0.739896 mTSLA  based on  1000.000000 uusd
                             when  823.78 →  901.03 uusd   ( 9.4%)
                             owner terra1ldff05jhweptzyae32gmaxse2uufkl3l3qv028
  174 1.659411 285.541208 mUSO   based on 16712.000000 uusd
                             when   35.27 →   39.02 uusd   (10.6%)
                             owner terra1x87fla7nuws8ugwmjlwy3v85zf6z2a3e4lhvzj
% ./dangerous_cdps.py -h
usage: dangerous_cdps.py [-h] [-m MAXRATIO | --maxRise MAXRISE]

You can liquidate under-collateralized CDPs
 by running `mirrorcli exec mint auction <id> <asset>`.

optional arguments:
  -h, --help            show this help message and exit
  -m MAXRATIO, --maxRatio MAXRATIO
                        list CDPs under this ratio threshold (default: 1.7)
  --maxRise MAXRISE     list CDPs under this percent threshold
```

