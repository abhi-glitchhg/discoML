import discord
import os
import arxiv

client = discord.Client()


@client.event
async def on_ready():
    print(f"im on_ready, {client.user}")


@client.event
async def on_message(message):
    if message.content.startswith("$arx "):

        query = message.content[5:]
        search = arxiv.Search(
            query=query,
            max_results=5,
        )
        title = ""
        links = []
        abso = ""
        pdf = ""
        authors = []
        summary = ""
        comment = ""
        i = 0
        for result in search.results():

            title = result.title + "\t"
            author = [_ for _ in result.authors]
            if result.summary is not None:
                summary = result.summary + "\t"
            if result.comment is not None:
                comment = result.comment + "\t"

            links = [str(i) for i in result.links]
            for link in links:
                if "abs" in link:
                    abso = link
                if "pdf" in link:
                    pdf = link
            reply_ = discord.Embed(
                title=title,
                authors=authors,
                description=summary,
                url=abso,
                set_footer=(
                    "I'm grateful for the Arvix Labs for providing this API service! Also thanks to @Likas Schwasb for the library!")
            )
            reply_.add_field(name="pdf", value=pdf, inline=True)
            i += 1
            if i == 5:
                # greet="we are grateful to arxiv for api service!"
                greet = None
            else:
                greet = None
            await message.channel.send(greet, embed=reply_)


my_secret = os.environ['TOKEN']
client.run(my_secret)