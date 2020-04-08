from scipy import stats
obs = [817,183]
exp = [842,158]
res = stats.chisquare(obs, exp)
print(res)