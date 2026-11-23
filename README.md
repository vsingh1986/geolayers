# GEOlayers 3 — UPSC geography catalog

A GitHub-hosted catalog of **small, named GeoJSON features** for the native **GEOlayers 3 GitHub Browser** in Adobe After Effects.

## What this project supports

- Open this repository **inside GEOlayers** through the documented `geolayers3.githubBrowser()` scripting interface.
- Find named GeoJSON files using GitHub Browser's filter, and import selected files into GEOlayers' **Feature Browser**.
- After importing, find the loaded features using the **Feature Browser** filter or the upper Search box (with the Feature Browser search source enabled).
- Draw and animate points, lines and polygons through GEOlayers as usual.

**Important:** This does **not** make the main GEOlayers Search field query all as-yet-unimported GitHub features. File discovery happens in the native GitHub Browser; GEOlayers' built-in search finds *loaded* features. A repository is not a live GIS database or a GeoJSON search API.

## Quick start in After Effects

1. Download [UPSC_GitHub_Browser.jsx](geolayers-scripts/UPSC_GitHub_Browser.jsx).
2. Copy it to the GEOlayers 3 scripts directory. Your preferences showed:
   `C:\Users\vivek\AppData\Roaming\aescripts\GEOlayers3\scripts`
3. Open the GEOlayers 3 panel. Run the script from GEOlayers' script list/menu. You may need to refresh or reopen the panel to detect it.
4. The script opens this GitHub repository inside GEOlayers. In its GitHub Browser, filter for `Demo`, select a demo `.geojson` and choose **Import to GEOlayers**.
5. The imported entry appears in the Feature Browser. Select/draw it in a Mapcomp. Enable **Preferences > Feature Search > Feature Browser** to search *loaded* entries from the upper search bar.

## Preparing your own large GeoJSON files

For massive `.geojson` files that GEOlayers rejects with **File is too large**, do not upload the original files. First create *individual named features* with `tools/split_geojson.py`. This tool uses a streaming parser so the whole input file need not be held in memory. It preserves coordinates and properties and **does not simplify geometries**.

From Windows PowerShell, with Python 3 installed:

```powershell
py -m pip install -r requirements.txt
py tools\split_geojson.py --input "F:\Your GIS Folder\Coal.geojson" --category Coal --name-field name --max-features 100 --output data
```

Repeat for `WorldRiver.geojson` with `--category Rivers`, or `WorldLandforms.geojson` with `--category Landforms`.

Optional: `--contains Ganga` exports names matching *Ganga*, and `--start-after 100` resumes from the input feature position after a prior batch. Source GeoJSON is expected to be a standard **FeatureCollection in WGS84 EPSG:4326**.

Publish only the resulting small `data/.../*.geojson` files. The default maximum size is 1.5 MiB *per resulting feature*. Very complex individual geometries are skipped and recorded in `reports/` for review, not silently simplified. Do not bulk-publish thousands of files until you've tested GitHub Browser's performance and limits.

## Catalog layout

```
data/
  Demo/             # synthetic point examples for a connection test
  Rivers/           # to be generated from your original data
  Landforms/
  Coal/
geolayers-scripts/
  UPSC_GitHub_Browser.jsx
tools/
  split_geojson.py
requirements.txt
```

This public repository contains only fictional demo points until you add your own data. **Check licensing before publishing source GIS information.** Do not upload original large MBTiles/PMTiles or private datasets.

## Official references

- [GEOlayers 3 scripting API and githubBrowser](https://github.com/GEOlayers/Help#geolayers3githubbrowseroptions)
- [GEOlayers 3 addToBrowser](https://github.com/GEOlayers/Help#geolayers3addtobrowseraddobj-callback-options)
- [GitHub size limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
