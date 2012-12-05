import string

rows = open("map_v4_religions.tsv","r").readlines()

out = open("map_v4_data.txt","w")

out.write("%d\n"%len(rows))
religions = {}
for i,religion in enumerate(rows):
    i = string.printable[i]
    religion, colour = religion.split("\t")
    religion = religion.strip()
    colour = colour.strip()
    religions[religion] = i
    out.write("%s\t%s\t%s\n"%(i,religion,colour))

rows = open("map_v4.tsv","r").readlines()

years = [year.strip() for year in rows[1].split("\t")[4:]]
out.write("\t".join(years)+"\n")

row = rows[-1].split("\t")
width, height = int(row[0]), int(row[1])

dup, run_short, run_long = string.printable[len(religions):][:3]
out.write("%d\t%d\t%s\t%s\t%s\n"%(width,height,dup,run_short,run_long))
data = []
prev = [[None]*width for _ in xrange(height)]

for year in xrange(len(years)):
    for y in xrange(height):
        for x in xrange(width):
            row = rows[1+(x*height)+y+1].split("\t")
            assert int(row[0]) == x+1, (x,y,row)
            assert int(row[1]) == y+1, (x,y,row)
            religion = religions[row[4+year].strip()]
            if religion == prev[y][x]:
                religion = dup
            else:
                prev[y][x] = religion
            data.append(religion)
            
assert len(data) == len(years)*height*width
           
ofs, written = 0, 0
MIN, SHORT, MAX = 2, 122-64, (122-64)**2
while ofs < len(data):
    run = 0
    while ofs+run+1 < len(data) and run < MAX:
        if data[ofs+run+1] == data[ofs]:
            run += 1
        else:
            break
    out.write(data[ofs])
    written += 1
    if run > MIN:
        if run < SHORT:
            out.write(run_short)
            out.write(chr(64+run))
            written += 2
        else:
            out.write(run_long)
            out.write(chr(64+(run//SHORT)))
            out.write(chr(64+(run%SHORT)))
            written += 3 
        ofs += run+1
    else:
        ofs += 1
        
print len(data), ofs-1, written, sum(ord(ch) for ch in data)
        
    



