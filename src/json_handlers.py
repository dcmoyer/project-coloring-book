
import json

##
## JSON LOADING STUFF
##

def dump_json( filepath ):
  with open(filepath,"r") as f:
    json_obj = json.load(f)
  return json_obj

#searches the allen inst. ontology for a key and a value, returning target
def search_ontology(onto, key, value, target):
  if onto[key] == value:
    return onto[target]

  try:
    for sub_onto in onto["children"]:
      attempt = search_ontology( sub_onto, key, value, target )
      if attempt is not None:
        return attempt
  except KeyError:
    pass

  return None


