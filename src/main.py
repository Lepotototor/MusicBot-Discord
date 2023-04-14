import discord
from discord.ext import commands
import os
import dotenv
import time
import asyncio
from youtubesearchpython import VideosSearch



# Autorisations pour le bot
intents = discord.Intents().all()
intents.messages = True
intents.message_content = True
intents.members = True
intents.voice_states = True


#On charge les variables d'environnement
dotenv.load_dotenv(dotenv_path="../config")
id_general_channel = int(os.getenv("GENERAL_CHANNEL"))
token = os.getenv("TOKEN")



MusicBot = commands.Bot(command_prefix="!", description="Music Bot", intents=intents)






@MusicBot.command()
async def hello(ctx):
    """ Answer 'Hello World !'
    """
    await ctx.send('Hello World !')

@MusicBot.command()
async def ping(ctx):
    """ Answer Pong
    """
    await ctx.send("Pong")

@MusicBot.command()
async def quoi(ctx):
    """ Answer quoicoubaka
    """
    await ctx.send("Quoicoubaka")



##############     Commandes pour la musique       ############################################


playlist = []

@MusicBot.command()
async def join(ctx):
    """ Allows the bot to join the channel
    """
    voice_channel = ctx.channel
    if str(voice_channel.type) != "voice":
        return await ctx.send('Cette commande ne fonctionne que dans les salons vocaux !')
    try:
        await voice_channel.connect()
    except discord.errors.ClientException:
        await ctx.send('Je suis déjà dans ce salon vocal')

@MusicBot.command()
async def leave(ctx):
    """ Make the bot leave the channel
    """
    voice = ctx.voice_client
    await voice.disconnect()
    await erase(ctx, False)


@MusicBot.command()
async def add(ctx):
    """ To add a song in the playlist by keyword
    """
    musique_a_chercher = ctx.message.content[5:]
    musique = VideosSearch(musique_a_chercher, limit=1)
    result = musique.result()["result"][0]
    url_musique = result['link']
    await download(ctx, url_musique, name=(True, result['title']))
    playlist.append(result['title'])



@MusicBot.command()
async def download(ctx, url, name=(False, "")):
    """ To add a song in the playlist by url
    """
    try:
        if name[0]:
            os.system(f' yt-dlp -x --audio-format mp3 """{url}""" -o "../musiques/{name[1]}.mp3" ')
        else:
            os.system(f' youtube-dl -x --audio-format mp3 """{url}""" ')
            os.system("mv *.mp3 ../musiques/")
    except:
        await ctx.send("Désolé, je n'ai pas réussi à télécharger la musique")

@MusicBot.command()
async def play(ctx):
    """ To start the playlist
    """
    while len(playlist) > 0:
        player = await discord.FFmpegOpusAudio.from_probe(f"../musiques/{playlist[0]}.mp3")
        del playlist[0]
        ctx.voice_client.play(player)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

    await ctx.send("La playlist est vide...")


@MusicBot.command()
async def pause(ctx):
    """ To pause the song, you can resume it
    """
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()

@MusicBot.command()
async def resume(ctx):
    """ To resume the song
    """
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()


@MusicBot.command()
async def next(ctx):
    """ Move to next song
    """
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("Aucune musique en cours")
        return


@MusicBot.command()
async def see_playlist(ctx):
    """ To see titles in the playlist
    """
    if playlist == []:
        await ctx.send("Playlist vide...")
    else:
        all_titles = ""
        for title in playlist:
            all_titles += f"• {title}\n"
        await ctx.send(all_titles)
        await ctx.send(f"Il y a {len(playlist)} titres dans la playlist")

@MusicBot.command()
async def erase(ctx, affiche=True):
    """ Erase all titles in the playlist
    """
    for i in range(len(playlist)):
        playlist[0]
        del playlist[0]
    if affiche:
        await see_playlist(ctx)






###############################################################################################

@MusicBot.event
async def on_ready():
    print("Bot connecté")
    general_channel = MusicBot.get_channel(id_general_channel)
    await general_channel.send("Et zest baartiiiiii !!!!")





MusicBot.run(token)
