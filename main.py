from typing import Final
from dotenv import load_dotenv
import os
import discord
from discord import Intents, Member
from discord.ext import commands
import nest_asyncio
from responses import get_faceit_stats
import asyncio



# Zastosowanie poprawki dla kompatybilności asyncio w środowiskach takich jak Jupyter
nest_asyncio.apply()

# Załadowanie zmiennych środowiskowych z pliku .env
load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Definicja intentów dla bota
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Inicjalizacja bota z intentami i prefiksem komendy
bot = commands.Bot(command_prefix='!', intents=intents)



# Komenda: Wyświetlenie regulaminu
@bot.command()
async def regulamin(ctx):
    embed = discord.Embed(
        title="📜 Regulamin Serwera Discord",
        description="Poniżej znajdziesz zasady, które obowiązują na naszym serwerze. Prosimy o ich przestrzeganie dla zachowania przyjaznej atmosfery.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="1️⃣ Postanowienia Ogólne",
        value=(
            "1. Korzystanie z serwera oznacza akceptację niniejszego regulaminu.\n"
            "2. Administracja zastrzega sobie prawo do modyfikacji regulaminu.\n"
            "3. Nieznajomość regulaminu nie zwalnia użytkownika z jego przestrzegania."
        ),
        inline=False
    )
    
    embed.add_field(
        name="2️⃣ Zasady Ogólne",
        value=(
            "1. Szanuj innych użytkowników – zakaz obrażania, grożenia oraz dyskryminacji.\n"
            "2. Zabrania się spamu, floodingu i wysyłania niechcianych linków.\n"
            "3. Publikowanie nieodpowiednich treści (np. mowy nienawiści, brutalnych obrazów) jest zabronione."
        ),
        inline=False
    )
    
    embed.add_field(
        name="3️⃣ Zasady Dotyczące Nicków i Avatarów",
        value=(
            "1. Nicki i awatary nie mogą zawierać treści obraźliwych ani wulgarnych.\n"
            "2. Administracja może wymagać zmiany nicku lub awatara, jeśli są one nieodpowiednie."
        ),
        inline=False
    )
    
    embed.add_field(
        name="4️⃣ Zasady Reklamy",
        value=(
            "1. Reklamowanie serwerów, produktów lub usług jest dozwolone tylko za zgodą administracji.\n"
            "2. Zakaz wysyłania reklam w prywatnych wiadomościach do innych użytkowników."
        ),
        inline=False
    )
    
    embed.add_field(
        name="5️⃣ Administracja i Moderacja",
        value=(
            "1. Decyzje administracji są ostateczne.\n"
            "2. W razie problemów kontaktuj się z administracją przez kanał 'Pomoc' lub prywatną wiadomość.\n"
            "3. Nadużywanie funkcji „pingowania” administracji jest zabronione."
        ),
        inline=False
    )
    
    embed.add_field(
        name="6️⃣ Sankcje",
        value=(
            "1. Łamanie regulaminu może skutkować ostrzeżeniem, wyciszeniem, wyrzuceniem lub banem.\n"
            "2. Administracja ma prawo indywidualnie rozpatrywać każdy przypadek naruszenia zasad."
        ),
        inline=False
    )
    
    embed.add_field(
        name="7️⃣ Prywatność",
        value=(
            "1. Zabrania się udostępniania prywatnych informacji innych użytkowników bez ich zgody.\n"
            "2. Serwer nie gromadzi danych osobowych poza tymi wymaganymi przez Discord."
        ),
        inline=False
    )
    
    embed.set_footer(text="Dziękujemy za przestrzeganie zasad i życzymy miłego pobytu na serwerze! 😊")

    await ctx.send(embed=embed)

