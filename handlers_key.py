from aiogram import F
from aiogram.filters import Command
from handlers import router, handle_ai_menu, handle_run, stop_command, echo_enabled, echo_disabled, handle_setup, \
    process_online_tv, cmd_start, info_command, handle_interval, handle_url_str, process_url_set_button, \
    process_list_urls_button, handle_admin, handle_help, handle_sound, handle_info_command, handle_check_status, \
    command_set_interval, handle_go_back, go_back_from_info, echo_bot

# ОБРАБОТЧИКИ КОМАНД:
def register_echo_handlers(dp: router):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(stop_command, F.text == "STOP")
    # dp.message.register(handle_reg_one, F.text == "REG")
    dp.message.register(handle_run, F.text == "RUN")
    dp.message.register(handle_ai_menu, F.text == "AI")
    dp.message.register(echo_enabled, F.text == "ON")
    dp.message.register(echo_disabled, F.text == "OFF")
    dp.message.register(handle_setup, F.text == "SETUP")
    dp.message.register(process_online_tv, F.text == "ONLINE")
    dp.message.register(info_command, F.text == "STR_INFO")
    dp.message.register(handle_interval, F.text == "INTERVAL")
    dp.message.register(handle_url_str, F.text == "URL_STR")
    dp.message.register(process_url_set_button, F.text == "URL_SET")
    dp.message.register(process_list_urls_button, F.text == "URL_LIST")
    dp.message.register(handle_admin, F.text == "ADMIN")
    dp.message.register(handle_help, F.text == "HELP")
    dp.message.register(handle_sound, F.text == "SOUND")
    dp.message.register(handle_info_command, F.text == "INFO")
    dp.message.register(handle_check_status, F.text == "CHECK")
    dp.message.register(command_set_interval, F.text == "SET")
    # dp.message.register(set_new_interval, StateFilter(IntervalSetting.waiting_for_interval))
    dp.message.register(handle_go_back, F.text == "BACK")
    dp.message.register(go_back_from_info, F.text == "MENU")
    dp.message.register(echo_bot, ~F.text.startswith("/"))  # echo_bot - *после* команд!