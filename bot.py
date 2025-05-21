
import discord
from discord import app_commands
from discord.ext import commands
import requests
import json

TOKEN = "MTM3Mzk3NTM4OTg0NzgxODM4Mw.GECX6H.cNz02s2REomKnvpOX6HgDxk3yUrMbmKIooZT8g"
GUILD_ID = 1244885780661272617  # Replace with your Discord server ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

admin_ids = [1350875691666640956]  # Thay bằng ID admin thật

def is_admin(user):
    return user.id in admin_ids

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {bot.user}")

async def upload_account_to_php(url, email, password):
    try:
        res = requests.post(url, json={"email": email, "password": password}, timeout=5)
        return res.status_code == 200
    except Exception as e:
        print(f"Upload error: {e}")
        return False

async def upload_account(interaction, url, email, password, label):
    if not is_admin(interaction.user):
        await interaction.response.send_message("Bạn không có quyền.", ephemeral=True)
        return

    success = await upload_account_to_php(url, email, password)
    if success:
        await interaction.response.send_message(f"Đã thêm tài khoản {label}: `{email}`", ephemeral=True)
    else:
        await interaction.response.send_message("Lỗi khi gửi tài khoản tới máy chủ.", ephemeral=True)

@tree.command(name="upmail", description="Thêm tài khoản Email")
@app_commands.describe(email="Email", password="Mật khẩu")
async def upmail(interaction: discord.Interaction, email: str, password: str):
    await upload_account(interaction, "https://txziczacroblox.site/mail.php", email, password, "Email")

@tree.command(name="upugphone", description="Thêm tài khoản UGPhone")
@app_commands.describe(email="Email", password="Mật khẩu")
async def upugphone(interaction: discord.Interaction, email: str, password: str):
    await upload_account(interaction, "https://txziczacroblox.site/ug.php", email, password, "UGPhone")

@tree.command(name="upldcloud", description="Thêm tài khoản LD Cloud")
@app_commands.describe(email="Email", password="Mật khẩu")
async def upldcloud(interaction: discord.Interaction, email: str, password: str):
    await upload_account(interaction, "https://txziczacroblox.site/ld.php", email, password, "LD Cloud")

@tree.command(name="upredfinger", description="Thêm tài khoản RedFinger")
@app_commands.describe(email="Email", password="Mật khẩu")
async def upredfinger(interaction: discord.Interaction, email: str, password: str):
    await upload_account(interaction, "https://txziczacroblox.site/red.php", email, password, "RedFinger")

async def list_accounts_from_php(url):
    try:
        res = requests.get(url, timeout=5)
        return res.json()
    except Exception as e:
        print(f"List error: {e}")
        return {}

async def list_accounts(interaction, url, label):
    if not is_admin(interaction.user):
        await interaction.response.send_message("Bạn không có quyền.", ephemeral=True)
        return

    accounts = await list_accounts_from_php(url)
    if not accounts:
        await interaction.response.send_message(f"Không có tài khoản {label}.", ephemeral=True)
    else:
        msg = "\n".join([f"{email}: {pw}" for email, pw in accounts.items()])
        await interaction.response.send_message(f"Tài khoản {label}:\n`{msg}`", ephemeral=True)

@tree.command(name="listmail", description="Liệt kê tài khoản Email")
async def listmail(interaction: discord.Interaction):
    await list_accounts(interaction, "https://txziczacroblox.site/mail.json", "Email")

@tree.command(name="listugphone", description="Liệt kê tài khoản UGPhone")
async def listugphone(interaction: discord.Interaction):
    await list_accounts(interaction, "https://txziczacroblox.site/ug.json", "UGPhone")

@tree.command(name="listldcloud", description="Liệt kê tài khoản LD Cloud")
async def listldcloud(interaction: discord.Interaction):
    await list_accounts(interaction, "https://txziczacroblox.site/ld.json", "LD Cloud")

@tree.command(name="listredfinger", description="Liệt kê tài khoản RedFinger")
async def listredfinger(interaction: discord.Interaction):
    await list_accounts(interaction, "https://txziczacroblox.site/red.json", "RedFinger")

bot.run(TOKEN)
