from .navi import navi
#from .updts import Updts

def setup(bot):
    bot.add_cog(navi(bot))
    #bot.add_cog(Updts(bot))
