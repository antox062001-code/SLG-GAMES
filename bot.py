import discord
import os
from discord import app_commands

# Render usará la variable TOKEN desde su panel de Environment Variables
TOKEN = os.getenv("TOKEN")

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

# Crear el cliente
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# IDs de los canales (ajusta con los tuyos)
CANAL_RECURSOS_ID = 1506174169971294359  # Canal A (solo tú escribes)
CANAL_BUSQUEDA_ID = 1506174440365494392  # Canal B (usuarios buscan)

@client.event
async def on_ready():
    await tree.sync()  # 🔥 Registra los comandos slash en Discord
    print(f"✅ Bot conectado como {client.user}")

@tree.command(name="buscar", description="Busca un recurso en el canal de recursos")
async def buscar(interaction: discord.Interaction, termino: str):
    # Solo permitir el comando en el canal de búsqueda
    if interaction.channel_id != CANAL_BUSQUEDA_ID:
        await interaction.response.send_message("⚠️ Este comando solo funciona en el canal de búsqueda.", ephemeral=True)
        return

    canal_recursos = interaction.guild.get_channel(CANAL_RECURSOS_ID)
    encontrado = None

    # Buscar en los últimos 500 mensajes del canal de recursos
    async for mensaje in canal_recursos.history(limit=500):
        if termino.lower() in mensaje.content.lower():
            encontrado = mensaje
            break

    if encontrado:
        # Responder con el link al mensaje original
        await interaction.response.send_message(f"✅ Encontrado: {encontrado.jump_url}")
    else:
        await interaction.response.send_message("❌ No encontré nada con ese término.")

# Ejecutar el bot
try:
    client.run(TOKEN)
except Exception as e:
    print(f"❌ Error al iniciar el bot: {e}")
