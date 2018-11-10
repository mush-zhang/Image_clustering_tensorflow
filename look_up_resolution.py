import json, glob, re, time
from PIL import Image

print 'begin'
start = time.time()

base = '/home/ling/sharedFiles'

# read file name look up table
with open(base + '/FileNames.txt', 'r') as lookup:
    lookup_raw = lookup.read()

lookup_vector = re.findall('"([^"]*)" = "([^"]*)"', lookup_raw)

lookup_dict = {}
for index in range(len(lookup_vector)):
    # key: filename without extension
    # values: original image name
    lookup_dict[lookup_vector[index][1][0:-4]] = lookup_vector[index][0]

# read json files
infiles = glob.glob(base + '/nearest_neighbors/*.json')
total = 0
mismatch = 0
data = []

for file_index, i in enumerate(infiles):
    
    #print(file_index)

    with open(i) as nn_list:

        file_vector = json.load(nn_list)
    
    file_total = 0
    file_mismatch = 0

    # find file number
    file_index = file_vector[0]['filename'].split('_')[1]
    # get original file resolution
    ori_image = Image.open(base+'/Original/'+lookup_dict[file_index])
    ori_size = ori_image.size

    # look up original image sizes of those with similarity>= 0.85
    for ind in range(len(file_vector)):
        
        if ind != 0 and file_vector[ind]['similarity'] >= 0.83:
            file_total += 1
            # find file number
            curr_index = file_vector[ind]['filename'].split('_')[1]
            # get original file resolution
            curr_image = Image.open(base+'/Original/'+lookup_dict[file_index])
            curr_size = curr_image.size
            
            #print curr_size
            
            # compare resolution
            if curr_size != ori_size:
                file_mismatch += 1
    
    data.append({
        'image': file_index,
        'total_similar': file_total,
        'size_mismatch': file_mismatch
    })

    #print data[-1]

    mismatch += file_mismatch
    total += file_total

# record number and percentage of resolution mismatch

data.insert(0, {
    'image': total,
    'total_similar': total,
    'size_mismatch': mismatch,
    'percentage_mismatch': float(mismatch)/total
})

with open(base + '/size_comparison_summary2.json', 'w') as out:
    json.dump(data, out)

print time.time() - start
