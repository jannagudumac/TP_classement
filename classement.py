import os
import sys
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

photos = []  # for photo paths

# recursive scan functionphotos = []  # for photo paths

def scan(folder):
    print("Scanning:", folder)
    
    items = os.listdir(folder)
    
    for item in items:
        path = os.path.join(folder, item)
        if os.path.isdir(path):
            scan(path)
        else:
            ext = item.lower().split(".")[-1]
            if ext in ["jpg", "jpeg", "png"]:
                photos.append(path)
                
# extract EXIF or file modification date
def extract_date(photo):
    image = Image.open(photo) # open image
    exif = image._getexif() # get EXIF data
    
    if exif:
        for tag, value in exif.items():
            name = TAGS.get(tag) # TAGS is a dictionary mapping tag numbers to names
            if name == 'DateTimeOriginal':  # original date tag
                date_str = value.split(" ")[0] #they're in format "YYYY:MM:DD HH:MM:SS", we separate where the space is, discarding the hours etc.
                year, month, _ = date_str.split(":") #then we split by ":" to get year, month, day, but day is not needed, therefore "_"
                return year, month, "exif"

    t = os.path.getmtime(photo) # file modification time in seconds from 1970
    date = datetime.fromtimestamp(t) # convert to a datetime object
    
    # Access year and month directly from the datetime object
    year = str(date.year)
    # The month value doesn't need explicit formatting; we can format it in the f-string 
    month = f"{date.month:02}"
    
    return year, month, "file" # return year, month, date_source

#classement 

def classify():
    if len(sys.argv) < 2: # check if folder argument is provided
        print("Error: Please provide a folder to scan")
        sys.exit(1) 

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a folder")
        sys.exit(1)

    scan(folder)

    main_folder = "classified_photos" #create main folder for classified photos

#dict
    photos_by_date = {} # dictionary to hold photos by date

    for photo in photos:
        year, month, date_source = extract_date(photo)
        date_folder = os.path.join(main_folder, year, month) # we create YEAR/MONTH folder
        #join is superior to simple concatenation because fits different OS / \
        
        if not os.path.exists(date_folder): # create destination folder if it doesn't exist
            os.makedirs(date_folder)
        
        photo_name = os.path.basename(photo) #basename gets the file name from the full path
        dest_path = os.path.join(date_folder, photo_name) # destination path
        os.rename(photo, dest_path) # move photo to new YEAR/MONTH location 

        key = f"{year}-{month}" # key for dictionary 
        if key not in photos_by_date: # check if key exists
            photos_by_date[key] = [] # initialize list
   
        year_month = os.path.join(year, month) 
        photos_by_date[key].append((photo_name, year_month, date_source)) # append photo info

    keys = photos_by_date.keys() # get all keys
    sorted_keys = sorted(keys) # sort keys

#csv
    with open("listePhotos.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write("file_name;destination_folder;date_source\n") # write CSV header
        for key in sorted_keys: # loop through sorted keys
            for name, path, date_source in photos_by_date[key]: 
                csv_file.write(f"{name};{path};{date_source}\n") # write photo info into the CSV file

    print("CSV file was created")


classify()