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
        role_name = "Membre" 
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Merci ! Tu as accès au serveur.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Erreur : Le rôle '{role_name}' est introuvable sur le serveur.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    bot.add_view(ReglementView())
    
    channel_id = 1529648927333286034
    channel = bot.get_channel(channel_id)
    if channel:
        async for message in channel.history(limit=5):
            if message.author == bot.user:
                return
                
        reglement_texte = (
            "🌸 **RÈGLEMENT OFFICIEL DE YOZORA** 🌸\n\n"
            "Bienvenue sur **Yozora** ! Pour que notre communauté reste un espace chaleureux, sécurisé et agréable pour tout le monde, nous vous demandons de lire et de respecter les règles ci-dessous.\n\n"
            "**1. Le Respect d'Autrui**\n"
            "• Courtoisie obligatoire : Aucune insulte, harcèlement, sexisme, racisme ou discrimination.\n"
            "• Tolérance zéro : Propos haineux ou menaces = bannissement immédiat.\n"
            "• Vie privée : Interdiction de divulguer des infos personnelles (doxxing).\n\n"
            "**2. Salons et Communication**\n"
            "• Postez dans les bons salons.\n"
            "• Pas de spam, flood ou abus de majuscules.\n"
            "• Espace tout public : aucun contenu NSFW ou choquant.\n\n"
            "**3. Publicité**\n"
            "• Publicité interdite (salons et MP).\n\n"
            "**4. Modération**\n"
            "• Les décisions de l'équipe sont finales.\n\n"
            "Clique sur le bouton ci-dessous pour valider le règlement et accéder au serveur."
        )

        embed = discord.Embed(
            description=reglement_texte,
            color=discord.Color.pink()
        )
        view = ReglementView()
        await channel.send(embed=embed, view=view)

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
