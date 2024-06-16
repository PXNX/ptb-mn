import logging
import re
from collections import defaultdict
from typing import List

import requests
from telegram import Update, ChatPermissions
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.helpers import mention_html

from config import WARN_LIMIT, ADMINS
from util.helper import reply_html, reply_photo, CHAT_ID, MSG_REMOVAL_PERIOD, delete, MSG_ID, admin_reply, remove, \
    remove_reply


def get_rules() -> List[str]:
    return [
        "1️⃣ Keine Beleidigung anderer Mitglieder.",
        "2️⃣ Kein Spam (mehr als drei einzelne Nachrichten oder Alben hintereinander weitergeleitet).",
        "3️⃣ Keine pornografischen Inhalte.",
        "4️⃣ Keine Aufnahmen von Leichen oder Schwerverletzen.",
        "5️⃣ Keine privaten Inhalte anderer Personen teilen."
    ]


def manage_warnings(update: Update, context: CallbackContext, increment: int):
    user_id = update.message.reply_to_message.from_user.id
    user_data = context.bot_data.setdefault("users", defaultdict(lambda: {"warn": 0}))
    user_data[user_id]["warn"] = max(0, user_data[user_id]["warn"] + increment)
    return user_data[user_id]["warn"]


@admin_reply
async def ban_user(update: Update, context: CallbackContext):
    logging.info(f"banning {update.message.reply_to_message.from_user.id} !!")
    await context.bot.ban_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id,
                                      until_date=1)
    await update.message.reply_to_message.reply_text(
        f"Aufgrund eines gravierenden Verstoßes habe ich {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} gebannt.")


@admin_reply
async def unwarn_user(update: Update, context: CallbackContext):
    logging.info(f"unwarning {update.message.reply_to_message.from_user.id} !!")

    context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = []

    await update.message.reply_to_message.reply_text(
        f"Dem Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} wurde alle Verwarnungen erlassen.")


