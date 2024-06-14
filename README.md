# [Discord Virtual Microphone](https://github.com/Vazgen005/discord-virtual-micro)

Discord Virtual Microphone is a bot that leverages AI from [Silero Models](https://github.com/snakers4/silero-models) to read out loud any text you type in Discord. This bot can be particularly useful for individuals without access to a physical microphone.

## Features

- **Read out loud any text you type in Discord.**
- **Multiple languages.** _(See [languages supported](https://github.com/snakers4/silero-models#text-to-speech))_
- **Multiple speakers.** _(See [speakers supported](https://github.com/snakers4/silero-models#text-to-speech))_
- **Transliteration.** _(See [transliteration supported](https://github.com/barseghyanartur/transliterate))_
- **Custom word pronunciation.** _(Using vo!set-word [word to replace] [replacement word] and vo!del-word [word to delete] to replace/delete a word in the dictionary)_
- **Auto link replacement.** _(Specify `link_replacement` in the `config.json`)_

## Disclaimer

By using this bot, you are automating your Discord Account.
> The automation of Discord Accounts also known as self-bots is a violation of Discord Terms of Service & Community Guidelines and will result in your account(s) being terminated. Discretion is adviced. I will not be responsible for your actions. Read about [Discord's Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines).

## Requirements

Before installation, ensure you have the following requirements installed:

1. [Python](https://www.python.org/downloads) 3.10 or newer
2. [pip](https://pypi.org/project/pip) (Usually comes with Python. If missing, install it [manually](https://pip.pypa.io/en/stable/installation)) or [pipx](https://pipx.pypa.io) (Recommended)
3. [Virtual Audio Cable](https://vb-audio.com/Cable)

## Installation

To install the bot, run the following commands in your terminal (cmd, powershell, bash, zsh, etc.):

1. **Install latest release using pip:**

   ```shell
   pip install https://github.com/Vazgen005/discord-virtual-micro/releases/latest/download/discord_virtual_micro.tar.gz
   ```

2. **Create a configuration file:**

   ```shell
   discord-virtual-micro
   ```

   For the first time, this will generate a `config.json` file in the current directory.\
   _(You can get current directory using `pwd` command.)_

3. **Configure the bot:**
   Open the `config.json` file and replace the placeholder values with your Discord token and the name of your virtual audio cable. \
   _You can also adjust other settings as per your preferences._

4. **Start the bot:**

   ```shell
   discord-virtual-micro
   ```

   The bot will now start running and listen for your text inputs in Discord.

## Usage

Once the bot is running, you can type your messages in any Discord channel, and the bot will read them out loud using the configured virtual audio cable.

To stop the bot, simply navigate to the terminal window and press `Ctrl+C`.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Vazgen005/discord-virtual-micro/issues) if you want to contribute.

## License

This project is licensed under the [GPL-3.0 license](LICENSE).

## Contact

If you have any questions or inquiries, feel free to contact [me](https://github.com/Vazgen005).
