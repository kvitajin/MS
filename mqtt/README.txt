k instalaci MQTT jsem pouzil prikaz:
    pip install paho-mqtt

mam naimplementovano kompletni zadani klienta, vcetne last will (celkem 6.5 bodu?)

samozrejme je potreba byt ve skolni siti
po spusteni je uzivatel vyzvan k zadani ID
po "prihlaseni" jsou v klientovi nahore dve zalozky: verejny a privatni chat
jmeno prihlaseneho uzivatele je zobrazeno ve jmenu okna
jak verejny tak i privatni chat maji dole okno pro zadani textu a tlacitko pro odeslani
v pripade privatniho chatu je potreba z leveho seznamu vybrat jmeno prijemce
tento seznam se obnovuje dynamicky s prichazejicimi stavy z /mschat/status/#
klient lze spustit vicekrat na jednom systemu

Vim ze po graficke strance je v tom klientu mnoho nevyuziteho mista,
ale doufam ze pro demonstaci fungovani chatu v MQTT toto reseni postacuje.