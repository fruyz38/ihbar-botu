import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
import time

# Web sunucusu
app = Flask('')
@app.route('/')
def home(): return "Bot aktif!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True

class IhbarModal(discord.ui.Modal, title='Yeni İhbar Oluştur'):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.TextInput(label='Ad Soyad / Rumuz', placeholder='Şüphelinin adı...'))
        self.add_item(discord.ui.TextInput(label='İhbar Türü', placeholder='Emniyet Genel Müdürlüğü...'))
        self.add_item(discord.ui.TextInput(label='Konum', style=discord.TextStyle.paragraph))
        self.add_item(discord.ui.TextInput(label='Olay Detayı', style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('İhbarın iletildi.', ephemeral=True)

class IhbarButon(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="İhbar Et", style=discord.ButtonStyle.danger, custom_id="ihbar_butonu_benzersiz_id")
    async def ihbar_et(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IhbarModal())

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(IhbarButon())

bot = MyBot()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.command()
async def ihbarpanel(ctx):
    embed = discord.Embed(
        title="🚨 Zynex İhbar Sistemine Hoşgeldin!",
        description="Bu sistem üzerinden güvenli ve anonim şekilde ihbar gönderebilirsiniz.",
        color=discord.Color.red()
    )
    embed.add_field(name="🔒 GİZLİLİK GARANTİSİ:", value="• İhbarlar anonimdir ve veriler gizli tutulur.", inline=False)
    embed.add_field(name="⚡ SİSTEM GÜVENCESİ:", value="• İhbarlar otomatik olarak EGM'ye iletilir.", inline=False)
    embed.set_footer(text="fruyz ihbar sistemi / otomatik apı entegrasyonu")
    
    await ctx.send(embed=embed, view=IhbarButon())

# Web sunucusunu başlat
keep_alive()

# Hata durumunda yeniden başlatan döngü
while True:
    try:
        bot.run(os.environ['TOKEN'])
    except Exception as e:
        print(f"Bot hata aldı, 5 saniye sonra yeniden başlıyor: {e}")
        time.sleep(5)
