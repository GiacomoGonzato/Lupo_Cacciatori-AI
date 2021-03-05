from utils.gioco_lupo_cacciatori import lupo_cacciatori

gioco = lupo_cacciatori(2)
# Con profondità 10 il computer diventa bravo a giocare ma lascia i propri pezzi troppo separati tra di loro
gioco.play(14)