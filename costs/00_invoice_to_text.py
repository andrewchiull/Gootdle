# %%
from settings import S
from pathlib import Path
import pandas as pd
cwd = S.ROOT / "costs"

# %%

for d in cwd.iterdir():
    if d.is_dir() and (d / "invoice.csv").exists():
        results = list()
        with open(d / "invoice.csv") as f:
            df = pd.read_csv(f)

            # %%
            df
            
            # %%
            for index, row in df.iterrows():
                row

                # %%
                results.append(f"{index+1}. {row['品名']} [{row['單價']}*{row['數量']}] = NT${row['金額']}")

            # %%
            with open(d / "results.txt", 'w') as f:
                f.write("\n".join(results))
# %%
