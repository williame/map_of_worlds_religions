import os, urllib2

data = (
    (-4000,	"ANIMISM in the Americas, SHAMANISM in Siberia, FOLK Religion in China and PROTO-INDO-EUROPEAN and INDO-IRANIAN religion in the middle. MESOPOTAMIAN MYTHOLOGY in Iraq and HINDUISM and JAINISM in India."),
    (-2500,	"CANAANITE religion in the middle-east, and MINOAN religion on Crete; human sacrifice and child cannibalism in both."),
    (-2000,	"HINDUISM is spreading from India. Hard to say whether it worships many gods or one god. Along with Jainism it's probably the world's oldest major religion still practiced today."),
    (-1500,	"MYCENEAN religion in Greece is where we get Poseidon, also known as Neptune from. He ruled the oceans for at least 2500 years until put into unemployment by Christianity. "),
    (-750,	"Greek Religion is influencing the Etruscans in Italy, explaining the similarity of Greek and Roman religions. "),
    (-600,	"BUDDHISM is born in Northern India, where JAINISM is also flourishing beside HINDUISM."),
    (-400,	"ZOROASTRIANISM in Persia believes the world started out flat and then got mountains caused by Evil."),
    (-300,	"Indonesian fishermen have discovered MADAGASCAR which is pretty impressive sailing. Animism remains the main religion there to this day."),
    (-200,	"JAINISM temporarily has official sanction over HINDUISM and BUDDHISM in India."),
    (0,     "The whole B-C A-D thing was only invented later. BUDDHISM has finds the silk road to China, displacing Folk Religions."),
    (200,	"ZOROASTRIANISM is following BUDDHISM's lead by taking the trade routes to China. "),
    (250,	"GNOSTIC CHRISTIANITY  is rivaling the \"catholic\" church, who persecute it. If GNOSTICISM had won out, Christianity would be massively different today. "),
    (350,	"CHRISTIANITY has split into ORTHODOX in the East and CATHOLIC in the West."),
    (450,	"ARIAN-CHRISTIAN Goths and Vandals are Vandalizing Rome and Persecuting CATHOLICS"),
    (700,	"ISLAM is spreading East and West, taking most of Spain. ROMAN CATHOLICISM gains in Britain"),
    (800,	"Despite centuries of Persecution by fellow CHRISTIANS, GNOSTICISM briefly becomes the state religion in what's now Mongolia. "),
    (850,	"Irish CATHOLIC monks try out Iceland. They give up before the Vikings arrive "),
    (1100,	"Crusades in the Holy Land"),
    (1200,	"The Pope disapproves of CATHARISM, a form of Gnostic Christianity and launches a Crusade into France. When some French CATHOLICS stay with the Heretical CATHARS, the order is given to just Kill everyone - \"God will know is own\". "),
    (1350,	"The French set up their own Pope. It lasts about 100 years. At one point they even launch a Crusade against the Roman Catholics in Naples."),
    (1400,	"In Eastern Europe the HUSSITES want reform. The CATHOLICS lure their leader John Hus to a meeting on the promise of safe passage, but then torture and burn him at the stake. The Hussite wars follow.  "),
    (1500,	"The Europeans set about converting America to CHRISTIANITY, spreading Jesus' love via the sword."),
    (1550,	"The REFORMATION starts. LUTHER, CALVIN and ZWINGLI lead the charge. Luther allegedly nails a list to church doors; the Catholics nail Anabaptists' genitals to the city gates in Munster. "),
    (1650,	"RUSSIAN ORTHODOX church erroneously decides it's doing its ceremonies incorrectly. Important things like the correct way to hold the fingers when making the sign of the cross. Those that do not change are persecuted. "),
    (1750,	"Hindus continues to gain independence from their Muslim overlords in India."),
    (1850,	"In southern China a Christian convert decides that he is the younger brother of Jesus. His Christian rebellion costs twenty million lives. Meanwhile Mormonism decides that Jesus will not come again in China, but in America."),
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
