import os, urllib2

data = (
    (-4000,"Sumerians' religion in Mesopotamia (Iraq) is the father of the later Assyrian Empires' religion. The family of religions lasted thousands of years in the middle east. They practiced \"sacred prostitution\". Probably why they say the empire went up and down quite a bit. "),
    (-3500,"Civilization started in middle and south America around this time. A succession of great civilizations there, from the Validiva, Olmec,  and later and more familiar Mayan, Aztec and Inca civilizations generally built impressive temples and pyramids and believed in ritual sacrifice. "),
    (-2600,"The ancient Egyptians build the Great Sphinx at Giza. It is among the oldest religious monument surviving today, although a local Muslim leader attempted to destroy it 2000 years after it's construction on religious grounds. He only succeeded in removing the nose. "),
    (-2400,"Canaanite and Minoan religions believed in human sacrifice and possibly child cannibalism"),
    (-2000,"Hinduism spreads elephant-headed gods from India into South-East Asia.  Along with Jainism it's probably the world's oldest major religion still practiced today. Jainism emphasizes pacifism"),
    (-1700,"The Hittites religion was another offshoot of the Mesopotamian religion. They believed that the god of thunder was conceived when the King god bit off the sky god's genitals. The story is made all the more weird by the fact that the sky god is the king god's father. "),
    (-1500,"Mycenaean religion gave rise to Poseidon, later known as Neptune. He ruled the oceans for at least 2500 years until put into unemployment by Christianity. "),
    (-750,"Greek Religion is influencing the Etruscans in Italy, explaining the similarity of Greek and Roman mythology. "),
    (-600,"Buddha is born in Northern India (probably Nepal) as a Hindu prince. The religion he started is comparatively rare in India today. "),
    (-400,"Zoroastrianism in Persia believes the world started out flat, but then evil created mountains. Zoroastrianism believes in only one God, which is termed Mono-theism. "),
    (-300,"South-East Asian fishermen have discovered Madagascar. Animism remains the main religion there to this day."),
    (-200,"Jainism temporarily has official sanction over Hinduism and Buddhism in India."),
    (0,"Buddhism follows the silk road to China, displacing local folk religions as the main religion for poor people there. The elite follow Taoism, but successive dynasties are often tolerant of religions. There's also Confucianism but that is generally regarded as a philosophy rather than a religion. "),
    (200,"Zoroastrianism is follows Buddhism's lead by taking the trade routes to China, where it survives for about 1000 years, long after it is persecuted into a minority faith in its native Iran. "),
    (250,"Gnostic Christianity is rivaling Catholicism in Europe. If it had not been successfully suppressed Christianity might be massively different today. "),
    (450,"The Goths and Vandals that vandalized Rome were actually Christians. They followed Arianism which was an early form of Christianity that for a time rivaled the Church in Rome."),
    (700,"Islam spreads as far as Spain in the West. It also controlled Sicily at one point."),
    (800,"Despite centuries of Persecution, a form of Gnostic Christianity briefly becomes the state religion in what's now Mongolia. "),
    (850,"Irish CATHOLIC monks try out Iceland. They give up before the Vikings arrive "),
    (950,"Despite the Muslim dominance of north Africa, the Christian kingdom of Axum and it's successors hung on in Ethiopia. In the middle ages they built monolithic churches hidden within solid bedrock."),
    (1200,"The Pope disapproves of Catharism, another form of Gnostic Christianity which exists in southern France. He launches a Crusade into France. When some French Catholics stay with the heretical Cathars, the order is given to just \"Kill everyone - God will know is own\". "),
    (1300,"The last Pagan kingdom in Europe, Lithuania, finally succumbs to Christianity "),
    (1350,"The French set up their own Pope. The schism lasts about 100 years. At one point they even launch a Crusade against the Roman Catholics in Naples."),
    (1400,"In Eastern Europe the HUSSITES want reform. The CATHOLICS lure their leader John Hus to a meeting on the promise of safe passage, but then they torture and burn him at the stake. The Hussite wars follow.  "),
    (1550,"The reformation starts in Europe. Luther, Calvin and Zwingli lead the charge. Luther allegedly nails a list to a church door. The Catholics nail Anabaptists' genitals to the city gate in Munster. "),
    (1650,"The leader of the Russian Orthodox church erroneously decides it's been doing its ceremonies incorrectly. Things like the correct way to hold the fingers when making the sign of the cross, or which way to walk in a circle. Those that do not change to the revised doctrine are persecuted. "),
    (1850,"In southern China a Christian convert decides that he is the younger brother of Jesus Christ. His Christian rebellion costs twenty million lives. Meanwhile Mormonism decides that Jesus will actually come again in America not China."),
    (1900,"The Christianization of central and southern Africa is in full swing. The Dutch Reformed church, the 'official' church in South Africa, actively supported apartheid. Several uniquely African christian denominations are created. "),
    (1950,"Only two of the 55 Founding Fathers of America were Roman Catholics. Yet due to mass immigration Catholicism was soon the largest religious group in the United States. In the 1920s the Protestant Klu Klux Klan was focused on anti-Catholicism."),
    (2000,"The Zoroastrianism pixel in India actually represents the minority Parsi community. They originally fled Islamic persecution in Iran. Freddy Mercury was a Parsi. "),
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
