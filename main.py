import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Web sunucusunu başlat (Render'ın port hatasını engellemek için)
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True

class IhbarModal(discord.ui.Modal, title='Yeni İhbar Oluştur'):
    ad_soyad = discord.ui.TextInput(label='Ad Soyad / Rumuz', placeholder='Şüphelinin adı...')
    ihbar_turu = discord.ui.TextInput(label='İhbar Türü', placeholder='Emniyet Genel Müdürlüğü...')
    konum = discord.ui.TextInput(label='Konum', style=discord.TextStyle.paragraph)
    detay = discord.ui.TextInput(label='Olay Detayı', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('İhbarın iletildi.', ephemeral=True)

class IhbarButon(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="İhbar Et", style=discord.ButtonStyle.danger, custom_id="ihbar_butonu_benzersiz_id")
    async def ihbar_et(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 404 hatasını önlemek için defer ve followup kullanımı
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send_modal(IhbarModal())

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(IhbarButon())

bot = MyBot()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    await bot.tree.sync()

@bot.command()
async def ihbarpanel(ctx):
    await ctx.send("Aşağıdaki butona basarak ihbar oluştur:", view=IhbarButon())

# Önce web sunucusunu çalıştır, sonra botu başlat
keep_alive()
bot.run(os.environ['TOKEN'])
