import os
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

# ========== CONFIG ==========
WELCOME_CHANNEL = "welcome"
APPLICATION_CHANNEL = "applications"

WELCOME_TITLE = "🌑 Welcome"
WELCOME_DESC = (
    "Welcome {user} to **{server}**.\n\n"
    "Click **Apply** below to submit an application."
)

WELCOME_BANNER = "https://i.imgur.com/8Km9tLL.png"
EMBED_COLOR = 0x0b0b0b
# ============================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- APPLICATION FORM --------
class ApplicationModal(Modal, title="Server Application"):
    ign = TextInput(label="IGN / Username", required=True)
    age = TextInput(label="Age", required=True)
    reason = TextInput(
        label="Why do you want to join?",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = discord.utils.get(
            interaction.guild.text_channels,
            name=APPLICATION_CHANNEL
        )

        embed = discord.Embed(
            title="📩 New Application",
            color=EMBED_COLOR
        )
        embed.add_field(name="User", value=interaction.user.mention, inline=False)
        embed.add_field(name="IGN", value=self.ign.value, inline=True)
        embed.add_field(name="Age", value=self.age.value, inline=True)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)

        if channel:
            await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Application submitted!",
            ephemeral=True
        )

# -------- APPLY BUTTON --------
class ApplyView(View):
    @discord.ui.button(label="Apply", emoji="📝", style=discord.ButtonStyle.secondary)
    async def apply(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ApplicationModal())

# -------- EVENTS --------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(
        member.guild.text_channels,
        name=WELCOME_CHANNEL
    )

    if not channel:
        return

    embed = discord.Embed(
        title=WELCOME_TITLE,
        description=WELCOME_DESC.format(
            user=member.mention,
            server=member.guild.name
        ),
        color=EMBED_COLOR
    )
    embed.set_image(url=WELCOME_BANNER)

    await channel.send(
        content=member.mention,
        embed=embed,
        view=ApplyView()
    )

bot.run(os.getenv("DISCORD_TOKEN"))
