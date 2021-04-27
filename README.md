# tulips_opac_new

- 筑波大学附属図書館新刊情報bot
- [@tulipsnewbooks](https://twitter.com/tulipsnewbooks)

## Format

```text
<date>の新刊: <title>(<author>)
場所: <holding>(<status>)
詳細情報: <link>
```

## Example

- https://twitter.com/tulipsnewbooks/status/1386856533690966018

```text
2021-04-27の新刊: The desert Fayum, Plates(G. Caton-Thompson and E. W. Gardner, Royal Anthropological Institute of Great Britain & Ireland 1934)
場所: 中央 242-C26 一般図書(配架済)
詳細情報: https://tulips.tsukuba.ac.jp/opac/volume/3970705?current=1&total=73&trans_url=%2Fopac%2Fsearch%3Farrivedwithin%3D1%26count%3D100%26defaultpage%3D1%26defaulttarget%3Dlocal%26order%3Darrival_date_d%26searchmode%3Dcomplex%26type%255B%255D%3Dbook
```

## Setup

- Write auth keys of Twitter Developer API to: `.twitter.keys`
- Install require packages: `pip install -r requirements.txt`
- Dryrun: `./tulips-latest.py -d`
