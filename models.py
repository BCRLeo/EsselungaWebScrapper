class Prod:
    def __init__(self, Section,Page):
        self.StoreName = "Esselunga"
        self.Section = Section
        self.ProductsPage = Page
        self.ProductsIDs = []
        self.ProductsNames = []
        self.ProductsPrices = []
        self.ProductsDiscounts = []
        self.ProductsDiscountsStart = []
        self.ProductsDiscountsEnd = []


class Indicators:
    def __init__(self,category, button):
        self.Category = category
        self.Button = button
        self.IndicatorName = []
        self.IndicatorLatest = []
        self.IndicatorPrevious = []
        self.IndicatorUnit = []
        self.IndicatorDate = []