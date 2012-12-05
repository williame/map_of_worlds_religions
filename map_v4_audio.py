import os, urllib2

data = (
    (-4000,	"The Shamans of the Steppes get into holy trances. Many neolithic belief systems were not organized religion but elements of many remain today."),
    (-2500,	"Canaanite and Minoan religions believed in human sacrifice and possibly child cannibalism"),
    (-2000,	"Hinduism spread from India into South-East Asia.  Along with Jainism it's probably the world's oldest major religion still practiced today."),
    (-1500,	"Mycenaean religion gives us Poseidon, later known as Neptune. He ruled the oceans for at least 2500 years until put into unemployment by Christianity. "),
    (-750,	"Greek Religion is influencing the Etruscans in Italy, explaining the similarity of Greek and Roman mythology. "),
    (-600,	"Buddhism is born in Northern India, but is comparatively rare in India today."),
    (-400,	"Zoroastrianism in Persia believes the world started out flat, and then evil created mountains."),
    (-300,	"South-East Asian fishermen have discovered Madagascar, which is impressive sailing. Animism remains the main religion there to this day."),
    (-200,	"Jainism temporarily has official sanction over Hinduism and Buddhism in India."),
    (0,     "Buddhism follows the silk road to China, displacing local folk religions as the main religion there."),
    (200,	"Zoroastrianism is follows Buddhism's lead by taking the trade routes to China, where it survives for about 1000 years, long after it is persecuted into a minority faith in its native Iran. "),
    (250,	"Gnostic Christianity is rivaling Catholicism in Europe. If it had not been successfully suppressed Christianity might be massively different today. "),
    (450,	"Arian-Christian Goths and Vandals vandalized Rome and persecuted the Catholics."),
    (700,	"Islam spread as far as Spain in the West."),
    (800,	"Despite centuries of Persecution, a form of Gnostic Christianity briefly becomes the state religion in what's now Mongolia. "),
    (850,	"Irish CATHOLIC monks try out Iceland. They give up before the Vikings arrive "),
    (1200,	"The Pope disapproves of Catharism, another form of Gnostic Christianity which exists in southern France. He launches a Crusade into France. When some French Catholics stay with the heretical Cathars, the order is given to just \"Kill everyone - God will know is own\". "),
    (1350,	"The French set up their own Pope. The schism lasts about 100 years. At one point they even launch a Crusade against the Roman Catholics in Naples."),
    (1400,	"In Eastern Europe the HUSSITES want reform. The CATHOLICS lure their leader John Hus to a meeting on the promise of safe passage, but then torture and burn him at the stake. The Hussite wars follow.  "),
    (1550,	"The reformation starts in Europe. Luther, Calvin and Zwingli lead the charge. Luther allegedly nails a list to a church door. The Catholics nail Anabaptists' genitals to the city gate in Munster. "),
    (1650,	"The Russian Orthodox church erroneously decides it's doing its ceremonies incorrectly. Like the correct way to hold the fingers when making the sign of the cross. Those that do not change to the evolved Greek methods are persecuted. "),
    (1850,	"In southern China a Christian convert decides that he is the younger brother of Jesus. His Christian rebellion costs twenty million lives. Meanwhile Mormonism decides that Jesus will actually come again in America not China."),
	)

def parseText(text):
 """ returns a list of sentences with less than 100 caracters """
 toSay = []
 punct = [',',':',';','.','?','!'] # punctuation
 words = text.split(' ')
 sentence = ''
 for w in words:
  if not w: continue
  if w[len(w)-1] in punct: # encountered a punctuation mark
   if (len(sentence)+len(w)+1 < 100): # is there enough space?
    sentence += ' '+w # add the word
    toSay.append(sentence.strip()) # save the sentence
   else:
    toSay.append(sentence.strip()) # save the sentence
    toSay.append(w.strip()) # save the word as a sentence
   sentence = '' # start another sentence
  else:
   if (len(sentence)+len(w)+1 < 100):   
    sentence += ' '+w # add the word
   else:
    toSay.append(sentence.strip()) # save the sentence
    sentence = w # start a new sentence
 if len(sentence) > 0:
  toSay.append(sentence.strip())
 return toSay
 
google_translate_url = 'http://translate.google.com/translate_tts'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]

for year, text in data:
    print year
    text = "%d %s. %s"%(abs(year),"B C" if year < 0 else "A D",text)
    filename = 'map_v4_%d'%year
    ofp = open(filename+".mp3",'wb') # because we assume bitrate etc is always the same, we simply concatentate
    for i,sentence in enumerate(parseText(text)):
        print i,len(sentence), sentence
        response = opener.open(google_translate_url+'?q='+sentence.lower().replace(' ','+')+'&tl=en')
        ofp.write(response.read())
    ofp.close()
    os.system("mp3val %s.mp3 -f -nb"%filename);
    os.system('cvlc --play-and-exit -q '+filename)
