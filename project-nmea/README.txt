prepinace:
-ft talker1[+talker2[+...+talkerN]]
	moznost filtrovani NMEA talkeru ... vice talkeru spojit symbolem +
	kdyz neni definovan, talkery se nefiltruji
	viz: https://gpsd.gitlab.io/gpsd/NMEA.html#_talker_ids


-fa float
	filtrovani podle vzdalenosti v uhlovych vterinach


-fs float
	filtrovani podle casu v sekundach


-fm float
	filtrovani podle vzdalenosti v metrech


-fr or|and
	pouzity vztah mezi nastavenym casem a vzdalenosti (v uhlovych vterinach nebo metrech)
	default: or


-i filename
	cesta vstupniho souboru


-o filename
	cesta vystupniho souboru



priklady:

	python3 main.py nmea/2008-08-06-08-53-42.nmea -fr or -fm 10 -fs 10 -ft gp+gn+gl
	python3 main.py nmea/2008-08-06-08-53-42.nmea -fr or -fm 10 -fs 10 -ft gp+gn+gl -o nmea\aaa
	python3 main.py nmea/2008-08-06-08-53-42.nmea -fs 10 -ft gp+gn+gl nmea/bbb
	python3 main.py -fs 10 -ft gp+gn+gl nmea/2008-08-06-08-53-42.nmea nmea/ccc