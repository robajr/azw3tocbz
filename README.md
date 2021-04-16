# azw3tocbz

This dirty little python script converts azw3 (non-DRM) or epub files to cbz

It relies on:
* Python (base distribution)
* Calibre

It goes through a few steps:
* If the incoming file is azw3, converts to epub using calibre command line arguments (python os call)
* Unzips and parses through the epub directory, reordering the images based on their appearance in the .html files
* Copies and renames the cover image
* Packages up the files to cbz
* Cleans itself up

It assumes:
* The file layout and format calibre uses for azw3 to epub is consistent (has been so far!)

Still to do:
* Create cbz metadata file
