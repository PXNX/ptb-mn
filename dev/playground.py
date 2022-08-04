import traceback

from telegram import Update
from telegram.ext import ContextTypes

# from twitter import  tweet_text,tweet_file
from data.lang import languages
from util.translation import translate


async def flag_to_hashtag_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("-------\n\nTEST\n\n-------")
    await update.message.reply_text("-------\n\nTEST\n\n-------")
    try:

        #  await tweet_file(update, context)
        for lang in languages:
            await update.message.reply_text(translate(lang.lang_key, update.message.text, lang.lang_key_deepl))

    except Exception as e:
        await update.message.reply_text("-------\n\nTEST FAIL\n\n-------")
        await update.message.reply_text(
            f"-------\n\nEXCEPTION: {e}\n\nTRACE: {traceback.format_exc()}\n\n-------"
        )

    await update.message.reply_text("-------\n\nTEST DONE\n\n-------")