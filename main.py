import requests.packages.urllib3
import finviz
import time
import table_settings
from sheets_handler import get_info, put_info
from table_settings import load_settings, settings
import get_info_functions
import date
import schedule

# для корректной работы finviz
requests.packages.urllib3.disable_warnings()

# для выгрузки данных в гугл таблицу
Recom = []
Volume = []
Average_Volume = []
Zacks_rank = []
VGM = []
Date_category = []
price_from = []
price_to = []
SMA50 = []
SMA200 = []
Sectors = []
Industries = []


# заполнение таблицы z-stocks
def z_stocks(first, second):
    try:
        tickers = get_info("Z-Stocks", settings["z_ticker"], str(first), settings["z_ticker"], str(second))
        print("Тикеры получены из диапазона " + '\'Z-Stocks\'!' + settings["z_ticker"] + str(first) + ':' +
              settings["z_ticker"] + str(second))

        # Получение значений
        for i in tickers[0]:
            try:
                Recom.append(finviz.get_stock(i)["Recom"])
                print("Получено значение Recom для " + i)
            except:
                Recom.append("Тикера нет в базе")
            try:
                Volume.append(str(finviz.get_stock(i)["Volume"]).replace(",", ""))
                print("Получено значение Volume для " + i)
            except:
                Volume.append("Тикера нет в базе")
            try:

                if str(finviz.get_stock(i)["Avg Volume"])[-1] == "M":
                    Average_Volume.append(
                        int(str(finviz.get_stock(i)["Avg Volume"]).replace("M", "").replace(".", "")) * 10000)
                elif str(finviz.get_stock(i)["Avg Volume"])[-1] == "K":
                    Average_Volume.append(
                        int(str(finviz.get_stock(i)["Avg Volume"]).replace("K", "").replace(".", "")) * 10)
                else:
                    Average_Volume.append(int(str(finviz.get_stock(i)["Avg Volume"])))
                print("Получено значение Average Volume для " + i)
            except:
                Average_Volume.append("Тикера нет в базе")
            try:
                Zacks_rank.append(get_info_functions.zacks_rank(i))
                print("Получено значение Zacks_Rank для " + i)
            except:
                Zacks_rank.append("Тикера нет в базе")
            try:
                VGM.append(get_info_functions.vgm(i))
                print("Получено значение VGM для " + i)
            except:
                VGM.append("Тикера нет в базе")
            try:
                price_target = get_info_functions.modified_get_analyst_price_targets(i)
                Date_category.append(
                    str(date.normalize_date(price_target[0]["date"])) + " " + str(price_target[0]["category"]))
                print("Получено значение Date из analyst price targets для " + i)
                price_from.append(str(price_target[0]["price_from"]))
                print("Получено значение Price from из analyst price targets для " + i)
                price_to.append(str(price_target[0]["price_to"]))
                print("Получено значение Price to из analyst price targets для " + i)
            except:
                Date_category.append("Тикера нет в базе")
                price_from.append("Тикера нет в базе")
                price_to.append("Тикера нет в базе")
            try:
                SMA200.append(finviz.get_stock(i)['SMA200'])
                print("Получено значение SMA200 для " + i)
            except:
                SMA200.append("Тикера нет в базе")
            try:
                SMA50.append(finviz.get_stock(i)['SMA50'])
                print("Получено значение SMA 50 для " + i)
            except:
                SMA50.append("Тикера нет в базе")
            finviz.main_func.STOCK_PAGE.clear()
            if settings["sectors_industries"] == "1":
                Sectors.append(get_info_functions.get_sector(i))
                Industries.append(get_info_functions.get_industry(i))
                print(f"Получены значения industry и sector для {i}")
        if settings["sectors_industries"] == "1":
            put_info("Z-Stocks", settings["z_industries"], str(first), settings["z_industries"], str(second),
                     [Industries])
            put_info("Z-Stocks", settings["z_sectors"], str(first), settings["z_sectors"], str(second), [Sectors])

        put_info("Z-Stocks", settings["z_recom"], str(first), settings["z_recom"], str(second), [Recom])
        put_info("Z-Stocks", settings["z_vol"], str(first), settings["z_vol"], str(second), [Volume])
        put_info("Z-Stocks", settings["z_avol"], str(first), settings["z_avol"], str(second), [Average_Volume])
        put_info("Z-Stocks", settings["z_zacks"], str(first), settings["z_zacks"], str(second), [Zacks_rank])
        put_info("Z-Stocks", settings["z_vgm"], str(first), settings["z_vgm"], str(second), [VGM])
        put_info("Z-Stocks", settings["z_category"], str(first), settings["z_category"], str(second), [Date_category])
        put_info("Z-Stocks", settings["z_from"], str(first), settings["z_from"], str(second), [price_from])
        put_info("Z-Stocks", settings["z_to"], str(first), settings["z_to"], str(second), [price_to])
        put_info("Z-Stocks", settings["z_sma50"], str(first), settings["z_sma50"], str(second), [SMA50])
        put_info("Z-Stocks", settings["z_sma200"], str(first), settings["z_sma200"], str(second), [SMA200])
        print("Значения записаны в Z-Stocks")
    except:
        print("Ошибка")


