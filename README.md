# tulips_opac_new

- 筑波大学附属図書館 / 新着資料bot
- [@tulipsnewbooks](https://twitter.com/tulipsnewbooks)

## Format

- 書影があれば添付してツイート

```text
<date>の新着資料: <title>
著者: <author>
出版社: <publisher>
場所: <holding>
詳細情報: <link>
```

## Example

- https://twitter.com/tulipsnewbooks/status/1386931579600064513

```text
2021-04-27の新着資料: Relentlessly plain :…
著者: edited by Olivier P.…
出版社: Oxbow Books 2018
場所: 中央 227.5-N71 一般図書
詳細情報: https://tulips.tsukuba.ac.jp/opac/volume/3970653?current=9&total=73&trans_url=%2Fopac%2Fsearch%3Farrivedwithin%3D1%26count%3D100%26defaultpage%3D1%26defaulttarget%3Dlocal%26order%3Darrival_date_d%26searchmode%3Dcomplex%26type%255B%255D%3Dbook
```

## Setup

- Write auth keys of Twitter Developer API to: `.twitter.keys`
- Install require packages: `pip install -r requirements.txt`
- Dryrun: `./tulips-latest.py -d`
