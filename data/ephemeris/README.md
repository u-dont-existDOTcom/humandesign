# Ephemeris data

Production chart runs require local Swiss Ephemeris files. They are intentionally not bundled here. The tested 1950–2020 benchmark files came from the official `aloistr/swisseph` repository at commit `3fd0f956d73898b91cc4f67cf18b21af656d1342`; expected hashes are in `manifest.json`.

Download into an external/local cache and verify before use:

```bash
mkdir -p /tmp/hdmatch-ephe
curl -L --fail --output /tmp/hdmatch-ephe/sepl_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/3fd0f956d73898b91cc4f67cf18b21af656d1342/ephe/sepl_18.se1
curl -L --fail --output /tmp/hdmatch-ephe/semo_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/3fd0f956d73898b91cc4f67cf18b21af656d1342/ephe/semo_18.se1
python scripts/verify_ephemeris.py --dir /tmp/hdmatch-ephe
```

Swiss Ephemeris is dual-licensed under the AGPL or a professional license. Confirm license compatibility before distribution or public service operation.
