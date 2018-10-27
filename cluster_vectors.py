from annoy import AnnoyIndex
from scipy import spatial
from nltk import ngrams
import random, json, glob, os, codecs, random
import numpy as np

# data structures
file_index_to_file_name = {}
file_index_to_file_vector = {}
chart_image_positions = {}

# config
dims = 2048
n_nearest_neighbors = 5000
trees = 1000
infiles = glob.glob('image_vectors/*.npz')

# build ann index
t = AnnoyIndex(dims)
for file_index, i in enumerate(infiles):
  print('reading file', file_index)
  file_vector = np.loadtxt(i)
  file_name = os.path.basename(i).split('.')[0]
  file_index_to_file_name[file_index] = file_name
  file_index_to_file_vector[file_index] = file_vector
  t.add_item(file_index, file_vector)
print('buidling')
t.build(trees)
print('done')

# create a nearest neighbors json file for each input
if not os.path.exists('nearest_neighbors'):
  os.makedirs('nearest_neighbors')

for i in file_index_to_file_name.keys():
  master_file_name = file_index_to_file_name[i]
  master_vector = file_index_to_file_vector[i]

  named_nearest_neighbors = []
  nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)
  for j in nearest_neighbors:
	print('outer ', i, ' inner ', j)
	neighbor_file_name = file_index_to_file_name[j]
	neighbor_file_vector = file_index_to_file_vector[j]

    
  print(named_nearest_neighbors)
  with open('nearest_neighbors/' + master_file_name + '.json', 'w') as out:
    json.dump(named_nearest_neighbors, out)
