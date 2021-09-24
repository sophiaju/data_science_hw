import pandas as pd
# from pathlib import Path
# import os, sys
# parentdir = Path(__file__).parents[1]
# sys.path.append(parentdir)
# dialog_file_path = os.path.join(parentdir, 'src', 'dialog_analysis.py')

# print(parentdir)
# print(sys.path)
# print(dialog_file_path)

df = pd.read_csv("data/clean_dialog.csv")
print(list(df.columns))

