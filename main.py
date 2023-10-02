import nextcord
from tokens import *
from nodes import *
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, tasks
from nextcord.shard import EventItem
import wavelinkcord as wavelink



#------- Helper functions ---------- #

def format_duration(milliseconds):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000

    # Calculate hours, minutes, and seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    formatted_duration = ""

    # Add hours if they are greater than zero
    if hours > 0:
        formatted_duration += f"{int(hours)}:"
    
    # Always add minutes and seconds in the format "minutes:seconds"
    formatted_duration += f"{int(minutes):02}:{int(seconds):02}"

    return formatted_duration


def deformat_duration(time_str):
    #Convets to milisecodns from 00:00:00 format.
    parts = time_str.split(':')
    total_ms = 0

    if len(parts) == 3:  # Format: "00:00:00" (hours, minutes, seconds)
        hours, minutes, seconds = map(int, parts)
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000
    elif len(parts) == 2:  # Format: "00:00" (minutes, seconds)
        minutes, seconds = map(int, parts)
        total_ms = (minutes * 60 + seconds) * 1000
    elif len(parts) == 1:  # Format: "00" (seconds)
        total_ms = int(parts[0]) * 1000

    return total_ms




# ----------------------------- #


bot_version = "0.0.1"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix="!", intents = intents)


# recent_interaction_channel = None
# @bot.event
# async def on_interaction(interaction):
#     global recent_interaction_channel
#     recent_interaction_channel = interaction.channel


# bot.load_extension("cogs")
# bot.setup(recent_interaction_channel)

@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())
    wavelink.Player.autoplay = True

#test1

# on node
async def on_node():
    node: wavelink.Node = wavelink.Node(uri="54.38.198.24:88", password="stonemusicgay")
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    print("Connected")
    await bot.change_presence()




