> discord-music-bot is both a template and a download-and-run music bot for your discord server, made using Wavelinkcord and Nextcord.
> 
> It was made as a music bot that ANYONE - even those who are unfamiliar with coding can simply download and run it with as minimum trouble as possible.
> 
> It was also made as a template for anyone who wishes to make a more robust music bot that works with Youtube and Spotify. Feel free to use it!
> 



## Features <!-- omit in toc -->

- Slash commands using discord's Nextcord.
  - Simple commands like: play, volume, seek, skip, connect_to, pause, resume, leave, np (now playing), shuffle, forward, play_next, delete, queue, clear_queue.
  - Simple descriptions when using the slash commands on discord. Check them out!
- A lavalink based player, using Wavelinkcord - a fork by Zyb3rWolfi.


## Getting started <!-- omit in toc -->

- 1. First of, [install python](https://www.python.org/downloads/) or make sure you have it installed, by opening your Command Prompt (CMD) through searching "CMD" in your windows search bar, and writing "python" in it.
- 2. After making sure you have python installed, navigate to the folder you have the bot's files on and copy the path to the folder.
- 3. Write in your CMD:
     ```bash
     cd PATH_TO_FILE
     ```
     where PATH_TO_FILE is the path to the folder. For example C:/Discord-Music-BOt

     then:

     ```bash
     pip install -r requirements.txt
     ```
- 4. Now you should have everything you need to have installed! Now, we're gonna need to get your bot's token. If you still dont have it, don't worry:
     4.1. Head on over to [Discord's Developer Portal](https://discord.com/developers/docs/intro), log in, go to "Applications" and press 'New Application'. Give it a cool name.
     4.2. Head to "OAuth2" and click as follows (Those are the premissions the bot has. Currently, it needs Administrator permissions, and I plan to change it at a later date.)
     
     ![BotPermissions](https://i.imgur.com/ScHscuP.png)
     
     ![BotPremissions2](https://i.imgur.com/dIG7vWO.png)

     and there should be a URL at the bottom for you to get your bot to join the server.
     4.3. Head over to "Bot" and click on "Reset Token" and make sure you copy the token.
     
     ![BotToken](https://i.imgur.com/K8DluNV.png)
- 5. By now you should have the bot in your server and your token ready. Head over to 'tokens.py' in the bot's folder, and open it. You can open it through notepad if you don't have an IDE installed.
     Paste your bot's token between the commas like this:
     
     ![BotToken1](https://i.imgur.com/wEZLS2F.png)

     Make sure you don't close the file yet!
- 6. Now for the last part, you're gonna need a Lavalink server. I recommend using DarrenOfficial's [Lavalink-List](https://lavalink.darrennathanael.com/SSL/lavalink-with-ssl/) and picking a server.
     If you choose not to use a public server, you can host one yourself through [Lavalink](https://github.com/lavalink-devs/Lavalink).
     Simply put between the LAVALINK_IP the server's "Host address" and add ":" at the end with the port. For example, '1.2.3.4:433".
- 7. All thats left is running the bot. In your CMD (Make sure you're on the bot's directory) write "python main.py" and enjoy!



     
     
     
     
     
