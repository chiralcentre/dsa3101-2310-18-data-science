import pandas as pd

def convert_to_pickle(file,out_dir):
    df = pd.read_csv(file)
    df.to_pickle(out_dir)
    
'''
FILE = "Scraping/data/module_details_labelled.csv"
df = pd.read_csv(FILE)
df.to_pickle("Scraping/data/module_details_labelled.pkl")
'''

FILE = "Scraping/data/job_offers_categorized.csv"
out_dir = "Scraping/data/job_offers_categorized.pkl"
convert_to_pickle(FILE,out_dir)

'''
df = pd.read_pickle("Scraping/data/job_offers_categorized.pkl")
print(df["job_type"].unique())
'''
