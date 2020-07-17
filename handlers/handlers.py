from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from addons.utils import logger
from commands import cmd


@run_async
def msg_handlers(dispatcher):
    dispatcher.add_error_handler(cmd.error_handler)
    dispatcher.add_handler(CommandHandler("start", cmd.start))
    dispatcher.add_handler(CommandHandler("cricbuzz", cmd.select_option))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.back_to_home, pattern=r"take_me_there"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.live_matches, pattern=r"live_matches"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.back_to_home, pattern=r"back_to_home"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.list_matches, pattern=r"list_matches"))  
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.match_info, pattern=r"match_info")) 
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.score_card, pattern=r"score_card")) 
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.players, pattern=r"players"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.commentary, pattern=r"commentary")) 
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.live_score, pattern=r"live_score"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.live_score, pattern=r"force_ref"))
    dispatcher.add_handler(CallbackQueryHandler(callback=cmd.stop_live, pattern=r"stop"))
    logger.info("loaded all handlers")