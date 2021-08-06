import csv
import os

for dir in os.listdir('dados'):
    for filename in os.listdir('dados/'+dir):
        with open('dados/'+dir+'/'+filename, 'r') as in_file:
            next(in_file)
            stripped = (line.strip() for line in in_file)
            lines = (line.replace("X=", "").replace("Y=", "").replace("Z=", "").split() for line in stripped if line)
            with open('csv/'+dir+'/'+filename.replace('.txt', '')+'.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('time', 'x', 'y', 'z'))
                writer.writerows(lines)