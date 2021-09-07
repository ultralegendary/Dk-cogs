from .clsroom import ClsRoom

# from .updts import Updts


def setup(bot):
    bot.add_cog(ClsRoom(bot))
    # bot.add_cog(Updts(bot))
