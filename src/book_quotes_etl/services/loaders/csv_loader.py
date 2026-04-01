import pandas as pd

def load_to_csv(quotes: list[dict], csv_path):
    df = pd.DataFrame(quotes)
    df.to_csv(csv_path, index=False)
