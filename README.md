# Raw Data

The raw data for our collection come from various places:

## Database Catalog

Paul maintains a Microsoft Access database containing the catalog numbers, metadata, and legacy measurement data. A comprehensive cleaning of that database was made summer 2023. It is the authoritative source for catalog numbers, manufacturers, brands, brand descriptions, etc. New collection items are accessioned directly into it, and modifications are made to it via custom Access GUIs that Paul builds. It is stored on the IPCH server share ``\IPCH1-872004-YWCPCH\Labs\LML\``.

## Legacy Measurement Data

Prior to 2021, the paper collection was incompletely measured, and measurement data was collected at different times by different people. Precise provenance of these measurements is unavailable.

### Texture

Legacy texture captures are stored on the server share: ``IPCH1-872004-YWCPCH/Labs/LML/LML_collection/collection_catalog/client files/texture_images/from_camera``

### Thickness

Legacy thickness measurements come from the database itself, in columns "T1" through "T5". The server contains a file, ``IPCH1-872004-YWCPCH/Labs/LML/LML_collection/major_studies/Thickness/thickness_charts.xls``, but it appears to be a database export and not a raw source of thickness measurements.

### Gloss

Legacy gloss measurements are collected in a file (of unknown provenance) from 2015, and then alternatively in a study by Genevieve from 2019. There is some conflict with what the database reports, and some data puzzles remain about those measurements. All of Paul's 2015 measurements are in sample books, and all of Genevieve's measurements are from the binders.

### Color

Legacy color measurements were made by Madison, all of them on binder papers.

## Modern Measurement Data

### Texture

Modern texture captures are stored on the server share: ``\IPCH1-872004-YWCPCH\Labs\LML\LML_collection\major_studies\texture\LML Collection``

### Thickness, Gloss, Color

The rest of the modern measurement data is stored in a Dropbox folder: ``/lml/genome_measurements/``

Most comes from 2021, but we are adding additional measurements now in 2023.

# Processing

The processing of raw collection data is done here, in this repo, in the notebooks under ``proc/``. The notebooks also make use of processing libraries hosted on the ``ipchyale`` GitHub account: primarily [collproc](https://github.com/ipchyale/collproc) but also [ss2csv](https://github.com/ipchyale/ss2csv) for color data.

