import os, sys, shutil
import zipfile
import codecs, re

def main(argv):
    # Command line arguments are just a list of files, .epub or .azw3
    for x in argv[1:]:
        processZip(x)

def processZip(zipname):

    print("Processing " + zipname[:-5])
    if (zipname[-4:] == 'azw3'):

        # Use calibre to convert Amazon book to epub
        # "Tablet" profile prevents image downsizing
        oscmd = 'ebook-convert "'+zipname+'" "'+zipname[:-5]+'.epub" --output-profile tablet'
        print("Launching Calibre CLI to convert AZW3: " + oscmd)
        print("If this fails, please make sure Calibre is in your PATH directory")
        os.system(oscmd)

        #remove .azw3 and add .epub file type to variable
        zipname = zipname[:-5]+'.epub'


    # read file list
    if zipfile.is_zipfile(zipname):
        print("Valid file type - extracting to temporary directory to rebuild to .cbz structure")
        with zipfile.ZipFile(zipname) as zf:

            # Extract epub files
            tmpDirName = "tmpDir"+zipname
            zf.extractall(tmpDirName)

            # Process files
            reorderImages(tmpDirName)

            # Collect fixed images into one zip
            print("Zipping file")
            directory = tmpDirName+"\\fixed"
            shutil.make_archive(zipname, 'zip', directory)

            print("Renaming to cbz and cleaning up")
            shutil.move(zipname+".zip",zipname[:-5]+".cbz")
            shutil.rmtree(tmpDirName)
            
            print("Done")

    else:
        print(zipname + " is an invalid Zip or epub file")

def reorderImages(dirName):
    # This looks at .xhtml or .html files and finds correct image
    # Exports images into sequential order
    # Assumes calibre consistently places images in ../images folder
    # Assumes calibre consistently uses partXXXX.html for file naming

    i = 0
    os.system('md "'+dirName+'\\fixed"')

    while True:
        try:
            # This attempts two known format styles, no real backup here, it's one or the other
            # Will likely crap out if it doesn't follow these two, and I have no error raise functions
            try:
                file = codecs.open(dirName + "/text/part"+format(i, '04')+".html", 'r', 'utf-8')
            except:
                file = codecs.open(dirName + "/OEBPS/text/p_"+format(i, '04')+".xhtml", 'r', 'utf-8')

            line = file.readline()
            while line:
                    match = re.search(r'.*<img src="..(/images?\S*.[jpg,jpeg,png])',line)                    
                    if match:
                        # Moves the matched image to a single directory, ordered by image number
                        src = dirName+match.group(1)                        
                        dest = dirName+'\\fixed\\'+format(i, '04')+'.jpeg'
                                               
                        shutil.copyfile(src, dest)

                    line = file.readline()

            file.close()
            i = i + 1
        except:
            break

    print("Looking for cover image")
    try:
        file = codecs.open(dirName + "/titlepage.xhtml", 'r', 'utf-8')
    except:
        file = codecs.open(dirName + "/OEBPS/text/p_cover.xhtml", 'r', 'utf-8')
    line = file.readline()
    while line:
        
        match = re.search(r'(?<=="images/)\S*.[jpg,jpeg,png]',line)
        if match:
            
            src = dirName+'\\images\\'+match.group(0)
            dest = dirName+'\\fixed\\00000000_cover.jpg'
            
            shutil.copyfile(src, dest)

        line = file.readline()
        

if __name__ == "__main__":
    main(sys.argv)
