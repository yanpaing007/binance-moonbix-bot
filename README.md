## Setup

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
    pip install selenium
    ```

4. Copy [config.py.example]() and update the configuration as needed:
    ```sh
    cp config.py.example config.py
    ```

## Usage

Run the main script:
```sh
python main.py
