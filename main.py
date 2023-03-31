import discord
import read_cache

class WockaBot(discord.Client):
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

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = WockaBot(intents=intents)
    id = read_cache.grab_info("config.txt", "BOT_TOKEN")
    print(id)
    client.run(id)