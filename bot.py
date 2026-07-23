import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread

# --- SERVEUR WEB POUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Le bot de règlement est en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION DU BOT DISCORD ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class ReglementView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="J'accepte le règlement", style=discord.ButtonStyle.green, custom_id="accept_rules")
    async def accept_callback(self, interaction: discord.Interaction, button: Button):
        role_id = 1529660423379484793 
        role = interaction.guild.get_role(role_id)
        
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Merci ! Tu as accès au serveur.", ephemeral=True)
        else:
            await interaction.response.send_message("Erreur : Le rôle est introuvable sur le serveur.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    bot.add_view(ReglementView())

@bot.command()
@commands.has_permissions(administrator=True)
async def createreglement(ctx):
    reglement_texte = (
        "Bienvenue sur Yozora ! Pour que notre communauté reste un espace chaleureux, sécurisé et agréable pour tout le monde, nous vous demandons de lire et de respecter les règles ci-dessous.\n\n"
        "📌 **Section 1 : Le Respect d'Autrui**\n"
        "• **Courtoisie obligatoire :** Le respect mutuel est la base de Yozora. Aucune insulte, attaque personnelle, harcèlement, sexisme, racisme ou discrimination sous toutes ses formes ne sera toléré.\n"
        "• **Tolérance zéro :** Les propos haineux, menaces ou incitations à la violence entraîneront un bannissement immédiat et définitif du serveur.\n"
        "• **Vie privée :** Il est strictement interdit de divulguer des informations personnelles (doxxing) sur un membre ou un tiers sans son accord explicite.\n\n"
        "💬 **Section 2 : Les Salons et la Communication**\n"
        "• **Bon salon, bon sujet :** Veillez à poster vos messages dans les salons appropriés (par exemple, les discussions générales dans le salon principal, les mémos dans les salons dédiés, etc.).\n"
        "• **Anti-spam :** Le spam, le flood, l'utilisation excessive de majuscules (caps lock) ou de caractères spéciaux pour attirer l'attention sont interdits.\n"
        "• **Contenus inappropriés (NSFW) :** Yozora est un espace tout public. Aucun contenu à caractère pornographique, gore, choquant ou violent (textes, images, liens ou avatars) n'est toléré.\n\n"
        "📢 **Section 3 : Publicité et Liens**\n"
        "• **Publicité non autorisée :** Il est interdit de faire de la publicité pour d'autres serveurs Discord, des réseaux sociaux personnels ou des sites commerciaux dans les salons publics ou en message privé (MP) aux membres.\n"
        "• **Partenariats :** Pour toute demande de partenariat avec Yozora, veuillez contacter directement la modération ou les fondateurs.\n\n"
        "🛠️ **Section 4 : Modération et Sanctions**\n"
        "• **Décision des modérateurs :** L'équipe de Yozora (Modérateurs et Administrateurs) est là pour veiller au bon fonctionnement du serveur. Leurs décisions sont finales.\n"
        "• **Sanctions progressives :** En cas de non-respect du règlement, vous risquez selon la gravité :\n"
        "  1. Un avertissement (verbal ou officiel).\n"
        "  2. Une mise en sourdine (mute) temporaire.\n"
        "  3. Une expulsion (kick) ou un bannissement (ban) définitif.\n\n"
        "En cliquant sur le bouton d'acceptation ci-dessous, vous certifiez avoir lu, compris et accepté de respecter l'intégralité de ce règlement sur Yozora 🌸."
    )

    embed = discord.Embed(
        title="🌸 RÈGLEMENT OFFICIEL DE YOZORA 🌸",
        description=reglement_texte,
        color=discord.Color.pink()
    )
    view = ReglementView()
    await ctx.send(embed=embed, view=view)
    await ctx.message.delete()

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
