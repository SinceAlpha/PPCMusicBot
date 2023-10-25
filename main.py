import discord
from discord.ext import commands
import youtube_dl

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


class Queue:
    def __init__(self):
        self.queue = []

    def add_to_queue(self, url):
        self.queue.append(url)

    def get_next(self):
        return self.queue.pop(0) if self.queue else None


queue = Queue()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, url):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client.is_playing() or voice_client.is_paused():
        queue.add_to_queue(url)
        await ctx.send("Song added to the queue.")
    else:
        queue.add_to_queue(url)
        await play_music(ctx)


async def play_music(ctx):
    url = queue.get_next()

    if url is None:
        await leave(ctx)
        await ctx.send("No more music in queue.")
    else:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            voice_client.stop()

        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: bot.loop.create_task(play_music(ctx)))


@bot.command()
async def skip(ctx):
    ctx.voice_client.stop()


@bot.command()
async def stop(ctx):
    queue.queue.clear()
    ctx.voice_client.stop()


bot.run('MTE2NjU3NDgxMzUwNzIzMTg0NA.Ge14rc.s0cb6ghjKD_f-c755jkXlaNKapxRN5b8OeK_zg')
