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
            data += religion
assert len(data) == len(years)*height*width
print "map",len(data),hu(len(data))
print "checksum",sum(ord(ch) for ch in data)

# now RLE it
ofs, rle = 0, ""
run_1, run_2, run_3, code = chr(code), chr(code+1), chr(code+2), code+3
run_zero = None #UPPER-code # set to None to disable
MIN, MAX = 2, RANGE**2 # fun fact: swapping out (code,code) for (run,2) gives the next stage more to work on
while ofs < len(data):
    run = 0
    while ofs+run+1 < len(data) and run < MAX:
        if data[ofs+run+1] == data[ofs]:
            run += 1
        else:
            break
    rle += data[ofs]
    if run >= MIN:
        if run_zero and run < run_zero:
            rle += chr(code+run)
        elif run < RANGE:
            rle += run_1
            rle += chr(LOWER+run)
        elif run < RANGE*RANGE:
            rle += run_2
            rle += chr(LOWER+(run//RANGE))
            rle += chr(LOWER+(run%RANGE))
        else:
            rle += run_3
            rle += chr(LOWER+((run//(RANGE*RANGE))))
            rle += chr(LOWER+((run//RANGE)%RANGE))
            rle += chr(LOWER+(run%RANGE))
        ofs += run+1
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
ofs, prev = 0, None
while ofs < len(uncompressed):
    ch = uncompressed[ofs]
    ofs += 1
    run = 1
    if ch == run_1:
        ch = prev
        run = ord(uncompressed[ofs])-LOWER
        ofs += 1
    elif ch == run_2:
        ch = prev
        run = (ord(uncompressed[ofs])-LOWER)*RANGE
        run += ord(uncompressed[ofs+1])-LOWER
        ofs += 2
    elif ch == run_3:
        ch = prev
        run = (ord(uncompressed[ofs])-LOWER)*RANGE*RANGE
        run += (ord(uncompressed[ofs+1])-LOWER)*RANGE
        run += ord(uncompressed[ofs+2])-LOWER
        ofs += 3
    elif ord(ch) > code:
        assert run_zero
        run = ord(ch)-code
        ch = prev
    for i in xrange(run):
        unrle += ch
    prev = ch
    if not data.startswith(unrle):
        print "###",ofs,prev,ch,ch==run_1,ch==run_2,ch==run_3,ord(ch)>code,run
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


