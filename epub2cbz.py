import os
import sys, shutil
import zipfile
from zipfile import ZipFile
import codecs, re

def main(argv):
    for x in argv[1:]:
        processZip(x)

def processZip(zipname):

    print("Processing " + zipname + " " + zipname[:-5])
    if (zipname[-4:] == 'azw3'):
        oscmd = 'ebook-convert "'+zipname+'" "'+zipname[:-5]+'.epub" --output-profile tablet'
        print(oscmd)
        os.system(oscmd)

        zipname = zipname[:-5]+'.epub'


    # read file list
    if zipfile.is_zipfile(zipname):
        print("Valid file - extracting to temporary directory")
        with zipfile.ZipFile(zipname) as zf:

            # Extract epub files
            tmpDirName = "tmpDir"+zipname
            zf.extractall(tmpDirName)

            # Process files
            reorderImages(tmpDirName)

            # Collect fixed images into one zip
            directory = tmpDirName+"\\fixed"
            shutil.make_archive(zipname, 'zip', directory)
            shutil.move(zipname+".zip",zipname[:-5]+".cbz")
            shutil.rmtree(tmpDirName)

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
            file = codecs.open(dirName + "/text/part"+format(i, '04')+".html", 'r', 'utf-8')
            line = file.readline()
            while line:
                    # print(line)
                    match = re.search(r'(?<=img src="../images/)\S*.[jpg,jpeg,png]',line)
                    if match:
                        #print("Found image - " + match.group(0))
                        src = dirName+'\\images\\'+match.group(0)
                        dest = dirName+'\\fixed\\'+format(i, '04')+'.jpeg'
                                               
                        shutil.copyfile(src, dest)

                    line = file.readline()

            file.close()
            i = i + 1
        except:
            break

    print("Looking for cover image")
    file = codecs.open(dirName + "/titlepage.xhtml", 'r', 'utf-8')
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