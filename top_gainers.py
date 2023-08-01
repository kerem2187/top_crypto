import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# CoinMarketCap API anahtarını buraya girin
COINMARKETCAP_API_KEY = 'YOUR_COINMARKETCAP_API_KEY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Merhaba! CoinMarketCap üzerinden günlük en yükselen kripto paraların listesini almak için /topgainers komutunu kullanabilirsiniz.")

def get_top_gainers(update: Update, context: CallbackContext) -> None:
    limit = 5  # İstediğiniz en yüksek kripto sayısı

    # CoinMarketCap API
    cmc_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }

    params = {
        'limit': limit,
        'sort': 'percent_change_24h',
        'sort_dir': 'desc',
    }

    response = requests.get(cmc_api_url, headers=headers, params=params)
    cmc_data = response.json()

    # Format data
    top_gainers_list = []
    for cmc_coin in cmc_data['data']:
        name = cmc_coin['name']
        symbol = cmc_coin['symbol']
        percent_change_24h = cmc_coin['quote']['USD']['percent_change_24h']
        top_gainers_list.append(f"{name} ({symbol}): {percent_change_24h:.2f}%")

    update.message.reply_text("\n".join(top_gainers_list))

def main() -> None:
    # Telegram bot tokenını buraya girin
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    updater = Updater(TOKEN)

    # Komut işleyicileri ekleme
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("topgainers", get_top_gainers))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

