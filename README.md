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
UTC time 2021-01-15T11:32:47.277752
   id    ratio      minted asset          collateral
----- -------- -----------------          -------------------
  575 1.566714   0.003804 mNFLX  based on     2.992764 uusd
                             owner terra10my55ndyhpr7ww4r7hh4wyepdpzlxck7tj63m8
  484 1.567068 205.068588 mUSO   based on 11466.000000 uusd
                             owner terra1a4395q65xl280z8fp9uzrtqkem5pe4wlqu7wcv
  115 1.592157   0.176031 mUSO   based on    10.000000 uusd
                             owner terra1x87fla7nuws8ugwmjlwy3v85zf6z2a3e4lhvzj
  485 1.592432 145.253279 mUSO   based on  8252.999000 uusd
                             owner terra1a4395q65xl280z8fp9uzrtqkem5pe4wlqu7wcv
  418 1.597302   0.739896 mTSLA  based on  1000.000000 uusd
                             owner terra1ldff05jhweptzyae32gmaxse2uufkl3l3qv028
  380 1.629095  23.261723 mGOOGL based on 65540.000000 uusd
                             owner terra168z3l70phnj7df32fd3cq76nsa4kecepjwv7l2
  428 1.631581   6.350548 mGOOGL based on 17919.997000 uusd
                             owner terra168z3l70phnj7df32fd3cq76nsa4kecepjwv7l2
  174 1.640343 285.541208 mUSO   based on 16712.000000 uusd
                             owner terra1x87fla7nuws8ugwmjlwy3v85zf6z2a3e4lhvzj
  570 1.694586 474.766177 mIAU   based on 14200.000000 uusd
                             owner terra1p73vkrdex2v63f4pdausg3gpknw686k03ed46n
  265 1.694702 936.094812 mIAU   based on 28000.000000 uusd
                             owner terra18xe32tuqrlkqkep5r3xprq8sp3ywaux9zmaedf
  661 1.697592 349.999999 mIAU   based on 10486.875000 uusd
                             owner terra1p73vkrdex2v63f4pdausg3gpknw686k03ed46n
% ./dangerous_cdps.py -h
usage: dangerous_cdps.py [-h] [-m MAXRATIO]

You can liquidate under-collateralized cdps
 by running `mirrorcli exec mint auction <id> <asset>`.

optional arguments:
  -h, --help            show this help message and exit
  -m MAXRATIO, --maxRatio MAXRATIO
                        list cdps under this threshold (default: 1.7)
```

