import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

class IhbarModal(discord.ui.Modal, title='Yeni İhbar Oluştur'):
    ad_soyad = discord.ui.TextInput(label='Ad Soyad / Rumuz', placeholder='Şüphelinin adı...')
    ihbar_turu = discord.ui.TextInput(label='İhbar Türü', placeholder='Emniyet Genel Müdürlüğü...')
    konum = discord.ui.TextInput(label='Konum', style=discord.TextStyle.paragraph)
    detay = discord.ui.TextInput(label='Olay Detayı', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        # İşlem başarılı olduğunda kısa bir yanıt ver
        await interaction.response.send_message('İhbarın başarıyla iletildi!', ephemeral=True)

class IhbarButon(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Butonun hep çalışır kalması için

    @discord.ui.button(label="İhbar Et", style=discord.ButtonStyle.danger, custom_id="ihbar_button_1")
    async def ihbar_et(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Butona basıldığında Modal (form) penceresini aç
        await interaction.response.send_modal(IhbarModal())

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Bot her açıldığında butonu yeniden kaydet
        self.add_view(IhbarButon())

bot = MyBot()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    await bot.tree.sync()

@bot.command()
async def ihbarpanel(ctx):
    # !ihbarpanel yazıldığında butonu gönder
    await ctx.send("Aşağıdaki butona basarak ihbar oluştur:", view=IhbarButon())

bot.run(os.environ['TOKEN'])
