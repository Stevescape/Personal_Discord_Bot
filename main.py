import discord
import read_cache
from discord.ext import commands
import youtube_dl
import pafy


class WockaBot(discord.Client):

    def __init__(self, wockabot):
        self.wockabot = wockabot
        self.queue = {}

        self.setup()

    def setup(self):
        for guild in self.wockabot.guilds:
            self.queue[guild.id] = []

    async def check_queue(self, vc):
        if len(self.queue[vc.guild.id]) > 0:
            vc.voice_client.stop()
            await self.play_song(vc, self.queue[vc.guild.id][0])
            self.queue[vc.guild.id].pop(0)

    async def on_ready(self):
        print(f'I AM ALIVE | Bot - {self.user}')

    async def on_message(self, message):
        if (message.content == "hi"):
            await message.channel.send("HELLO")

        if (message.content == "join"):
            try:
                vc = message.author.voice.channel
            except:
                await message.channel.send("NO CHANNEL")
            await vc.connect()
            print(vc)

        if (message.content == "dc"):
            vc = self.voice_clients[0]
            await vc.disconnect()


    
    async def yt_search(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.Youtube({"format":"bestaudio","quiet" : True}).extrat_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if (len(info["entries"]) == 0):
            return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, vc, song):
        url = pafy.new(song).getbestaudio().url
        vc.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegAudio(url)), after=lambda error: self.wockabot.loop.create_task(self.check_queue(vc)))
        vc.voice_client.source.volume = 0.3 # defualt start sound

    @commands.command()
    async def play(self, vc, *, song=None):
        if song is None:
            return await vc.send("must include song")
        if vc.voice_client is None:
            return await vc.send("must be in voice channel")
        
        await self.play_song(vc, song)



if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = WockaBot(intents=intents)
    id = read_cache.grab_info("config.txt", "BOT_TOKEN")
    print(id)
    client.run(id)