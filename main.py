import discord
import os
import arxiv

client=discord.Client()
@client.event
async def on_ready():
  print(f"im on_ready, {client.user}")
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("$arx "):
    title,abso,pdf,authors,summary,comment=get_arx(message.content[5:])
    reply_=discord.Embed(
      title=title,
      authors=authors,
      description=summary,
      url=abso,
      set_footer=("I'm grsteful for the Arvix Labs for providing this API service! Also thanks to @Likas Schwasb for the library!")
    )
    await message.channel.send(reply_)


def get_arx(query):
  query=str(query)
  search= arxiv.Search(
    query=query,
   max_results=5)
  titles=""
  links=[]
  abso=""
  pdf=""
  authors=""
  summary=""
  comment=""
  for result in search.results():
    titles += result.title+"\t"
    authors=result.authors+"\t"
    summary=result.summary+"\t"
    comment=result.comment+"\t"

    links+=[str(i) for i in result.links]
    for link in links:
      if "abs" in link:
        abso=link
      if "pdf" in link:
        pdf=link

  return titles,abso,pdf,authors,summary,comment



my_secret = os.environ['TOKEN']
client.run(my_secret)