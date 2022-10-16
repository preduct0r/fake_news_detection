import os

import pandas as pd
import telethon
import telethon.sync
import tqdm
import yaml

with open("src/crawler_telegram/telegram_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    username = config["username"]

client = telethon.sync.TelegramClient(username, api_id, api_hash)
client.start()

total_posts_limit = 10
limit = 1  
data_path = "data/raw/telegram"

channels = pd.read_csv("src/crawler_telegram/channels.csv", header=None).iloc[:, 0].to_list()
channels = set(channels)


for i, channel in enumerate(channels):
    print(f"{channel}")

    offset_post = 0
    num_ready_posts = 0
    df_messages, df_dates = [], []
    bar = tqdm.tqdm(total=total_posts_limit)
    while (
        total_posts_limit and num_ready_posts < total_posts_limit
    ):
        try:
            history = client(
                telethon.functions.messages.GetHistoryRequest(  
                    peer=channel,
                    offset_id=0,
                    offset_date=None,
                    add_offset=offset_post,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
            posts = history.messages
            for post in posts:
                message = post.message
                offset_post += 1
                
                if message != '':
                    df_messages.append(post.message)
                    df_dates.append(post.date)
                    
                    num_ready_posts += 1
                    bar.update(1)
                                
        except Exception as e:
            posts = []

        if len(posts) < limit:
            break
        
    df = pd.DataFrame(columns=["text", "date"])
    df["text"] = df_messages
    df["date"] = df_dates
    df.to_csv(os.path.join(data_path, channel + f"_{num_ready_posts}.csv"), index=False)

     
