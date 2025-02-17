from tokens import *
from nodes import *
from commands import *


bot_version = "0.0.1"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())
    wavelink.Player.autoplay = True


# on node
async def on_node():
    node: wavelink.Node = wavelink.Node(uri=LAVALINK_IP, password=LAVALINK_PASSWORD)
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    print("Connected")
    await bot.change_presence()




# /Test
@bot.slash_command(guild_ids=[])
async def test(interaction : Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    print(f"vc: {bool(vc)}")
    print(f"connected: {vc.is_connected()}")




bot.run(BOTTOKEN)
