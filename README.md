# Overview
This python script will rename json files from google takeout to match the downloaded media files. 
All settings in this script are set to read only mode by default, so you do not accidentally modify your takeout 
data.

After fixing the json file names, you can run the exif command to patch back missing exif data into your media. 
See below for the commands I picked from the internet. 

## script arguments
| argument | Description                                                                                                                 |
| --- |-----------------------------------------------------------------------------------------------------------------------------|
| -t | Specify the folder to scan for media and json files. Typically specify the google takeout folder containing all your images |
| -r | Actually rename the json files to match the media file                                                                      |
| -v | Enable the verbose mode. The script will log more detailed messages while running. |

# EXIF commands
Run this command in the root folder of your media folder:

## Fix time stamps
On Windows
```
exiftool -d "%s" -tagsfromfile %d%f.%e.json "-DateTimeOriginal<PhotoTakenTimeTimestamp" "-FileCreateDate<PhotoTakenTimeTimestamp" "-FileModifyDate<PhotoTakenTimeTimestamp" -overwrite_original -ext mp4 -ext jpg -r .
```

On Linux
```
exiftool -d "%s" -tagsfromfile %d%f.%e.json "-DateTimeOriginal<PhotoTakenTimeTimestamp" "-FileModifyDate<PhotoTakenTimeTimestamp" -overwrite_original -ext mp4 -ext jpg -r .
```

## Fix geo location
```
exiftool -tagsfromfile %d%f.%e.json -description -title "-gpslatitude<GeoDataLatitude" "-gpslatituderef<GeoDataLatitude" "-gpslongitude<GeoDataLongitude" "-gpslongituderef<GeoDataLongitude" ... -ext mp4 -ext jpg -r .
```

