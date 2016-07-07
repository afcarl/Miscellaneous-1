import sys
reload(sys)
import os
import HTMLParser
from os.path import join
import xml.etree.ElementTree as et

sys.setdefaultencoding('UTF8')

input_dir = ''
out_file = ''
xml_fields = {}
files_failed  = ''

def extractTxtFromXmlFile(in_file, out_file):
    global files_failed
    try:
        inpT = et.parse(in_file)
    except:
        files_failed += in_file + '\n'
        return
    outf = open(out_file, "a+")
    found = 0;
    for field in xml_fields.keys():
        text = inpT.findtext(field)
        if text is not None:
            outf.write(HTMLParser.HTMLParser().unescape(text)+'\n')
            found = 1
            
    if found == 0:
        files_failed += in_file + '\n'     
    outf.close()        
    inpT = None

        

def extractTxtFromXmlFiles(input_dir, out_file):
    global files_failed
    outf = open(out_file, "w")
    if outf is None:
        print "Unable to open "+ out_file +" file for writing.\n"
        return
    outf.close()
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            extractTxtFromXmlFile(join(root, f), out_file)

    if files_failed is not "":
        print "Unable to process the following files:\n" + files_failed
    return
    


def process_arguments(argv):
    i = 0
    global input_dir
    global out_file
    global xml_fields
    content_fields = []
    while (i+1)<len(argv):
        if argv[i] == '--input_dir':
            input_dir = argv[i+1]
            i += 1
        elif argv[i] == '--out_file':
            out_file = argv[i+1]
            i += 1
        elif argv[i] == '--fields':
            content_fields = argv[i+1].split(',')
            xml_fields = dict(zip(content_fields, [j for j in range(len(content_fields))])) 
            i += 1
        i += 1
    if input_dir == '' or out_file == '' or content_fields == '':
        print 'input_dir and output file arguments are not specified.\n'
        print 'USAGE:' + sys.argv[0] + ' --input_dir location  --out_file location --fields tag_name\n'
        return 0
    return 1

if __name__ == '__main__':
    ret = process_arguments(sys.argv)
    if ret != 0:
      extractTxtFromXmlFiles(input_dir, out_file)


