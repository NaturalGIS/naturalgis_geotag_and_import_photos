# Geotag and Import Photos
A QGIS plugin to tag and geo-tag photos (and import them as point layer)

### Introduction
This QGIS plugin can be considered an upgrade of the already existing and very good photo2shape plugin (http://hub.qgis.org/projects/photo2shape), developed by Alexander Bruy. The "Geotag and import photos" plugin was developed by Alexander Bruy and funded/designed by Giovanni Manghi (NaturalGIS, http://www.naturalgis.pt/) and Lolita Bizzarri (Museo Regionale di Scienze Naturali della Valle d'Aosta, http://www.museoscienze.it/)for a specific task: manage, display and analyse photos obtained from photo-trapping (http://en.wikipedia.org/wiki/Camera_trap) surveys of wildlife. This doesn't mean that the plugin can't be used for other purposes: it is pretty flexible and the result of imported tagged and geo-tagged photos do integrate nicely with other QGIS tools.

### Requirements
The tool is normal python plugin that can be installed trough the QGIS plugin installer/manager. The Geo-Tagging and Tagging capabilities rely on an external software called _exiftool_ (http://www.sno.phy.queensu.ca/~phil/exiftool/), freely available for all major platforms. On Ubuntu GNU/Linux "exiftool" is available by installing the package _libimage-exiftool-perl_.

### Configuring the plugin
Once installed the plugin adds a new entry in the QGIS vector menu (called "Geotag and import photos") and a new toolbar with three icons as shortcuts for different tools:

* GeoTag photos
* Tag photos
* Import photos

Before starting geotagging and tagging photos is needed to tell the plugin where the _exiftool_ program executable is located. Under GNU/Linux, if we installed _exiftool_ using a package manager, this step should not be necessary, while under OsX and MS Windows is mandatory.

Open the **Vector -> Geotag and import photos -> Settings** menu and in the resulting dialog set the appropriate path to the folder where _exiftool_ is located

**Note:** For MS Windows is suggested to download the standalone version (that do not requires any dependency and no installation at all) and then rename the executable to "exiftool.exe" to allow using its use from the command line. See: http://www.sno.phy.queensu.ca/~phil/exiftool/

### GeoTag photos

The tool recursively scan directories and sub-directories so it is not required to have all the photos in the same folder. Anyway all the photos in the same folder (and subfolders) will be tagged with the same coordinate.

It is possible to geotag multiple folders in one step, and each folder must be associated with the coordinate (in latitude/longitude, decimal degrees) to be given to photos. Coordinates can be entered manually or it is possible to use the ones of a point vector layer loaded in the QGIS project: the tool will populate (by hitting the "populate" table button) the table with the points coordinates and a label (taken from the point layer table of attributes)

When the "rename geotagged files" is unselected the plugin makes a copy of the photos as "filename_original" then it geotags the photos without changing their names.

When the "rename geotagged files" is selected the plugin makes a copy of the photos as "filename_original" then it geotags the photos renaming them: the chosen schema is **folder1_folder2_date_hour_progressivenumber**, where

**folder1, folder2, ...:** are the folder names where the photos are contained (the "top" folder is the one where the option "path to folder" points)

**date_hour:** is the date and hour when the photos was taken

**progressivenumber:** self explanatory

### Tag photos

The plugin allows to write/rewrite into photos both standard **EXIF** tags and also custom tags.

The dialog is very similar to the previous one and it works also in a very similar way, by tagging recursively all the photos inside a folder and its subfolders.

In this case the table must populated by hand, by:

* adding a new row
* entering the tag name
* entering the tag value

The tag names and values can also be chosen using a dropdown populated with the values inside of columns of the table of attributes of a vector layer added to the QGIS project.

If the tag name is a standard EXIF one, then the plugin does not need any further configuration. The list of standard EXIF tags is available here

http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html

For non standard (custom) tag names is necessary to use a configuration file, so if none is provided the non standard tags names will not be written inside photos.

Informations about how the configuration must be written are here

http://www.sno.phy.queensu.ca/~phil/exiftool/config.html

An example exiftool config file is available inside of the folder where the "Geotag and import photos" was installed. It looks like this:


    %Image::ExifTool::UserDefined = (
        # All EXIF tags are added to the Main table, and WriteGroup is used to
        # specify where the tag is written (default is ExifIFD if not specified):
        'Image::ExifTool::Exif::Main' => {
            0xd000 => {
                Name => 'Specie',
                Writable => 'string',
                WriteGroup => 'IFD0',
            },
            # add more user-defined EXIF tags here...
        },
    );
    
    #------------------------------------------------------------------------------
    1;  #end

This specific config file will allow to write a custom tag called Specie as a string value. Exiftool config files can be adapted to allow write more then 1 custom tags at the same time.

**Where to place/How to use the exiftool config file**

A exiftool config file can be placed/used in different ways:

* By selecting a config file from within the "Tag photos" dialog
* By selecting/configuring one in **Vector -> Geotag and import photos -> Settings**
* By placing it in the home folder of your user (typically for GNU/Linux and OsX machines). In this case to work the file must be named exactly _.ExifTool_config_

Rationale:

If a config file is specified in the "tag photos" dialog (1) then it will be used, and will override (2) if defined. If there is no local config file, then plugin will use global config from plugin settings. And finally, if there is no global config exiftool will use the config file available in the "home" directory, if exists.

### Import photos

The last tool is the one that allows the use to import geo-tagged photos as a point vector layer (in shapefile format) inside a QGIS project. The tool is pretty straightforward to use, as it is just necessary to specify the folder that contains the photos to be imported (the tool will scan also subfolders) and the name of to give to the resulting point vector layer.

Interesting features of this tool:

* It allows to append the results of the import to an already existing point vector layer
* It allows to choose what tags to import from the photos: the imported tags will be used to populate the table of attributes of the resulting point vector layer

along the process in the table of attributes of the resulting point vector layer will always be added two columns holding the absolute path and the filename of the imported photos

**IMPORTANT**

Shapefiles column names are by format design always limited to 10 chars maximum, so while importing EXIF tags this can result in truncated names.

### Styling with QGIS

All the imported photos that were tagged with the very same coordinate will render in QGIS as overlapped points. Applying a standard symbology would not be very useful as the points would be rendered as a cluster of overlapped symbols.

Fortunately QGIS has two nice adavanced symbology renderers that are very handy in such situations: they are called the rule based renderer and the point displacement renderer. Please refer to the Quantum GIS user manual to see how to use such symbology modes and to obtain the best results.

### Integration with other QGIS tools

The result of the imported geotagged photos (a point vector layer) integrate nicely with other QGIS tools, like the EViS Event Viewer tool, or even with other third party tools like the Time Manager plugin.