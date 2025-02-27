#this will be the main file for the scrappingand the database, i will create
#the scrappers for each of the pages individually and then import them as libraries

#import Esselugna carne, pesce etc
#Create the db (maybe have that in a seperate program as I wont need to always be creating it
#run modules
#use pandas to analise the data
import os
import sqlite3
import EsselungaScrapper
import AuxiliaryData
import InsertTodb
import pandas as pd
from datetime import date
from models import Prod
import time
start = time.time()

 

FruttaVerdura = Prod("FruttaVerdura", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002314/frutta-e-verdura")
SpesaBio = Prod("SpesaBio", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021465/spesa-bio")
PesceSushi = Prod("PesceSushi", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002027/pesce-e-sushi")
Carne = Prod("Carne", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002007/carne")
LatticiniSalumiFormaggi = Prod("LatticiniSalumiFormaggi", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002343/latticini-salumi-e-formaggi")
AlimentiVegetali = Prod("AlimentiVegetali", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001006876/alimenti-vegetali")
PanePasticceria = Prod("PanePasticceria", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002050/pane-e-pasticceria")
GastronomiaPiattiPronti = Prod("GastronomiaPiattiPronti", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002033/gastronomia-e-piatti-pronti")
ColazioneMerende = Prod("ColazioneMerende", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001011197/colazione-e-merende")
PatatineDolciumi = Prod("PatatineDolciumi", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001019692/patatine-e-dolciumi")
ConfezionatiAlimentari = Prod("ConfezionatiAlimentari", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002399/confezionati-alimentari")
SurgelatiGelati = Prod("SurgelatiGelati", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002075/surgelati-e-gelati")
MondoBimbi = Prod("MondoBimbi", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002278/mondo-bimbi")
AcquaBibiteBirra = Prod("AcquaBibiteBirra", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002062/acqua-bibite-e-birra")
ViniLiquori = Prod("ViniLiquori", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002081/vini-e-liquori")
IgieneCuraPersona = Prod("IgieneCuraPersona", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/600000001034067/igiene-e-cura-persona")
IntegratoriSanitari = Prod("IntegratoriSanitari", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/600000001034208/integratori-e-sanitari")
CuraCasaDetersivi = Prod("CuraCasaDetersivi", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002206/cura-casa-e-detersivi")
TempoLiberoOutdoor = Prod("TempoLiberoOutdoor", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001024351/tempo-libero-e-outdoor")
AmiciAnimali = Prod("AmiciAnimali", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002264/amici-animali")
CancelleriaPartyGiocattoli = Prod("CancelleriaPartyGiocattoli", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021339/cancelleria-party-giocattoli")
MultimediaCarteRicariche = Prod("MultimediaCarteRicariche", "https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021383/multimedia-carte-e-ricariche")


objects_list = [
    FruttaVerdura,
    SpesaBio,
    PesceSushi,
    Carne,
    LatticiniSalumiFormaggi,
    AlimentiVegetali,
    PanePasticceria,
    GastronomiaPiattiPronti,
    ColazioneMerende,
    PatatineDolciumi,
    ConfezionatiAlimentari,
    SurgelatiGelati,
    MondoBimbi,
    AcquaBibiteBirra,
    ViniLiquori,
    IgieneCuraPersona,
    IntegratoriSanitari,
    CuraCasaDetersivi,
    TempoLiberoOutdoor,
    AmiciAnimali,
    CancelleriaPartyGiocattoli,
    MultimediaCarteRicariche
]

Indices = AuxiliaryData.FindEconomicData()
weather = AuxiliaryData.FindWeatherData()





conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
scrape_date = date.today()
cursor.execute("""
    INSERT INTO ScrapeRuns (ScrapeDate)
    VALUES (?)
""", (scrape_date,))
scrape_id = cursor.lastrowid
conn.commit()
conn.close()


##Insert esselunga scrape
for objects in objects_list:
    print(objects.Section)
    objects = EsselungaScrapper.Main(objects)
    InsertTodb.Insert(objects, scrape_id)

for index in Indices:
    InsertTodb.Insert(index, scrape_id)
##Inser Auxiliary scrapes
InsertTodb.Insert(weather, scrape_id)

end = time.time()
print("total time taken = ",end - start)

#FruttaVerdura = EsselungaScrapper.Main(FruttaVerdura)
# SpesaBio = EsselungaScrapper.Main(SpesaBio)
# PesceSushi = EsselungaScrapper.Main(PesceSushi)
# Carne = EsselungaScrapper.Main(Carne)
# LatticiniSalumiFormaggi = EsselungaScrapper.Main(LatticiniSalumiFormaggi)
# AlimentiVegetali = EsselungaScrapper.Main(AlimentiVegetali)
# PanePasticceria = EsselungaScrapper.Main(PanePasticceria)
# GastronomiaPiattiPronti = EsselungaScrapper.Main(GastronomiaPiattiPronti)
# ColazioneMerende = EsselungaScrapper.Main(ColazioneMerende)
# PatatineDolciumi = EsselungaScrapper.Main(PatatineDolciumi)
# ConfezionatiAlimentari = EsselungaScrapper.Main(ConfezionatiAlimentari)
# SurgelatiGelati = EsselungaScrapper.Main(SurgelatiGelati)
# MondoBimbi = EsselungaScrapper.Main(MondoBimbi)
# AcquaBibiteBirra = EsselungaScrapper.Main(AcquaBibiteBirra)
# ViniLiquori = EsselungaScrapper.Main(ViniLiquori)
# IgieneCuraPersona = EsselungaScrapper.Main(IgieneCuraPersona)
# IntegratoriSanitari = EsselungaScrapper.Main(IntegratoriSanitari)
# CuraCasaDetersivi = EsselungaScrapper.Main(CuraCasaDetersivi)
# TempoLiberoOutdoor = EsselungaScrapper.Main(TempoLiberoOutdoor)
# AmiciAnimali = EsselungaScrapper.Main(AmiciAnimali)
# CancelleriaPartyGiocattoli = EsselungaScrapper.Main(CancelleriaPartyGiocattoli)
# MultimediaCarteRicariche = EsselungaScrapper.Main(MultimediaCarteRicariche)



