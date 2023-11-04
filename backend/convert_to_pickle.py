import pandas as pd

FILE = "Scraping/data/module_details_labelled.csv"
df = pd.read_csv(FILE)
df.to_pickle("Scraping/data/module_details_labelled.pkl")
