# IMPORTANT NOTE: I have not used oidv6-class-descriptions.csv as there are some duplicates in DisplayName
# So ALL the below functions have i/p and o/p as LabelName not as DisplayName


import json

def read_json(path):
  with open(path) as f:
    data = json.load(f)
    return data
    
def get_parsed_tree(tree):
  child_parsed_tree = {tree['LabelName']: {}}

  if 'Subcategory' not in tree.keys():
    return child_parsed_tree

  for child in tree['Subcategory']:
    parsed_child = get_parsed_tree(child)
    child_name = list(parsed_child.keys())[0]
    child_parsed_tree[tree['LabelName']][child_name] = parsed_child[child_name]
  return child_parsed_tree

def get_all_ancestors(tree, target, acc=None):
  if acc is None:
    acc = []
  
  tree_class = list(tree.keys())[0]
  if tree_class == target:
    return acc
  
  for child in list(tree[tree_class].keys()):
    found = get_all_ancestors({child: tree[tree_class][child]}, target, acc + [tree_class])
    if found is not None:
      return found

def get_all_siblings(tree, target):
  ancestors = get_all_ancestors(tree, target)
  
  for ancestor in ancestors:
    tree = tree[ancestor]

  return list(tree.keys())

def get_parent(tree, target):
  ancestors = get_all_ancestors(tree, target)
  if len(ancestors)==0:
    return None
  return ancestors[-1]

def get_parent(tree, target):
  ancestors = get_all_ancestors(tree, target)
  if len(ancestors)==0:
    return None
  return ancestors[-1]

def have_same_ancestors(tree, target1, target2):
  # Assuming father and sons don't have same ancestors as father is also ancestor of son
  siblings = get_all_siblings(tree, target1)
  return target2 in siblings

# tree = read_json("bbox_labels_600_hierarchy.json")
# parsed_tree = get_parsed_tree(tree)
# get_all_ancestors(parsed_tree, target='/m/0167gd')
# get_all_siblings(parsed_tree, target='/m/0167gd')
# get_parent(parsed_tree, target='/m/0167gd')
# have_same_ancestors(parsed_tree, target1='/m/0167gd', target2='/m/02rdsp')

