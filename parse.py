import glob, sys
import regex as re
from xml.etree import ElementTree

category = sys.argv[1]

namespace = "{http://www.w3.org/2005/Atom}"

def get(element, name):
    child = element.find(namespace + name)
    if child.text != None:
        return child.text
    else:
        return ""

for xmlfile in glob.glob(f"{category}/*.xml"):
    tree = ElementTree.parse(xmlfile)
    
    for entry in tree.iter(namespace + "entry"):
        entry_id = get(entry, "id")
        date = get(entry, "updated")[0:7]
        title = get(entry, "title")
        summary = get(entry, "summary")
        
        text = "{} {} {}".format(title, title, summary)
        text = re.sub(r"\s+", " ", text)
        
        print("{}\t{}\t{}".format(entry_id, date, text))