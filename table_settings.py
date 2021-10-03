from sheets_handler import get_info
import datetime
import time
# переменные с настройками, чтобы программа не докапывалась до сервера

settings = {"z_amount_tickers": 0, "portfolio_amount_tickers": 0, "step": 0, "z_ticker": None, "z_zacks": None,
               "z_vgm": None, "z_category": None, "z_from": None, "z_to": None, "z_recom": None,
               "z_avol": None, "z_vol": None, "z_sma50": None, "z_sma200": None, "p_ticker": None, "p_zacks": None,
               "p_vgm": None, "p_category": None, "p_from": None, "p_to": None, "p_vol": None, "p_avol": None,
               "p_sma50": None, "p_sma200": None, "sectors_industries": 0, "z_sectors": None, "z_industries": None}


def load_settings():
    global settings
    buffer = get_info("Настройки", "B", 1, "B", 30)[0]
    del buffer[3]
    del buffer[14]
    del buffer[24]
    i = 0
    for setting in settings:
        settings[setting] = buffer[i]
        i += 1

