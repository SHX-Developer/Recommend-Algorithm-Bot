from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#  INLINE
action_inline = InlineKeyboardMarkup()
action_inline.row(InlineKeyboardButton(text = "❤️", callback_data = "like"),
                  InlineKeyboardButton(text = "👎", callback_data = "dislike"))
action_inline.row(InlineKeyboardButton(text = "Next", callback_data = "next"))
