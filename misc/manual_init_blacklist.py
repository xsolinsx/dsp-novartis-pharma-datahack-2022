import pandas as pd

blacklist = set()
with open("domain_blacklist.txt", "r") as f:
    blacklist = set(f.read().splitlines())

df = pd.read_csv("domains.csv")
# have a list of unique urls for each domain sorted by descending number of urls
df_grouped = (
    df.groupby("domain")["url"]
    .apply(set)
    .apply(list)
    .reset_index()
    .sort_values(by="url", key=lambda x: x.apply(len), ascending=False)
)
# filter domains having 2+ urls
df_grouped = df_grouped[df_grouped["url"].apply(len) > 1]

for _, x in df_grouped.iterrows():
    tmp = x.to_dict()
    should_blacklist = input(
        f"\nThese are the links connected to {tmp['domain']}\n{tmp['url']}\n\nDo you want to blacklist it? Y|N "
    )
    if should_blacklist.lower() in ("yes", "y", "ok"):
        blacklist.add(tmp["domain"])
        with open("domain_blacklist.txt", "w") as f:
            f.writelines(f"{domain}\n" for domain in blacklist if domain)
        print(f"{tmp['domain']} was added to the blacklist\n")

with open("domain_blacklist.txt", "w") as f:
    f.writelines(f"{domain}\n" for domain in sorted(blacklist) if domain)

print(f"The blacklist now contains {len(blacklist)} domains")
