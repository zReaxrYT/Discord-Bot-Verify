import discord
from discord.ext import commands
import random

verify_role = 123 # the role to be assigned after verification

class verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    @commands.is_owner() # only the server owner can use this command.
    async def start_verify(self, ctx):
        await ctx.send(embed=discord.Embed(title="Verify", description="Click on the button.", color=discord.Color.green()), view=verify_button()) # the verify message.

    @start_verify.error # This is a error handler. 
    async def start_verify_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            print(f"Logging: {ctx.author} ({ctx.author.id}) has been tried the 'start_verify' command to use.") # when a user tries to use the command, this comes in the console.

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(verify_button()) # add to the on_ready event because when the bot restart then is the button still working.

class verify_button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, custom_id="verify") # the verify button:
    async def verify_callback(self, button, interaction):
        role = discord.utils.get(interaction.guild.roles, id=verify_role)
        if role in interaction.user.roles: # check of user has the role.
            await interaction.response.send_message("You have already verified yourself.", ephemeral=True)
        else:
            await interaction.response.send_modal(verify_modal()) 

class verify_modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Verify")

        self.verify_code = random.randint(1000, 9999) # generate the random code

        self.add_item(discord.ui.InputText(label=f"Your code is {self.verify_code}", placeholder="Type here your code..", max_length=4))

    async def callback(self, interaction: discord.Interaction):
        try:
            if int(self.children[0].value) == self.verify_code: # checking the correctness of the code is
                role = discord.utils.get(interaction.guild.roles, id=verify_role)
                await interaction.user.add_roles(role, reason="Verify was succesfully")
                await interaction.response.send_message("Succesfully! The code you entered was correct.", ephemeral=True)
            else:
                await interaction.response.send_message("The code you entered was incorrect.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Please enter numbers only.", ephemeral=True)


def setup(bot):
    bot.add_cog(verify(bot))
