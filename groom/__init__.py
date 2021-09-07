from .updts import Updts


def setup(bot):
    bot.add_cog(Updts(bot))
