import os
import configargparse

import pandas as pd
import telethon
import telethon.sync
import tqdm
import yaml

parser = configargparse.ArgParser()

parser.add_argument(
    "--config_path",
    type=str,
    default="src/crawler_telegram/telegram_config.yaml",
    help="credentials для telegram api"
)
parser.add_argument(
    "--data_dir",
    type=str,
    default="data/raw/telegram",
    help="куда сгружаем данные (временная заглушка)"
)
parser.add_argument(
    "--channels_path",
    type=str,
    default="src/crawler_telegram/channels.csv",
    help="каналы для парсинга"
)
parser.add_argument(
    "--total_posts_limit",
    type=int,
    default=10,
    help="сколько новостей выгрузить с каждого канала"
)

args = parser.parse_args()

with open(args.config_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    username = config["username"]

client = telethon.sync.TelegramClient(username, api_id, api_hash)
client.start()

limit = 1  
channels = pd.read_csv(args.channels_path, header=None).iloc[:, 0].to_list()
channels = set(channels)


for i, channel in enumerate(channels):
    print(f"{channel}")

    offset_post = 0
    num_ready_posts = 0
    df_messages, df_dates = [], []
    bar = tqdm.tqdm(total=args.total_posts_limit)
    while (
        args.total_posts_limit and num_ready_posts < args.total_posts_limit
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
    df.to_csv(os.path.join(args.data_dir, channel + f"_{num_ready_posts}.csv"), index=False)

     
