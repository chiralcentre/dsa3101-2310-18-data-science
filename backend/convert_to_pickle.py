import pandas as pd

def convert_to_pickle(file,out_dir):
    df = pd.read_csv(file)
    df.to_pickle(out_dir)
    
'''
FILE = "./data/module_details_labelled.csv"
df = pd.read_csv(FILE)
df.to_pickle("./data/module_details_labelled.pkl")
'''

FILE = "./data/job_offers_categorized.csv"
out_dir = "./data/job_offers_categorized.pkl"
convert_to_pickle(FILE,out_dir)

'''
df = pd.read_pickle("./data/job_offers_categorized.pkl")
print(df["job_type"].unique())
'''
