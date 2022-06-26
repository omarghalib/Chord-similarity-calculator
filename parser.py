import os
import json
import re

def read_all_files_and_parse_to_json(folderPath, fileName):
  subfolders = [ f.path for f in os.scandir(folderPath) if f.is_dir() ]
  # a Python object (dict):
  dict_object = {}
  node_id = 0
  for subfolder in subfolders:
    sub_dict = {}
    chords_dict = {}
    f = open(subfolder+"/" +fileName, "r")
    salami_chords = f.read()
    chord_set = get_chord_set(salami_chords)
    chord_id = 0
    for chord in chord_set:
      chords_dict[chord_id] = chord
      chord_id = chord_id + 1
    sub_dict["title"] = get_title(salami_chords)
    sub_dict["artist"] = get_artist(salami_chords)
    sub_dict["chords"] = chords_dict
    dict_object[node_id] = sub_dict
    node_id = node_id + 1
    # convert into JSON:
  json_object = json.dumps(dict_object)
  return json_object

def get_chord_set(text):
  chord_list = []
  chords = re.findall('\|(.*)\|', text, flags=0)
  for line in chords:
    chord_list = chord_list + re.split('\|', line)
  chord_set = set(chord_list)
  return chord_set

def get_title(text):
  return re.search('# title:(.*)',text).group(1)

def get_artist(text):
  return re.search('# artist:(.*)',text).group(1)

def save_json_to_file(filePath, jsonString):
  with open(filePath, 'w') as outfile:
    outfile.write(jsonString)

def main():
    json_tree = read_all_files_and_parse_to_json("/content/drive/MyDrive/Colab Notebooks/McGill-Billboard", "salami_chords.txt")
    save_json_to_file("/content/drive/MyDrive/McGill_Billboard.json",json_tree)

if __name__ == "__main__":
    main()