@admin_reply
async def warn_user(update: Update, context: CallbackContext):
    logging.info(f"warning {update.message.reply_to_message.from_user.id} !!")

    if "users" not in context.bot_data or update.message.reply_to_message.from_user.id not in context.bot_data[
        "users"] or "warn" not in context.bot_data["users"][update.message.reply_to_message.from_user.id]:
        context.bot_data["users"] = {
            update.message.reply_to_message.from_user.id: {"warn": [update.message.reply_to_message.id]}}

    else:
        if update.message.reply_to_message.id in \
                context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]:
            msg = await update.message.reply_to_message.reply_text(
                "Der Nutzer wurde für diese Nachricht bereits verwarnt.")
            context.job_queue.run_once(delete, MSG_REMOVAL_PERIOD,
                                       {CHAT_ID: msg.chat_id, MSG_ID: msg.message_id})
            return

        context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"].append(
            update.message.reply_to_message.id)

    warn_amount = len(context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"])

    if warn_amount >= WARN_LIMIT:
        try:
            logging.info(f"restricting {update.message.reply_to_message.from_user.id} !!")
            await context.bot.restrict_chat_member(update.message.reply_to_message.chat_id,
                                                   update.message.reply_to_message.from_user.id,
                                                   ChatPermissions(can_send_messages=False))
        except TelegramError as e:
            logging.info(f"needs admin: {e}")

        await update.message.reply_to_message.reply_text(
            f"Aufgrund wiederholter Verstöße habe ich {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} die Schreibrechte genommen.")
        return
    else:

        warn_text = f"Der Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} hat die Warnung {warn_amount} von {WARN_LIMIT} erhalten."
        if len(context.args) == 0:
            warn_text = (
                f"Hey {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)}‼️ Das musste jetzt echt nicht sein. Bitte verhalte dich besser!"
                f"\n\n{warn_text}"
                f"\n\n<i>Mit /rules bekommst du eine Übersicht der Regeln dieser Gruppe.</i>")

        elif context.args[0].isnumeric():
            warn_text = f"{warn_text}\n\nGrund: {get_rules()[int(context.args[0]) - 1]}"
        else:

            warn_text = f"{warn_text}\n\nGrund: {' '.join(context.args)}"
        await update.message.reply_to_message.reply_text(warn_text)


@admin_reply
async def report_user(update: Update, _: CallbackContext):
    logging.info(f"reporting {update.message.reply_to_message.from_user.id} !!")
    r = requests.post(url="http://localhost:8080/reports",
                      json={
                          "user_id": update.message.reply_to_message.from_user.id,
                          "message": update.message.reply_to_message.text_html_urled,
                          "account_id": 1
                      })
    logging.info(r)
    await update.message.reply_to_message.reply_text(
        f"Der Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} wurde Tartaros-Antispam gemeldet.")


async def maps(update: Update, context: CallbackContext):
    await reply_html(update, context, "maps")

    # todo: collect list of losses


async def loss(update: Update, context: CallbackContext):
    await reply_html(update, context, "loss")


async def donbas(update: Update, context: CallbackContext):
    await reply_html(update, context, "donbas")


async def commands(update: Update, context: CallbackContext):
    await reply_html(update, context, "cmd")


async def genozid(update: Update, context: CallbackContext):
    await reply_html(update, context, "genozid")


async def peace(update: Update, context: CallbackContext):
    await reply_html(update, context, "peace")


async def short(update: Update, context: CallbackContext):
    await reply_html(update, context, "short")


async def stats(update: Update, context: CallbackContext):
    await reply_html(update, context, "stats")


async def bias(update: Update, context: CallbackContext):
    await reply_html(update, context, "bias")


async def sold(update: Update, context: CallbackContext):
    await reply_html(update, context, "sold")


@remove
async def ref(update: Update, context: CallbackContext):
    if link_match := re.search(r"([^\/]\w*\/\d+$)", update.message.text[4:]):
        link = link_match[0]
        logging.info(f"link REF: {link}")
        text = f"Ich habe dir mal was passendes aus unserem Kanal rausgesucht😊\n\n👉🏼 <a href='t.me/{link}'>{link}</a>"
        if update.message.reply_to_message:
            await update.message.reply_to_message.reply_text(
                f"Hey {update.message.reply_to_message.from_user.name}!\n{text}", disable_web_page_preview=False)
        else:
            await context.bot.send_message(update.message.chat_id, text, disable_web_page_preview=False)


async def sofa(update: Update, context: CallbackContext):
    await reply_photo(update, context, "sofa.jpg")


async def bot(update: Update, context: CallbackContext):
    await reply_photo(update, context, "bot.jpg")


async def mimimi(update: Update, context: CallbackContext):
    await reply_photo(update, context, "mimimi.jpg")


async def cia(update: Update, context: CallbackContext):
    await reply_photo(update, context, "cia.jpg")


async def duden(update: Update, context: CallbackContext):
    await reply_photo(update, context, "duden.jpg")


async def argu(update: Update, context: CallbackContext):
    await reply_photo(update, context, "argu.jpg")


async def vs(update: Update, context: CallbackContext):
    await reply_photo(update, context, "vs.jpg")


async def disso(update: Update, context: CallbackContext):
    await reply_photo(update, context, "disso.jpg")


async def front(update: Update, context: CallbackContext):
    await reply_photo(update, context, "front.png")


async def deutsch(update: Update, context: CallbackContext):
    await reply_photo(update, context, "deutsch.png")


async def pali(update: Update, context: CallbackContext):
    await reply_photo(update, context, "pali.jpg")


async def send_rules(update: Update, context: CallbackContext):
    await reply_html(update, context, "rules", "\n\n".join(get_rules()))


@remove_reply
async def notify_admins(update: Update, _: CallbackContext):
    logging.info(f"admin: {update.message}")

    if update.message.reply_to_message is not None:
        response = "".join(mention_html(a, "​") for a in ADMINS) + (
            "Danke für die Meldung dieses Posts, wir Admins prüfen das 😊"
            if update.message.reply_to_message.is_automatic_forward
            else "‼️ Ein Nutzer hat deine Nachricht gemeldet. Wir Admins prüfen das.\n\nDie Regeln diesr Gruppe findest du unter /rules."
        )
        await update.message.reply_to_message.reply_text(response)
