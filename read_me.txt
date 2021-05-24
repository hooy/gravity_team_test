Developers task:

There are two tasks prepared. Data should be sourced from binance api which is largest crypto exchange in the world.
API documentation found here: https://binance-docs.github.io/apidocs/spot/en/#change-log

Script for first task is in task1 folder. Goal of the task is to improve code to continuously print highest bid and
lowest ask price for pair BTC/USDT.
1. Use type hints where possible
2. Use web socket to gather information
3. Use asynchronous programming
4. Print highest bid and lowest ask and time when we received them.

Second task is to use this api key and continuously print out balances on account holding following keys.
*Pease write code in task2 folder:
API Key: 9QC75c7IzdwU1w23EMPMIB4X1JCFf5v3VDSArXXmc8jSIHyuGbbxyoLpaLviMs39
Secret Key: OQ8JbgsHNd4Nq8MmLIHfsPkzQWgUajLwwSV4w3cD59EG72diAlLdTCkv1mrG6Maw
1. Use asynchronous programming.
2. Use rest api.
3. Print latency between local machine and exchange on each iteration.
4. Request balance data as frequently as possible without getting banned.
5. Try to minimize cpu time.
6. Print out time and balances of coins that we own. Do this every time we receive balances from binance.
