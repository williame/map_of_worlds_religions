from collections import defaultdict
import sys

def hu(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

LOWER = 33
UPPER = 122
RANGE = UPPER-LOWER
code = LOWER

rows = open("map_v4_religions.tsv","r").readlines()

out = open("map_v4_data.txt","w")

# list the religions
out.write("%d\n"%len(rows))
religions = {}
for i,religion in enumerate(rows):
    religion, colour = religion.split("\t")
    religion = religion.strip()
    colour = colour.strip()
    religions[religion], code = chr(code), code+1
    out.write("%s\t%s\n"%(religion,colour))

rows = open("map_v4.tsv","r").readlines()

# list the years
years = [year.strip() for year in rows[1].split("\t")[4:]]
out.write("\t".join(years)+"\n")

# and the map size
row = rows[-1].split("\t")
width, height = int(row[0]), int(row[1])
out.write("%d\t%d\n"%(width,height))

# now make a bitmap per year, with same-as-last-year marked as dups
dup, code = chr(code), code+1
data = ""
prev = [[None]*width for _ in xrange(height)]
for year in xrange(len(years)):
    for x in xrange(width-1,-1,-1): # this leads to better RLE compression, doing column order, and flipped
        for y in xrange(height-1,-1,-1):
            row = rows[1+(x*height)+y+1].split("\t")
            assert int(row[0]) == x+1, (x,y,row)
            assert int(row[1]) == y+1, (x,y,row)
            religion = religions[row[4+year].strip()]
            if religion == prev[y][x]:
                religion = dup
            else:
                prev[y][x] = religion
            data += religion
assert len(data) == len(years)*height*width
print "map",len(data),hu(len(data))
checksum = sum(ord(ch) for ch in data)
print "checksum",checksum
assert checksum == 55009555

# now RLE it
ofs, rle = 0, ""
run_1, run_2, code = chr(code), chr(code+1), code+2
MIN = 1 # fun fact: swapping out (code,code) for (code,rle-1) gives the next stage more to work on
MAX = MIN+RANGE**2 
while ofs < len(data):
    run = 0
    while ofs+run+1 < len(data) and run < MAX:
        if data[ofs+run+1] == data[ofs]:
            run += 1
        else:
            break
    rle += data[ofs]
    if run >= MIN:
        run -= MIN+1
        if run < RANGE:
            rle += run_1
            rle += chr(LOWER+run)
        elif run < RANGE*RANGE:
            rle += run_2
            rle += chr(LOWER+(run//RANGE))
            rle += chr(LOWER+(run%RANGE))
        else:
            sys,exit("bad run! "+run);
        ofs += run+1+MIN+1
    else:
        ofs += 1
print "rle",len(rle),hu(len(rle))

# now compress substrings
buf, compressed = rle, ""
MAX_REPLACE = 12
while True:
    # count all the strings of lengths 1 to 5
    counts = [None]
    for i in xrange(MAX_REPLACE):
        counts.append(defaultdict(int))
    for ofs in xrange(len(buf)):
        for i in xrange(1,len(counts)):
            if ofs+i == len(buf):
                break
            counts[i][buf[ofs:ofs+i]] += 1
    # find the most common occurances of each length
    commonest = [None]
    for i in xrange(1,len(counts)):
        commonest.append(sorted((count,key) for key,count in counts[i].items())[-1])
    if not compressed: # first time, so trivia
        print "trivia",commonest[-1]
    # find an unused character or digraph
    unused, unused_len = None, None
    for i in xrange(LOWER,UPPER+1):
        if chr(i) not in counts[1]:
            unused = chr(i)
            break
        elif not unused:
            for j in xrange(LOWER,UPPER+1):
                if chr(i)+chr(j) not in counts[2] and i != j:
                    unused = chr(i)+chr(j)
                    break
    if not unused:
        print "no more unused characters nor digraphs"
        break
    # if we have no unused characters, what is the cost of going character->digraph to create one?
    expansion = None
    if len(unused) > 1:
        for count, key in sorted((count,key) for key,count in counts[1].items()):
            if key not in unused:
                expansion = (key, 2+2+1+count)
                break
    # what is the greedy best thing to compress?
    best, best_size, best_expands = None, len(buf), False
    for i in xrange(len(unused)+1,len(counts)):
        # straight replace
        target = buf.replace(commonest[i][1],unused)
        target_size = 2+len(unused)+i+len(target)
        if target_size < best_size:
            best, best_size, best_expands = commonest[i][1], target_size, False
        # now with expansion?
        if expansion:
            target = buf.replace(commonest[i][1],expansion[0])
            target_size = expansion[1]+2+1+i+len(target)
            if target_size < best_size:
                best, best_size, best_expands = commonest[i][1], target_size, True
    # do it
    if best:
        if best_expands:
            best, best_size = expansion
        print compressed.count("\n")+1,"expands" if best_expands else "compacts",best,"->",unused,"=",(len(buf)-best_size),"->",best_size
        compressed = "%s\t%s\n%s"%(unused,best,compressed)
        buf = buf.replace(best,unused)
    else:
        print "no more compression to be had"
        break
compressed = "%s\n%s"%(buf,compressed)

out.write(compressed)
print "compressed",len(compressed),hu(len(compressed))
        
# check it all, by decompressing
rows = compressed.split("\n")
uncompressed = rows[0]
for row in rows[1:]:
    if not row: break
    find, replace = row.split("\t")
    uncompressed = uncompressed.replace(find,replace)
if rle == uncompressed:
    print "decompressed ok"
else:
    print "###"
    print uncompressed
    print rle
    sys.exit("decompression failed!")
unrle = ""
ofs, last = 0, None
while ofs < len(uncompressed):
    ch = uncompressed[ofs]
    ofs += 1
    if ch == run_1:
        run = ord(uncompressed[ofs])-LOWER
        run += MIN+1
        ofs += 1
    elif ch == run_2:
        run = (ord(uncompressed[ofs])-LOWER)*RANGE
        run += ord(uncompressed[ofs+1])-LOWER
        run += MIN+1
        ofs += 2
    else:
        unrle += ch
        last = ch
        continue
    for i in xrange(run):
        unrle += last
    #print "###",ofs,prev,ch,ch==run_1,ch==run_2,ord(ch)>=code,run
    if not data.startswith(unrle):
        print unrle
        print data[:len(unrle)]
        sys.exit("un-rle failed!")
if unrle == data:
    print "un-rle ok"
else:
    print "###"
    print unrle
    print data
    sys.exit("un-rle failed!")


