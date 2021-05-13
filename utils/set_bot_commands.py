from aiogram import types

from loader import bot


async def set_default_commands(dp):
    await bot.set_my_commands([
        types.BotCommand("/test", "Run tests"),
        types.BotCommand("/items", "List of items"),
        types.BotCommand("/menu", "Cryptocurrencies menu"),
        types.BotCommand("/create_post", "Create post in channel or in our group"),
        types.BotCommand("/channels", "List of channels to subscribe"),
        types.BotCommand("/set_photo", "Set photo of group"),
        types.BotCommand("/set_title", "Set title of group"),
        types.BotCommand("/read_only", "Run read only mode for user"),
        types.BotCommand("/del_read_only", "Stop read only mode for user"),
        types.BotCommand("/ban", "Ban user"),
        types.BotCommand("/unban", "Unban user"),
        types.BotCommand("/get_loc", "Get your location for show nearest marketplace"),
        types.BotCommand("/callback", "Get your contacts for callback"),
        types.BotCommand("/invoices", "Get invoice for product"),
        types.BotCommand("/qiwi_pay", "Make qiwi payment"),
        types.BotCommand("/btc_pay", "Make btc payment"),
        types.BotCommand("/add_email", "Add user email to base"),
        types.BotCommand("/add_item", "Add new item (only admin)"),
        types.BotCommand("/tell_all", "Add new item (only admin)"),
        types.BotCommand("/buy_items", "Buy items from shop"),
        types.BotCommand("/support", "Write in support"),
        types.BotCommand("/support_call", "Call in support"),


    ])