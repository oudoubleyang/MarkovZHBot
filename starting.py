import os
import gzip
import botCache
import markovify
from baseTools import mkdir
from diskIO import write_msg, write_stat
from botSession import markov, scheduler, logger
from botInfo import bot_url, cache_size, large_size
from botTools import reset_cache, reset_triggered_user, remove_inactive_chats


def set_frp(url, path=None):
    return markov.set_webhook(url, path)


def pre_model(size=cache_size, large=large_size):
    files = []
    for i in os.listdir('data/text'):
        if os.path.isfile(f'data/text/{i}') and os.path.getsize(f'data/text/{i}') > size:
            files.append(f'data/text/{i}')
    for i in files:
        chat_id = int(os.path.splitext(i)[0].replace('data/text/', ''))
        print(f'[INFO] Generating cached Markov model for chat {chat_id}.')
        with gzip.open(i, 'rb') as f:
            if os.path.getsize(i) > large:
                botCache.models[chat_id] = markovify.Text(f.read().decode('utf-8'), retain_original=False)
            else:
                botCache.models[chat_id] = markovify.Text(f.read().decode('utf-8'))
        print(f'[INFO] Generated.')


def starting():
    mkdir(['data', 'stat'])
    set_frp(bot_url)
    pre_model()
    scheduler.add_job(write_stat, 'cron', minute='*/30')
    scheduler.add_job(write_msg, 'cron', minute='*/15')
    scheduler.add_job(reset_cache, 'cron', hour=0, minute=2)
    scheduler.add_job(remove_inactive_chats, 'cron', hour=0, minute=3)
    scheduler.add_job(reset_triggered_user, 'cron', minute=1)
    scheduler.start()
    logger.info('[INFO] Starting fine.')