# заполнение таблицы с портфелем
def portfolio(first, second):
    try:
        tickers = get_info("💼", settings["p_ticker"], first, settings["p_ticker"], second)
        print("Тикеры получены из диапазона " + '\'💼\'!A' + str(first) + ':A' + str(second))

        # Получение значений
        for i in tickers[0]:
            try:
                Volume.append(str(finviz.get_stock(i)["Volume"]).replace(",", ""))
                print("Получено значение Volume для " + i)
            except:
                Volume.append("Тикера нет в базе")
            try:

                if str(finviz.get_stock(i)["Avg Volume"])[-1] == "M":
                    Average_Volume.append(
                        int(str(finviz.get_stock(i)["Avg Volume"]).replace("M", "").replace(".", "")) * 10000)
                elif str(finviz.get_stock(i)["Avg Volume"])[-1] == "K":
                    Average_Volume.append(
                        int(str(finviz.get_stock(i)["Avg Volume"]).replace("K", "").replace(".", "")) * 10)
                else:
                    Average_Volume.append(int(str(finviz.get_stock(i)["Avg Volume"])))
                print("Получено значение Average Volume для " + i)
            except:
                Average_Volume.append("Тикера нет в базе")
            try:
                Zacks_rank.append(get_info_functions.zacks_rank(i))
                print("Получено значение Zacks_Rank для " + i)
            except:
                Zacks_rank.append("Тикера нет в базе")
            try:
                VGM.append(get_info_functions.vgm(i))
                print("Получено значение VGM для " + i)
            except:
                VGM.append("Тикера нет в базе")
            try:
                price_target = get_info_functions.modified_get_analyst_price_targets(i)
                Date_category.append(
                    str(date.normalize_date(price_target[0]["date"])) + " " + str(price_target[0]["category"]))
                print("Получено значение Date из analyst price targets для " + i)
                price_from.append(str(price_target[0]["price_from"]))
                print("Получено значение Price from из analyst price targets для " + i)
                price_to.append(str(price_target[0]["price_to"]))
                print("Получено значение Price to из analyst price targets для " + i)
            except:
                Date_category.append("Тикера нет в базе")
                price_from.append("Тикера нет в базе")
                price_to.append("Тикера нет в базе")
            try:
                SMA200.append(finviz.get_stock(i)['SMA200'])
                print("Получено значение SMA200 для " + i)
            except:
                SMA200.append("Тикера нет в базе")
            try:
                SMA50.append(finviz.get_stock(i)['SMA50'])
                print("Получено значение SMA 50 для " + i)
            except:
                SMA50.append("Тикера нет в базе")
            finviz.main_func.STOCK_PAGE.clear()

        put_info("💼", settings["p_vol"], str(first), settings["p_vol"], str(second), [Volume])
        put_info("💼", settings["p_avol"], str(first), settings["p_avol"], str(second), [Average_Volume])
        put_info("💼", settings["p_zacks"], str(first), settings["p_zacks"], str(second), [Zacks_rank])
        put_info("💼", settings["p_vgm"], str(first), settings["p_vgm"], str(second), [VGM])
        put_info("💼", settings["p_category"], str(first), settings["p_category"], str(second), [Date_category])
        put_info("💼", settings["p_from"], str(first), settings["p_from"], str(second), [price_from])
        put_info("💼", settings["p_to"], str(first), settings["p_to"], str(second), [price_to])
        put_info("💼", settings["p_sma50"], str(first), settings["z_sma50"], str(second), [SMA50])
        put_info("💼", settings["p_sma200"], str(first), settings["p_sma200"], str(second), [SMA200])

    except:
        print("Ошибка")


def superfunc():
    for i in range(2, int(settings["z_amount_tickers"]), int(settings["step"])):
        first = i
        last = i + int(settings["step"]) - 1
        if last > int(settings["z_amount_tickers"]):
            last = int(settings["z_amount_tickers"])
        z_stocks(first, last)
        Recom.clear()
        Volume.clear()
        Average_Volume.clear()
        Zacks_rank.clear()
        VGM.clear()
        Date_category.clear()
        price_from.clear()
        price_to.clear()
        SMA50.clear()
        SMA200.clear()
        Sectors.clear()
        Industries.clear()
    for i in range(2, int(settings["portfolio_amount_tickers"]), int(settings["step"])):
        first = i
        last = i + int(settings["step"]) - 1
        if last > int(settings["portfolio_amount_tickers"]):
            last = int(settings["portfolio_amount_tickers"])
        portfolio(first, last)
        Recom.clear()
        Volume.clear()
        Average_Volume.clear()
        Zacks_rank.clear()
        VGM.clear()
        Date_category.clear()
        price_from.clear()
        price_to.clear()
        SMA50.clear()
        SMA200.clear()


def every_day_func():
    load_settings()
    superfunc()


schedule.every().day.at("05:55").do(load_settings)
schedule.every().day.at("06:00").do(every_day_func)

if __name__ == '__main__':
    while True:
        load_settings()
        schedule.run_pending()
        time.sleep(1)
