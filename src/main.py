
import xml_handlers
import json_handlers
import random

def random_color():
  levels = range(32,256,32)
  return [random.choice(levels) for _ in range(3)]

def random_hex_color():
  c = random_color()
  output = "#" + "".join(["%0.2X" % x for x in c])
  return output

json_obj = json_handlers.dump_json( "data/brain_atlas_labels.json" )

json_obj = json_obj["msg"][0]

#load the xml and its root node
doc,svg = xml_handlers.svg2xml("data/test_brain.svg")

#this is a hack, should do edits using search instead of iteration?
out_paths = xml_handlers.find_paths_tree(svg,limit=10)

for path in out_paths:
  node = svg

  for item in path:
    node = node[item]

  color = "#000000"

  #if node has a structure id
  try:
    struct_id = int(node.attrib["structure_id"])

    #search for the name of the structure
    struct_name = json_handlers.search_ontology(
      json_obj,
      "id", struct_id, "name"
    )

    #if the id has no name (not in allen ontology), continue
    if struct_name is None:
      continue

    #otherwise print it and its color
    old_style = node.attrib["style"]
    style_sub_fields = {}
    for field in old_style.split(";"):
      field = field.split(":")
      if len(field) != 2:
        print("style field error")
        exit(1)
      key = field[0]
      value = field[1]
      style_sub_fields[key] = value

    old_color = style_sub_fields["fill"]
    color=random_hex_color()
    print("struct name: %s, old color %s, new color (random) %s" % (struct_name, old_color, color))
  except KeyError:
    color="#000000"
    continue

  node.attrib["style"] = "stroke:#000000;fill:%s" % color

doc.write("data/test_out_random.svg")


