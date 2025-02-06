import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

TOKEN = "7929013012:AAHoQi8yEWYNL0uxJLwpMSkCdx_epjjtAFQ"

players = []
roles = []
player_roles = {}
words = ["Olma", "Banan", "Gilos", "Telefon", "Mashina", "Daryo", "Doktor", "Futbol"]  # Kichik ro'yxat
word_for_game = ""
imposter_id = None
eliminated_players = set()
true_votes = 0
false_votes = 0

# O'yinga qo'shilish
def join_game(update: Update, context: CallbackContext):
    player = update.message.from_user.id
    if player not in players:
        if len(players) < 6:
            players.append(player)
            update.message.reply_text("Siz o‘yinga qo‘shildingiz! O‘yin boshlanishini kuting.")
        else:
            update.message.reply_text("O‘yin to‘liq. Maksimal 6 ta ishtirokchi bo‘lishi mumkin.")
    else:
        update.message.reply_text("Siz allaqachon o‘yinda ishtirok etmoqdasiz.")

# O'yinni boshlash
def start_game(update: Update, context: CallbackContext):
    global players, player_roles, words, word_for_game, imposter_id, eliminated_players

    if len(players) < 4:
        update.message.reply_text("Kamida 4 ishtirokchi kerak. O‘yin boshlanmaydi.")
        return
    
    update.message.reply_text("O‘yin 10 soniyadan keyin boshlanadi. Ishtirok etmoqchi bo‘lganlar qo‘shilsin!")
    time.sleep(10)

    if len(players) < 4:
        update.message.reply_text("Yetarli ishtirokchilar yo‘q. O‘yin boshlanmaydi.")
        return
    
    roles = ['personaj'] * (len(players) - 1) + ['imposter']
    random.shuffle(roles)
    player_roles = dict(zip(players, roles))
    word_for_game = random.choice(words)
    eliminated_players.clear()

    for player, role in player_roles.items():
        if role == "imposter":
            imposter_id = player
            context.bot.send_message(chat_id=player, text="Siz Impostersiz! So‘zni bilmayapsiz, diqqat bilan tinglang.")
        else:
            context.bot.send_message(chat_id=player, text=f"Siz personajsiz! Sizning so‘zingiz: {word_for_game}.")

    update.message.reply_text("O‘yin boshlandi! Ishtirokchilar gaplasha boshlaydi.")

# Imposter "Topdim" tugmachasini bosganda
def imposter_found(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id == imposter_id:
        query.message.reply_text("Qanday so‘z ekanini yozing:")

# Imposter taxmin qilgan so‘zni yuborganda
def imposter_guess_word(update: Update, context: CallbackContext):
    global imposter_guess

    if update.message.from_user.id == imposter_id:
        imposter_guess = update.message.text
        update.message.reply_text("Sizning taxminingiz qabul qilindi.")

        # Guruhga anonim tarzda tashlash
        context.bot.send_message(chat_id=update.message.chat_id, text=f"⚠️ Anonim xabar: Imposter so‘zni {imposter_guess} deb taxmin qildi.")

        # True / False tugmachalari
        keyboard = [
            [InlineKeyboardButton("✅ True", callback_data="true_vote")],
            [InlineKeyboardButton("❌ False", callback_data="false_vote")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Imposter to‘g‘ri topdimi?", reply_markup=reply_markup)

# Ovoz berish natijalari
def vote_handler(update: Update, context: CallbackContext):
    global true_votes, false_votes
    query = update.callback_query

    if query.data == "true_vote":
        true_votes += 1
    elif query.data == "false_vote":
        false_votes += 1

    query.answer("Sizning ovozingiz qabul qilindi.")

    if true_votes + false_votes == len(players) - len(eliminated_players):
        finish_voting(update)

# Ovoz natijalarini hisoblash
def finish_voting(update: Update):
    global true_votes, false_votes

    if true_votes > false_votes:
        update.message.reply_text("✅ Imposter g‘alaba qozondi!")
    else:
        update.message.reply_text("❌ Personajlar g‘alaba qozondi!")

    true_votes = 0
    false_votes = 0

# Botni ishga tushirish
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start_game", start_game))
    dp.add_handler(CommandHandler("join", join_game))
    dp.add_handler(CallbackQueryHandler(imposter_found, pattern="found_word"))
    dp.add_handler(CallbackQueryHandler(vote_handler, pattern="true_vote|false_vote"))
    dp.add_handler(MessageHandler(Filters.text & Filters.private, imposter_guess_word))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
