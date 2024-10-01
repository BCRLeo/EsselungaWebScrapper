#this will be the main file for the scrappingand the database, i will create
#the scrappers for each of the pages individually and then import them as libraries

#import Esselugna carne, pesce etc
#Create the db (maybe have that in a seperate program as I wont need to always be creating it
#run modules
#use pandas to analise the data
import os
import sqlite3
import EsselungaScrapper

class Prod:
    def __init__(self, Page):
        self.ProductsPage = Page
        self.ProductsIDs = []
        self.ProductsNames = []
        self.ProductsPrices = []
        self.ProductsDiscounts = []
        self.ProductsDiscountsStart = []
        self.ProductsDiscountsEnd = []
    
db_file = 'product_database.db'

db_exists = os.path.exists(db_file)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
def CreateDB():
    
    if not db_exists:
        cursor.execute('''
            CREATE TABLE Products (
                product_id INTEGER PRIMARY KEY,
                product_description TEXT NOT NULL
                -- Add other static product fields here if necessary
            )
        ''')

        cursor.execute('''
            CREATE TABLE PriceHistory (
                product_id INTEGER,
                date DATE,
                price_per_unit TEXT,
                discount_description TEXT,
                discount_start_date DATE,
                discount_end_date DATE,
                PRIMARY KEY (product_id, date),
                FOREIGN KEY (product_id) REFERENCES Products (product_id)
            )
        ''')
        """

        # Create the ExternalStats table
        cursor.execute('''
            CREATE TABLE ExternalStats (
                date DATE PRIMARY KEY,
                fuel_price REAL,
                inflation_rate REAL
                -- Add other external stats fields here
            )
        ''')"""

        conn.commit()
        print("Database created and tables set up.")
    else:
        print("Database already exists.")

CreateDB()

FruttaVerdura = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002314/frutta-e-verdura")
SpesaBio = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021465/spesa-bio")
PesceSushi = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002027/pesce-e-sushi")
Carne = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002007/carne")
LatticiniSalumiFormaggi = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002343/latticini-salumi-e-formaggi")
AlimentiVegetali = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001006876/alimenti-vegetali")
PanePasticceria = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002050/pane-e-pasticceria")
GastronomiaPiattiPronti = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002033/gastronomia-e-piatti-pronti")
ColazioneMerende = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001011197/colazione-e-merende")
PatatineDolciumi = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001019692/patatine-e-dolciumi")
ConfezionatiAlimentari = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002399/confezionati-alimentari")
SurgelatiGelati = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002075/surgelati-e-gelati")
MondoBimbi = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002278/mondo-bimbi")
AcquaBibiteBirra = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002062/acqua-bibite-e-birra")
ViniLiquori = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002081/vini-e-liquori")
IgieneCuraPersona = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/600000001034067/igiene-e-cura-persona")
IntegratoriSanitari = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/600000001034208/integratori-e-sanitari")
CuraCasaDetersivi = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002206/cura-casa-e-detersivi")
TempoLiberoOutdoor = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001024351/tempo-libero-e-outdoor")
AmiciAnimali = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001002264/amici-animali")
CancelleriaPartyGiocattoli = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021339/cancelleria-party-giocattoli")
MultimediaCarteRicariche = Prod("https://spesaonline.esselunga.it/commerce/nav/supermercato/store/menu/300000001021383/multimedia-carte-e-ricariche")


FruttaVerdura = EsselungaScrapper.Main(FruttaVerdura)

print(FruttaVerdura.ProductsIDs)


conn.close()