#test
@bot.slash_command(guild_ids=[])
async def test(interaction : Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    print(f"vc: {bool(vc)}")
    print(f"connected: {vc.is_connected()}")



#------------------- COMMANDS ------------------------#


#play
@bot.slash_command(guild_ids=[], description="Play a song! or just que it up.")
async def play(interaction : Interaction, search : str):

    vc: wavelink.Player = interaction.guild.voice_client
    query = await wavelink.YouTubeTrack.search(search)

    if not query:
        await interaction.response.send_message(f"I couldn't find a video titled '{search}'")
        return
    
    query = query[0]

    # Check if either user or bot are connected to a VC
    if not interaction.user.voice and not vc:
        await interaction.response.send_message(f"You or the bot must be in a channel to use this command.")
        return
    
    # User is in channel
    if interaction.user.voice: 
        destination = interaction.user.voice.channel

    # The bot isnt connected
    if not vc:
        try:
            vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
        except wavelink.exceptions.InvalidChannelPermissions as e:
            await interaction.response.send_message(f"Something went wrong. I could not enter the voice channel.")
            return
        except Exception as e:
            # Handle other exceptions here if needed
            await interaction.response.send_message(f"Something went wrong. I could not enter the voice channel. Error: {e}")
            return
    
    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(query)

    else: #queue not empty
        await vc.queue.put_wait(query)

    embed = nextcord.Embed(title="Added to the queue:", color=nextcord.Color.green())
    embed.add_field(name="\u200B", value=f":white_check_mark: [{query.title}]({query.uri})")
    embed.set_thumbnail(query.thumbnail)
    await interaction.response.send_message(embed=embed)



#volume
@bot.slash_command(guild_ids=[], description="Set the volume to a certain percentage (0-100).")
async def volume(interaction : nextcord.Interaction, volume_percent : int):

    vc: wavelink.Player = interaction.guild.voice_client
    if 0 <= volume_percent <= 100:
        await vc.set_volume(volume_percent)
        await interaction.response.send_message(f"Setting volume to {volume_percent}..")
    else:
        await interaction.response.send_message(f"The volume must be between 0-100!")



#seek
@bot.slash_command(guild_ids=[], description="Seek to a certain time in the current song.")
async def seek(interaction : nextcord.Interaction, time: str):
    
    vc: wavelink.Player = interaction.guild.voice_client
    toSeek = deformat_duration(time)
    
    if not vc or not vc.is_playing():
    
        await interaction.response.send_message(f"The bot is not currently playing music.")
        return
    

    if vc.current.duration >= toSeek >= 0:
        await vc.seek(toSeek)
        await interaction.response.send_message(f"Seeking to {time}..")

    else:
        await interaction.response.send_message(f"Illegal time! The time must be between 0 to {format_duration(vc.current.duration)}")



#skip
@bot.slash_command(guild_ids=[], description="Skip the current song.")
async def skip(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There are no songs currently playing.")
    
    else:
        await vc.stop()
        await interaction.response.send_message(f"Song was skipped!")



#move_to
@bot.slash_command(guild_ids=[], description="Connect or move the bot to a specified voice channel.")
async def connect_to(interaction: nextcord.Interaction,
                  channel: nextcord.VoiceChannel = SlashOption(name="channel",
                                             description="Select a voice channel",
                                             required=True,
                                             )
                                             ):
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc:
        await channel.connect(cls=wavelink.Player)
        await interaction.response.send_message(f"Connected to '{channel.name}'")
    else:
        await vc.move_to(channel)
        await interaction.response.send_message(f"Moved to '{channel.name}'")
    



#pause
@bot.slash_command(guild_ids=[], description="Pause the current song.")
async def pause(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There is no song currently playing.")


    if vc.is_playing():
        
        await vc.pause()
        await interaction.response.send_message(f"Song has been paused.")
        
    print(f"is_playing: {vc.is_playing()}")

#resume
@bot.slash_command(guild_ids=[], description="Resume the currently paused song.")
async def resume(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There are no songs paused right now.")
        return
    
    await vc.resume()
    await interaction.response.send_message(f"Song is resumed.")

#roni
@bot.slash_command(guild_ids=[], description="Recieve a beautiful picture of Roni.")
async def roni(interaction : nextcord.Interaction):
    await interaction.response.send_message(f"https://i.imgur.com/mbHUJEB.png")

#disconnect / leave
@bot.slash_command(guild_ids=[], description="Make the bot leave.. its ok.. He'll be okay..")
async def leave(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client  
    if not vc:
        await interaction.response.send_message(f"Leave what bruh?")
        return     
    await vc.disconnect()
    await interaction.response.send_message(f"Goodbye.. sadge..")


#now playing / np
@bot.slash_command(guild_ids=[], description="Displays the current song playing..")
async def np(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There is no song currently playing..")
        return

    embed = nextcord.Embed(title=vc.current.title, url=vc.current.uri)
    embed.set_thumbnail(vc.current.thumbnail)
    embed.add_field(name=f"", value=f"{format_duration(vc.position)}**/**{format_duration(vc.current.length)}")

    await interaction.response.send_message(embed=embed)   


#shuffle
@bot.slash_command(guild_ids=[], description="Shuffles the queue.")
async def shuffle(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or vc.queue.is_empty():
        await interaction.response.send_message(f"The queue is currently empty.:")   
        return

    vc.queue.shuffle()
    await interaction.response.send_message(f"The queue has been shuffled :)")



#forward
@bot.slash_command(guild_ids=[], description="Forwards the song by the inputted time.")
async def forward(interaction : nextcord.Interaction, time : str):
    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There is no song currently playing.")   
        return
    
    curr_time = vc.position
    to_forward = deformat_duration(time) + curr_time


    await vc.seek(to_forward)
    await interaction.response.send_message(f"Seeking to {format_duration(to_forward)}..")
    

    

#put next
@bot.slash_command(guild_ids=[] , description="Enqueue a song or playlist in the front of the queue.")
async def play_next(interaction : nextcord.Interaction, search : str):

    vc: wavelink.Player = interaction.guild.voice_client
    query = (await wavelink.YouTubeTrack.search(search))[0]


    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There is no song currently playing.. just use 'play' ")
        return

    if query:
         
        vc.queue.put_at_front(query)
        await interaction.response.send_message(f"Added {query.title} as the next song.")

    else:
        await interaction.response.send_message(f"Could not find the specified song..")



#delete
@bot.slash_command(guild_ids=[], description="Delete a song at a certain index. Tip: use /queue to find it.")
async def delete(interaction : nextcord.Interaction, index: int):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"There is no song currently playing..")

    try:
        name = (vc.queue[index - 2]).title
        del vc.queue[index - 2]
        await interaction.response.send_message(f"Deleted the song at index '{index}' named **'{name}'**.")
    except:
        await interaction.response.send_message(f"There is no such index.")

#clear_queue
@bot.slash_command(guild_ids=[], description="Clears the bot's queue.")
async def clear(interaction : nextcord.Interaction):
    
    vc: wavelink.Player = interaction.guild.voice_client

    if not vc or not vc.is_playing():
        await interaction.response.send_message(f"The queue is currently empty.")
        return
    
    vc.queue.clear()
    await interaction.response.send_message(f"The queue has been cleared.")



#queue
@bot.slash_command(guild_ids=[], description="Displays the bot's queue.")
async def queue(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if vc is None:

        await interaction.response.send_message("Bot is not connected to a voice channel.")
        return
    
    if vc.is_playing():

        embed = nextcord.Embed(title="Queue")
        embed.set_thumbnail(vc.current.thumbnail)
        embed.add_field(name="\u200B",value=f":arrow_forward: **1. [{vc.current.title}]({vc.current.uri}) - {format_duration(vc.current.duration)}**", inline=True)
        songs_duration = vc.current.duration

        if not vc.queue.is_empty:

            song_counter = 1
            queue = vc.queue.copy()
            songs = DoublyLinkedList()

            for song in queue:            
                songs_duration += song.duration
                song_counter += 1
                songs.append(song)
                embed.add_field(name="\u200B",value=f"{song_counter}. [{song.title}]({song.uri}) - {format_duration(song.duration)}", inline=False)
        embed.description = f"Total queue duration: {format_duration(songs_duration)}"
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Queue is empty")



bot.run(BOTTOKEN)
