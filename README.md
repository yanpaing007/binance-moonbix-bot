## Setup

- [BotLink](https://t.me/Binance_Moonbix_bot/start?startApp=ref_5612706767&startapp=ref_5612706767&utm_medium=web_share_copy)

1. Clone the repository:
    ```sh
    git clone https://github.com/yanpaing007/binance-moonbix-bot.git
    cd binance-moonbix-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install selenium colorlog
    ```

4. Copy [config.py.example]() and update the configuration as needed:
    ```sh
    cp config.py.example config.py
    ```
## How to get bot iframe URL
- Go to binance bot
- Inspect the page and with selector click binance bot to find {ifram src="your link}
- Copy the link and paste it in the config.py

## Usage

Run the main script:
```sh
python main.py
