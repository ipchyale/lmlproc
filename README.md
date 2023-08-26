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

## Pipeline Structure

In ``proc/`` there are separate folders for each of thickness, gloss, color, and texture. For each of these dimensions, we take a sequence of processing steps, all done in notebooks with the help of custom processing functions. The process is partly automated, partly manual, and there is simply no way to fully automate it. The data is created manually in most cases, and certain puzzles are too difficult for an automated pipeline to handle. Moreover, since our data is "small" and our collection is full of treasures, we cannot tolerate fixable errors.

1. ``raw.ipynb``: This is the simple conversion from raw data files to a single table. Very little in the way of cleaning is done, beyond eliminating null rows and columns, dropping complete duplicates, and perhaps splitting compound sample IDs to yield columns for catalog number, measurement location, trial number, etc.
2. ``dedupe.ipynb``: Although officially, catalog numbers should be unique, you will inevitably find duplicate catalog numbers in the measurement data. The core question we want to answer when we are resolving duplicates is: "Are the measurements made on the same object, or not?" In case they are, it is likely because the object was simply measured more than once, either accidentally or for some purpose (like a study of measurement variance). In case they are not, it is likely because of a typo. And when a typo creates a spurious duplicate, we now have two mysteries to solve: (1) which measurement is the genuine one (assuming there is one) and (2) which object did we measure when we made the typo? These mysteries cannot always be solved (and may require re-measurement), but in most cases, we can use external sources of data to clear up the confusion. Legacy measurements are surprisingly helpful here (and suffer far less duplication themselves) and in the modern measurement era, we started using a two-letter code that refers to the manufacturer and brand of the measured sample. These have been invaluable in reconciling duplicates.
3. ``validate.ipynb``: Typos can occur in other parts of the sample ID than the catalog number, at least for those physical dimensions that include a measurement location&mdash;viz., color and (sometimes) gloss. There are such typos in our color data, and we deal with them during this validation step. For example, if a measurement labeled _dmax_ has a lightness value of 0.97 (nearly pure white), that's probably invalid, and there was probably a typo.
4. ``outliers.ipynb``: Outliers have special importance in our pipeline, because we rely on our physical extrema to normalize our measurement values. When such extrema are too, ahem, extreme, we have to make a choice: do we want to leave the data in, on the assumption that it's valid, and suffer the consequences to our glyph shapes, or do we simply eliminate them? Should we always suspect that extreme outliers are invalid, and work to find out? These are tough questions, and they are not hypothetical: there are, for example, several gloss readings above 200GU, which is absurd, and far above the nearest tier below (which tops out at around 115GU). In the case of gloss, the problem arises in part because the measurement angle exerts significant influence on the gloss value. But this turns up in color, when we've measured an unusual sample, and in roughness, when we have capture artifacts in our texture micrographs.

### Multidimensional Validation and Measurement Flags

After processing each dimension separately, we can then consider them together with the catalog listing in the database. This is where we learn whether we have missing measurements. Taken singly, measurements from a single dimension can't tell us much about data that is missing completely&mdash;our measurement files contain only catalog numbers we've measured, so we can't know what is missing by looking for null rows, for example. But when we look at all the data together, we can see where the gaps lie. Moreover, we might find that, during the measurement process, we've created a spurious catalog number, one that doesn't exist at all in the database.

Additionally, it is here we can review measurement flags placed at the time of measurement. It would be possible to review these earlier in the process, during the unidimensional processing steps, but they are better reviewed at the end, when we have potentially corroborating information from other dimensions, and we can tell just what consequence our flags will have for the catalog item in question: did we skip multiple measurements? Just one? Should we eliminate the item from the data altogether (e.g., a color paper we flagged along multiple dimensions)? 

### CollectionItem

At this stage, we now have clean, deduped, validated data, and we've reviewed all of our measurement flags. From the perspective of the abstract "dataset", we're done. We have the data. But that data now needs to feed into different applications for analysis, visualization, reporting, etc. And we don't want to store this data simply as a data table (e.g., as a CSV file). Why? Because our collection is always growing, and updating a CSV file is a pain. We want a way to store each item as an instance of a class, a class that applies to every collection item and carries all of its relevant information. This way, when we need to make surgical modifications&mdash;either adding or removing individual items, modifying an item, etc.&mdash;we can work on individual objects without disrupting the rest.

Accordingly, we've written a Python class, ``CollectionItem``, that serves this purpose. The class definition can be found at ``collproc.coll.CollectionItem``, and includes attributes for core metadata as well as all measurement data. Moreover, because this is a Python object, and we will serialize it for storage using ``pickle``, we can actually store PIL Image objects in the class attributes as well. Thus, any glyph or goosebump plots we create can be stored right alongside the measurements and metadata. Technically, we could store all image assets in the class attributes (as NumPy arrays, for example), but this is probably a bad idea, because we'd then need to hold all such images in RAM if we want to load the collection into memory for analysis.

# Future: Object Database

For now, this is where the pipeline ends, and the ``CollectionItem`` instances are fed into collection reports, analyses, webapps like Paperbase, etc. They have their own schemata, and they shape and select the collections data accordingly. 

But the nature of the Python class is that it can be represented as a dictionary, which can then be easily converted to a JSON object. Once we have a JSON object for every collection item, we can store them in an object database (sometimes called _document_ database) like MongoDB. This probably doesn't make sense for now, but in the future, it may be preferable to store our data this way and access it through a GUI like Compass (which MongoDB offers for free).