# Komenda: Sprawdzenia statystyk Faceit
@bot.command()
async def faceit(ctx, *, profile_url: str):
    """Wpisz !faceit <link do profilu FACEIT>, aby sprawdzić statystyki."""
    try:
        if "faceit.com" in profile_url or "faceittracker.net" in profile_url:
            player_name = profile_url.split("/")[-1]
        else:
            await ctx.send("Podano nieprawidłowy link. Użyj formatu: https://faceittracker.net/players/NICKNAME")
            return

        stats = get_faceit_stats(player_name)
        if not stats:
            await ctx.send("Nie udało się pobrać statystyki dla tego gracza. Sprawdź, czy nick jest poprawny.")
            return

        embed = discord.Embed(title=f"**Statystyki FACEIT dla {player_name}**", color=0x00ff00)
        embed.add_field(name="Poziom", value=stats["level"], inline=True)
        embed.add_field(name="ELO", value=stats["elo"], inline=True)
        embed.add_field(name="Rozegrane mecze", value=stats["matches"], inline=True)
        embed.add_field(name="Win Rate", value=f"{stats['winrate']}", inline=True)
        embed.add_field(name="Headshot Rate", value=f"{stats['headshots']}", inline=True)
        embed.add_field(name="K/D Ratio", value=f"{stats['kd_ratio']}", inline=True)
        embed.add_field(name="**LAST 10 MATCHES**", value="", inline=False)
        embed.add_field(name="K/D Ratio", value=f"{stats['k/d_ratio_last_10']}", inline=True)
        embed.add_field(name="Wins", value=f"{stats['wins']}", inline=True)
        embed.add_field(name="Losses", value=f"{stats['losses']}", inline=True)
        embed.add_field(name="Results", value=f"{stats['last_10_results']}", inline=True)

        embed.set_footer(text="Statystyki dostarczone przez FaceitTracker.net")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("Wystąpił błąd podczas przetwarzania żądania.")
        print(e)

# Wydarzenie, które jest wywoływane, gdy bot jest gotowy
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} jest online')
    activity = discord.CustomActivity(name='Owner: kurzowskyy')
    await bot.change_presence(activity=activity)
    channel = bot.get_channel(1244337321608876042)
    if channel:
        await channel.send('Jestem online')

# Wydarzenie, które jest wywoływane, gdy status użytkownika zmienia się na online
@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    # ID ról, które chcemy monitorować
    monitored_roles = {1249508176722661416, 941320096452841572}

    # Sprawdzenie, czy użytkownik przeszedł ze statusu offline na online
    if before.status == discord.Status.offline and after.status != discord.Status.offline:
        # Sprawdzanie, czy użytkownik ma jedną z wymaganych ról
        if any(role.id in monitored_roles for role in after.roles):
            # Pobieramy kanał, do którego wysyłamy wiadomość
            channel = after.guild.get_channel(1244337321608876042)
            if channel:
                await channel.send(f'{after.display_name} jest teraz online!')

# Komenda do zmiany pseudonimu użytkownika (wymaga uprawnień)
@bot.command(name='zmien_nick')
@commands.has_permissions(manage_nicknames=True)
async def change_nick(ctx, member: Member, *, new_nickname: str):
    try:
        old_nickname = member.display_name
        await member.edit(nick=new_nickname)
        await ctx.send(f'Pseudonim użytkownika {old_nickname} został zmieniony na {new_nickname}')
    except discord.Forbidden:
        await ctx.send('Nie mam uprawnień do zmiany pseudonimu tego użytkownika.')
    except discord.HTTPException as e:
        await ctx.send(f'Wystąpił błąd podczas zmiany pseudonimu: {e}')

blocked_nicknames = {}  # Słownik do przechowywania blokowanych pseudonimów {user_id: nick_to_block}

@bot.command()
@commands.has_permissions(administrator=True)
async def block_nickname(ctx, member: Member, nick: str):
    """Blokuje lub odblokowuje możliwość zmiany pseudonimu dla konkretnego użytkownika."""
    if member.id in blocked_nicknames:
        del blocked_nicknames[member.id]
        await ctx.send(f'Odblokowano zmianę pseudonimu dla użytkownika {member.display_name}.')
    else:
        blocked_nicknames[member.id] = nick
        await ctx.send(f'Zablokowano zmianę pseudonimu dla użytkownika {member.display_name}. '
                       f'Pseudonim zostanie zmieniony na "{nick}" w przypadku próby edycji.')

# Wydarzenie wywoływane podczas zmiany pseudonimu użytkownika
@bot.event
async def on_member_update(before: Member, after: Member):
    """Zapobiega zmianie pseudonimu dla użytkowników znajdujących się na liście blokowanych."""
    if after.id in blocked_nicknames:
        blocked_nick = blocked_nicknames[after.id]
        if before.nick != after.nick:
            try:
                await after.edit(nick=blocked_nick)
                print(f'Zmieniono pseudonim użytkownika {after.display_name} na "{blocked_nick}".')
            except discord.Forbidden:
                print(f'Bot nie ma uprawnień do zmiany pseudonimu użytkownika {after.display_name}.')
            except discord.HTTPException as e:
                print(f'Wystąpił błąd podczas zmiany pseudonimu użytkownika {after.display_name}: {e}')

# Uruchomienie bota z tokenem
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
