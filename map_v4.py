import os, urllib2

data = (
	(-4000	,"and they are off! various animism in the americas, tribal stuff in africa, shamanism in siberia, folk stuff in china and proto-indo-european and indo-iranian religion in the middle. we have meso-po-tamian mythology in the sky blue and hinduism in the royal blue. a bit of jainism in india too by the looks of it!"),
	(-3500	,"a slow and steady start! wait, i think that's valdiva joining the race for the mid and south america's great civilizations! that's noshinto in japan and arabian polytheism in arabia by the way!"),
	(-3000	,"norte chico joins valdiva in south america, ancient egyptian religion has joined the race in the middle east. a steady field elsewhere. "),
	(-2500	,"the race in the mediterranean is hotting up with the canaanite religion in the levant  and minoan religion on crete; possibly some human sacrifice and child cannibalism"),
	(-2000	,"and just when we thought everything was pretty static, hinduism is on the move out of india! this could get exciting!"),
	(-1500	,"woah!! the mycenean religion is all the rage in greece, mesoamerican religion is defining itself with the olmec, south america has gone quite, norse mythology is evolving out of indo-european in scandinavia and the hittites are rising in turkey!"),
	(-1000	,"and the hitties are out of the race! the phoenicans and spread along the north african coast and sicily, judaism in the levant and mayan religion in the caribbean "),
	(-750	,"the asyrians are dominating the middle east with that evolved sumarian stuff, chavin are on the rise in peru. minoan and myceanean is now greek mythology and the etruscans are entering the race in italy. hinduism is spreading eastwards!"),
	(-700	,"the celts have arrived in europe, the etruscans and greeks are on the march, it's looking like the race will be won in the mediterranean theater!"),
	(-600	,"the greeks are moving fast now, buddhism is born in northern india, zoroastrianism is starting out among the iranian peoples although they have yet to arrive in iran!"),
	(-500	,"the celts are spreading fast now across northern europe, rome has rebelled against the etruscans in italy, buddhism is still small. "),
	(-400	,"hinduism and celtish religion is really going strong! the brown in iran is zoroastrianism."),
	(-300	,"the celts are still spreading through europe, hinduism seems to have run out of steam. alexander the great has conquered many peoples but he did not impose greek mythology on them. indonesian fishermen have discovered madagascar"),
	(-250	,"woah! buddhism suddenly gains ground in india, roman mythology is getting stronger, and cathage gains in spain with their canaanite stuff. "),
	(-200	,"india is where it's all at! jainism temporarily has official sanction over hinduism and buddhism. the celts are in turkey and cathage continues to grow in spain. "),
	(-100	,"hinduism regains ground in india, the romans are getting cocky in the med. "),
	(0	,"the romans are in the lead in the med, buddhism has found the silk road to china! apparently the year zero is a big deal in christianity but they don't get a pixel just yet. "),
	(100	,"the christians have started out, hitting the map in egypt. buddism looks to have stuck in china. "),
	(150	,"christianity is the purple spreading through the middle east and europe. rome especially of course. "),
	(200	,"christianity is already fracturing into different shades of purple! zoroastrianism is following buddhism's lead by taking the trade routes to china!"),
	(250	,"christianity has gnosticism running around unseen on the map, zoroastrianism has found a home in china but in iran it's persecuting itself and officially zurvanism. "),
	(300	,"christianity is also persecuting itself, whilst angles and saxons are visible in northern europe. "),
	(350	,"bang!!! christianity has split into orthodox and catholic, and the goths convert to arianism, a strain of christianity which had shocking ideas like preaching in native languages! that'll bite those catholics!"),
	(400	,"rome is crumbling, the arian-christian visigoths have moved to spain and the christian kingdom of axim is strong in africa. meanwhile buddhism is gaining over hinduism in much of south east asia. "),
	(450	,"arian-christian goths and vandals are vandalizing rome and persecuting catholics"),
	(500	,"arianism wanes out, but not much moves on the map in europe. buddhism continues to spread across east asia."),
	(550	,"sardinia and corsica change hands again, buddhism starts to gain ground in japan."),
	(600	,"all is quite, mostly"),
	(650	,"woah!the green spreading throughout the middle east, displacing arabian polytheism, zoroastrianism and christianity is islam. meanwhile buddhism claims tibet."),
	(700	,"islam is spreading east and west, taking most of spain. roman catholicism gains in britain"),
	(750	,"mostly persecution. despite losing ground to islam in the med, roman catholicism gains in northern europe."),
	(800	,"the muslims reach deep into france, but their religion is already fracturing, with shia islam gaining in morocco despite centuries of persecution by fellow christians, gnosticism becomes the state religion in what's now mongolia. "),
	(850	,"norse mythology gains in russia, gnosticism is quickly forgotten in mongolia, and the muslims are halted in spain. irish catholic monks try out iceland."),
	(900	,"the race takes a time out! no, wait, norse mythology now grabs iceland."),
	(950	,"shia islam gains much of north africa and iran. "),
	(1000	,"shia islam gains in sicily, the norse king of russia converts to eastern christianity starting the russian orthodox church. christianity survives in ethiopia, norse mythology sets up camp in america."),
	(1050	,"the vikings convert to roman catholicism, and add greenland to the gains, but give up in america."),
	(1100	,"the roman catholics wage holy war against the muslims in the holy land, but net-net the muslims gain most of turkey. the catholics do regain sicily."),
	(1150	,"in southern france, catharism, another gnostic christianity gains ground. "),
	(1200	,"the pope disapproves of catharism and launches a crusade into france. when some french catholics stay with the heretical cathars, the order is given to just kill everyone - 'god will know is own'. lovely. sunni islam retakes north africa and arabia from the shia."),
	(1250	,"islam is on the move again, in north africa and into india. catholicism is gaining in spain, where muslims and jews are now persecuted"),
	(1300	,"inca religion starts out in peru, sunni islam continues to politically dominate india and the last pagan kingdom in europe, lithuania, converts to christianity. polynesians discover new zeeland."),
	(1350	,"the french decide they don't like the pope in rome anymore and set up their own pope. islam continues to grow, even reaching philippines."),
	(1400	,"islam starts spreading through south east asia, and in eastern europe the hussites want reform. the catholics lure their leader to a meeting, before he is tortured and killed as a heretic. "),
	(1450	,"after a bitter war the catholics put down the hussite heretics; much persecution ensues. the inca religion is gaining ground in south america. "),
	(1500	,"the europeans set about converting america to christianity, spreading jesus' love via the sword."),
	(1550	,"the reformation hits europe, with protestant flavors of christianity. luther, calvin and zwingli lead the charge. protestants nail lists to church doors, the catholics nail anabaptist's genitals to doors in munster!"),
	(1600	,"catholicism loses the foothold in japan but gains philippines. scandinavia is solidly lutheran. britain is also protestant, and tibetan buddhism gains in mongolia. oh, and indonesia is sunni muslim."),
	(1650	,"puritan christians set up in new england, latin america is almost completely latin, and russian orthodoxy is at war with itself over which way to make the sign of the cross. do it the old way and you'll be persecuted. "),
	(1700	,"the french and spanish are spreading catholicism in north america, russian orthodoxy pushes east and the hindus start to regain territory from their muslim overlords. "),
	(1750	,"more of the same. russian orthodoxy continues to dominate russia, hinduism continues to gain independence from muslims in india. "),
	(1800	,"the first sikh kingdom in northern india, the british anglicans settle in australia. "),
	(1850	,"the anglicans put a flag in new zealand, baptist christianity gains in america and in southern china a christian convert discovers he is the younger brother of christ. his christian rebellion costs 20 million lives. mormanism gains in mid west of america. "),
	(1900	,"anglican britain is almost done converting australia, and every christian sect and their mum throws missionaries at africa. shintoism partly displaces buddhism in japan. "),
	(1950	,"with the catholic-facists in germans having murdered the jews, the jewish state of israel is set up in palestine. india's independence kicks out the last muslim rulers.	"),
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
    filename = 'map_v4_%d.mp3'%year
    ofp = open(filename,'wb') # because we assume bitrate etc is always the same, we simply concatentate
    for i,sentence in enumerate(parseText(text)):
        print i,len(sentence), sentence
        response = opener.open(google_translate_url+'?q='+sentence.replace(' ','+')+'&tl=en')
        ofp.write(response.read())
    ofp.close()
    os.system("mp3val %s -f -nb"%filename);
    #os.system('cvlc --play-and-exit -q '+filename)
