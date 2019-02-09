
import os
from lxml import etree

##
##  XML LOADING STUFF
##

def svg2xml(path, **kwargs):

  # unzip .svgz file into .svg
  unzipped = False
  if isinstance(path, str) and os.path.splitext(path)[1].lower() == ".svgz":
    with gzip.open(path, 'rb') as f_in, open(path[:-1], 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    path = path[:-1]
    unzipped = True

  # load SVG file
  parser = etree.XMLParser(remove_comments=True, recover=True)
  try:
    doc = etree.parse(path, parser=parser)
    svg = doc.getroot()
  except Exception as exc:
    print("Failed to load input file! (%s)" % exc)
    return

  return doc,svg

def print_tree( tree, limit=2, level=0 ):
  print("."*level + ":",tree.tag)
  if level < limit and len(tree) > 0:
    for item in tree:
      print_tree(item, limit, level+1)

def find_paths_tree( tree, ret_path=[], limit=2, level=0 ):
  out_path = []
  if level < limit and len(tree) > 0:

    for idx,item in enumerate(tree):
      out_path.extend(\
        find_paths_tree(
          item,
          ret_path=ret_path+[idx],
          limit=limit,
          level=level+1
        )
      )

  elif tree.tag.endswith("path"):
    out_path.append(ret_path)
  return(out_path)


