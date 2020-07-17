from score_utils import cric
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup ,InlineKeyboardButton
from addons.utils import logger
import time

class Commands:
    
    @run_async
    def start(self, update, context):
        update.message.reply_text(
           text = f"Hello {update.message.chat.first_name}\n_Im a simple cricbuzz bot by @W4RR10R which let you know the live cricket score and updates from_ `cricbuzz.com` _within the telegram. \n/cricbuzz - to get all available options._",
           reply_markup = InlineKeyboardMarkup([
             [ InlineKeyboardButton(text=f"Source code",url="https://github.com/CW4RR10R/CircBuzz-bot"),
              InlineKeyboardButton(text=f"Me",url="https://t.me/W4RR10R")],
              [InlineKeyboardButton(text=f"Take me there",callback_data="take_me_there")]
          ]),
          quote = True,
          parse_mode = "markdown"
        )

    @run_async
    def error_handler(self, update, context):
        logger.error(f"Error {context.error}")

    @run_async    
    def select_option(self, update, context):
        update.message.reply_text(
          text = "*Okay cool now select what you wanted from the following buttons*\n_Note: The available options are fetched from cricbuzz.com so all the datas are updated and maintained by them._",
          reply_markup = InlineKeyboardMarkup(buttons()),
          quote = True,
          parse_mode = "markdown"
          
        )

    @run_async    
    def back_to_home(self, update, context):
        update.callback_query.message.edit_text(
           text = "*Okay cool now select what you wanted from the following buttons*\n_Note: The available options are fetched from cricbuzz.com so all the datas are updated and maintained by them._",
           reply_markup = InlineKeyboardMarkup(buttons()),
           parse_mode = "markdown",
           quote = True
        )
        
    @run_async
    def live_matches(self, update, context):
        msg = update.callback_query.message.edit_text(
          text = cric.live_matches(),
          parse_mode="markdown",
          reply_markup = InlineKeyboardMarkup([
             [ InlineKeyboardButton(text=f"<<< Go back to home",callback_data=f"back_to_home")]
          ])
        )
        
    @run_async
    def list_matches(self, update, context):
        data = update.callback_query.data.split("-")[1]
        update.callback_query.message.edit_text(
            text = f"<code>Select a match 🏏</code>",
            parse_mode = "HTML",
            reply_markup = InlineKeyboardMarkup(cric.list_matches_buttons(data))       
        )
        
    @run_async
    def match_info(self, update, context):
        match_id = update.callback_query.data.split("-")[1]
        msg = cric.match_info(match_id)
        update.callback_query.message.edit_text(
             text=msg,
             parse_mode="markdown",
             reply_markup = InlineKeyboardMarkup([
             [ InlineKeyboardButton(text=f"<<< Go back",callback_data=f"list_matches-match_info")]
          ])
        )
    
    
    @run_async
    def players(self, update, context):
        match_id = update.callback_query.data.split("-")[1]
        msg = cric.players(match_id)
        update.callback_query.message.edit_text(
             text=f"`{msg}`",
             parse_mode="markdown",
             reply_markup = InlineKeyboardMarkup([
             [ InlineKeyboardButton(text=f"<<< Go back",callback_data=f"list_matches-players")]
          ])
        )
        
    @run_async
    def score_card(self, update, context):
        match_id = update.callback_query.data.split("-")[1]
        msg = cric.score_card(match_id)
        update.callback_query.message.edit_text(
             text=msg,
             parse_mode="HTML",
             reply_markup = InlineKeyboardMarkup([
             [ InlineKeyboardButton(text=f"<<< Go back",callback_data=f"list_matches-score_card")]
          ])
        )
    
    
    @run_async
    def commentary(self, update, context):
        match_id = update.callback_query.data.split("-")[1]
        cmm = cric.commentary(match_id)    
        splitted = [cmm[i:i+4096] for i in range(0, len(cmm), 4096)]
        markup = None
        for i,message in enumerate(splitted):
            if len(splitted)-1 == i:
                markup = InlineKeyboardMarkup([
                  [ InlineKeyboardButton(text=f"<<< Go back",callback_data=f"list_matches-commentary")]
                ])
            update.callback_query.message.reply_text(
                  text=message,
                  parse_mode="HTML",
                  reply_markup = markup
            )        
                 
    @run_async
    def live_score(self, update, context):
        match_id=update.callback_query.data.split("-")[1]
        cric.live_score(update.callback_query.message,match_id)
        
    @run_async
    def stop_live(self, update, context):
        cric.run = False


cmd = Commands()

def buttons():
    btns = [
         [ InlineKeyboardButton(text=f"Live Matches",callback_data=f"live_matches"),
           InlineKeyboardButton(text=f"Match Info",callback_data=f"list_matches-match_info")
         ],
         [ InlineKeyboardButton(text=f"Live Score",callback_data=f"list_matches-live_score"),
           InlineKeyboardButton(text=f"Score Card",callback_data=f"list_matches-score_card")
         ],
         [ InlineKeyboardButton(text=f"Players",callback_data=f"list_matches-players"),
           InlineKeyboardButton(text=f"Commentary",callback_data=f"list_matches-commentary")
         ]        
      ]
    return btns
