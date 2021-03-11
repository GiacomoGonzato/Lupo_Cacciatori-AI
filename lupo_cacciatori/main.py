from utils.gioco_lupo_cacciatori import lupo_cacciatori

gioco = lupo_cacciatori(2)
# Con profondità 14 i cacciatori diventano letteralmente imbattibili (il lupo non ha speranze)
gioco.play(14)
