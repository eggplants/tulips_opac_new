# tulips_opac_new

[![Run Bot](https://github.com/eggplants/tulips_opac_new/actions/workflows/run.yml/badge.svg)](https://github.com/eggplants/tulips_opac_new/actions/workflows/run.yml)


- University of Tsukuba Library / New Arrival Twitter Bot
  - `筑波大学附属図書館 / 新着資料Bot`
  - [@tulipsnewbooks](https://twitter.com/tulipsnewbooks)

- Post Tweets daily with GitHub Actions

## Format

```text
✨{date}の新着資料✨
📖: {title<=70bytes}
👤: {author<=40bytes}
🏢: {publisher<=40bytes}
🏛️: {holding<=50bytes}
💬: {link}
```

- attach a book image if exists

## Example

```text
2021-04-27の新着資料
📖: Relentlessly plain : seventh millennium ceramics at Tell Sabi Abyad, Syria, : ha…
👤: edited by Olivier P. Nieuwenhuyse ; with…
🏢: Oxford ; Philadelphia : Oxbow Books, 201…
🏛️: 中央 227.5-N71 一般図書,中央 227.5-N71 一…
💬: https://tulips.tsukuba.ac.jp/opac/volume/3970653?current=9&total=73&trans_url=%2Fopac%2Fsearch%3Farrivedwithin%3D1%26count%3D100%26defaultpage%3D1%26defaulttarget%3Dlocal%26order%3Darrival_date_d%26searchmode%3Dcomplex%26type%255B%255D%3Dbook
```

## Setup

- Write auth keys of Twitter Developer API to: `.twitter.keys`
- Install require packages: `pip install -r requirements.txt`
- Dryrun: `./tulips-latest.py -d`
