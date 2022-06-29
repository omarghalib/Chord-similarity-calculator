import os
import json
import re

def read_all_files_and_parse_to_dict(folderPath, fileName):
  subfolders = [ f.path for f in os.scandir(folderPath) if f.is_dir() ]
  dict_object = {}
  songs_dict = {}
  list_of_chord_sets = []
  node_id = 0
  for subfolder in subfolders:
    sub_dict = {}
    chords_dict = {}
    f = open(subfolder+"/" +fileName, "r")
    salami_chords = f.read()
    chord_set = get_chord_set(salami_chords)
    list_of_chord_sets.append(chord_set)
    chord_id = 0
    for chord in chord_set:
      chords_dict[chord_id] = chord
      chord_id = chord_id + 1
    sub_dict["title"] = get_title(salami_chords)
    sub_dict["artist"] = get_artist(salami_chords)
    sub_dict["chords"] = chords_dict
    songs_dict[node_id] = sub_dict
    node_id = node_id + 1
  dict_object["songs"] = songs_dict
  return [dict_object, list_of_chord_sets]

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

def update_dict_with_similarity_scores(output_dict, list_of_chord_sets):
  song_id = 0
  scores_dict = {}
  for chord_set in list_of_chord_sets:
    scores_dict[song_id] = {"similarityScores": {}}
    other_song_id = 0
    for other_chord_set in list_of_chord_sets:
      similarity_score = calculate_similarity_score(chord_set, other_chord_set)
      scores_dict[song_id]["similarityScores"][other_song_id] = {"score": similarity_score, "songId": other_song_id}
      other_song_id = other_song_id + 1
    song_id = song_id + 1
  output_dict["scores"] = scores_dict
  return output_dict
    
def calculate_similarity_score(chord_set, other_chord_set):
  intersection = chord_set.intersection(other_chord_set)
  similarity_score = len(intersection) / len(other_chord_set)
  return similarity_score

def convert_dict_to_json(dict_object):
  json_object = json.dumps(dict_object)
  return json_object

def main():
    [output_dict, list_of_chord_sets] = read_all_files_and_parse_to_dict("/content/drive/MyDrive/Colab Notebooks/McGill-Billboard", "salami_chords.txt")
    output_dict = update_dict_with_similarity_scores(output_dict, list_of_chord_sets)
    json_tree = convert_dict_to_json(output_dict)
    save_json_to_file("/content/drive/MyDrive/McGill_Billboard.json",json_tree)

if __name__ == "__main__":
    main()
