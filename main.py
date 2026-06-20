import discord
from discord.ext import commands

# BOT TOKENINI BURAYA YAZ
TOKEN = 'MTUxNzk2Mjg2OTYwODY4MTU4Mw.GhgRC9.4sfcsR7mh8Ur1A9HbXuCqExo-EvpGeNX2D-yj0'

# İzinleri (intents) tanımlıyoruz
intents = discord.Intents.default()
intents.message_content = True 

class IhbarModal(discord.ui.Modal, title='Yeni İhbar Oluştur'):
    ad_soyad = discord.ui.TextInput(label='Ad Soyad / Rumuz', placeholder='Şüphelinin adı...')
    ihbar_turu = discord.ui.TextInput(label='İhbar Türü', placeholder='Emniyet Genel Müdürlüğü...')
    konum = discord.ui.TextInput(label='Konum', style=discord.TextStyle.paragraph)
    detay = discord.ui.TextInput(label='Olay Detayı', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.send(f"🚨 **Yeni İhbar:**\nİsim: {self.ad_soyad}\nTür: {self.ihbar_turu}\nKonum: {self.konum}\nDetay: {self.detay}")
        await interaction.response.send_message("İhbarın iletildi.", ephemeral=True)

class IhbarButon(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout'u None yaptık

    @discord.ui.button(label="🚨 İhbar Oluştur", style=discord.ButtonStyle.primary, custom_id="ihbar_btn_1")
    async def ihbar_buton(self, interaction: discord.Interaction, button: discord.ui.Button):
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
    await bot.tree.sync()

@bot.command()
async def ihbarpanel(ctx):
    await ctx.send("Aşağıdaki butona basarak ihbar oluştur:", view=IhbarButon())

bot.run(TOKEN)