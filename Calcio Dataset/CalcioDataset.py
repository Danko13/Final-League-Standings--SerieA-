# PROJECT ITALIAN FOOTBALL TABLE
# TO DO:
# Create table_total, table_home, table_away with following columns:
# Rank; Teams; MP (match played); W (wins); D (draws); L (lose); GS (goals scored); GC (goals conceded); GD (goals difference); P(points)

import pandas as pd
import matplotlib.pyplot as plt

# creating new dataFrame for future work
table_total = pd.DataFrame(columns=['Rank','Teams','MP','W','D','L','GS','GC','GD','P'])
table_home = pd.DataFrame(columns=['Rank','Teams','MP','W','D','L','GS','GC','GD','P'])
table_away = pd.DataFrame(columns=['Rank','Teams','MP','W','D','L','GS','GC','GD','P'])

# importing the basic dataset
calcio = pd.read_csv(r'C:\Users\Daniel\Desktop\Python Courses\MyProjects\Calcio Dataset\2006-2007.csv')

# convert Date column into datetime type
calcio.Date = pd.to_datetime(calcio.Date)

# creating a list with all the teams
Teams = []
for i in range (0,380):
    t = calcio['HomeTeam'].loc[i]
    if t in Teams:
        continue
    else:
        Teams.append(t)

table_home['Teams'] = sorted(Teams,key=str)
table_away['Teams'] = sorted(Teams,key=str)

# creating column with match number
calcio.insert(3, 'MatchNumber', range(1, 1 + len(calcio)))

# creating new columns for better manipulating with the score
calcio['HTGoalEnd'], calcio['ATGoalEnd'] = calcio['FT'].str.split('-', 1).str
calcio.drop(['FT'], axis=1, inplace=True)
calcio['HTGoalHT'], calcio['ATGoalHT'] = calcio['HT'].str.split('-', 1).str
calcio.drop(['HT'], axis=1, inplace=True)

# convert Result columns into numeric
calcio['HTGoalEnd'] = calcio['HTGoalEnd'].astype(str).astype(int)
calcio['ATGoalEnd'] = calcio['ATGoalEnd'].astype(str).astype(int)
calcio['HTGoalHT'] = calcio['HTGoalHT'].astype(str).astype(int)
calcio['ATGoalHT'] = calcio['ATGoalHT'].astype(str).astype(int)

# creating Result columns for HT and End result
calcio['ResultEnd'] = 'DrawEnd'
calcio['ResultHT'] = 'DrawHT'
calcio.ix[calcio['HTGoalEnd'] > calcio['ATGoalEnd'], 'ResultEnd'] = 'HTWinEnd'
calcio.ix[calcio['HTGoalEnd'] < calcio['ATGoalEnd'], 'ResultEnd'] = 'ATWinEnd'
calcio.ix[calcio['HTGoalHT'] > calcio['ATGoalHT'], 'ResultHT'] = 'HTWinHT'
calcio.ix[calcio['HTGoalHT'] < calcio['ATGoalHT'], 'ResultHT'] = 'ATWinHT'


# quick look at all End results with plot (pie chart)
#calcio.groupby('ResultEnd')['ResultEnd'].count().plot(kind='pie')
#plt.show()

# creating Total Goals column for all the matches
calcio['TotalGoalsEnd'] = calcio['HTGoalEnd'] + calcio['ATGoalEnd']
calcio['TotalGoalsHT'] = calcio['HTGoalHT'] + calcio['ATGoalHT']

# creating new column for home/away team goals in the whole season

HomeTeam_GS = (calcio.groupby(['HomeTeam'])['HTGoalEnd'].sum().reset_index().rename(columns={'HomeTeam':'Team', 'HTGoalEnd': 'HomeGS'}))
HomeTeam_GC = (calcio.groupby(['HomeTeam'])['ATGoalEnd'].sum().reset_index().rename(columns={'HomeTeam':'Team', 'ATGoalEnd': 'HomeGC'}))
AwayTeam_GS = (calcio.groupby(['AwayTeam'])['ATGoalEnd'].sum().reset_index().rename(columns={'AwayTeam':'Team', 'ATGoalEnd': 'AwayGS'}))
AwayTeam_GC = (calcio.groupby(['AwayTeam'])['HTGoalEnd'].sum().reset_index().rename(columns={'AwayTeam':'Team', 'HTGoalEnd': 'AwayGC'}))


# inserting new row for TOTAL values (total goals in the season and total goals in the first half of the match)
calcio.loc['Total'] = pd.Series(calcio['TotalGoalsEnd'].sum(), index = ['TotalGoalsEnd'])
calcio.loc['Total', 'TotalGoalsHT'] = calcio['TotalGoalsHT'].sum()

# creating new columns game_month and game_weekday
calcio['game_month'] = calcio['Date'].dt.month
calcio['game_weekday'] = calcio['Date'].dt.weekday_name

# re-arranging the order of the columns
calcio = calcio[['MatchNumber','Date','game_month','game_weekday','HomeTeam','AwayTeam','HTGoalHT','ATGoalHT','HTGoalEnd','ATGoalEnd','TotalGoalsHT','TotalGoalsEnd','ResultHT','ResultEnd',]]

# set MatchNumber as our index
calcio.index = calcio['MatchNumber']
calcio.drop(['MatchNumber'], axis=1, inplace=True)
# number of games per month, using bar chart
#calcio.groupby(calcio['game_month'])['MatchNumber'].count().plot(kind='bar')
#plt.show()

# Convert resultEnd column to three binary columns so they can be summed up later
calcio = calcio.merge(pd.get_dummies(calcio['ResultEnd']), left_index=True, right_index=True)

# Convert resultHT column to three binary columns so they can be summed up later
calcio = calcio.merge(pd.get_dummies(calcio['ResultHT']), left_index=True, right_index=True)


# Creating new columns for hometeam and awayteam wins/draws in the whole season
calcio['HomeTeam_wins_this_season'] = calcio.groupby(['HomeTeam'])['HTWinEnd'].transform('sum')
calcio['AwayTeam_wins_this_season'] = calcio.groupby(['AwayTeam'])['ATWinEnd'].transform('sum')
calcio['HomeTeam_draws_this_season'] = calcio.groupby(['HomeTeam'])['DrawEnd'].transform('sum')
calcio['AwayTeam_draws_this_season'] = calcio.groupby(['AwayTeam'])['DrawEnd'].transform('sum')

HomeTeam_wins = (calcio.groupby(['HomeTeam'])['HTWinEnd'].sum().reset_index().rename(columns={'HomeTeam':'Team', 'HTWinEnd': 'HomeWins'}))
AwayTeam_wins = (calcio.groupby(['AwayTeam'])['ATWinEnd'].sum().reset_index().rename(columns={'AwayTeam':'Team', 'ATWinEnd': 'AwayWins'}))
HomeTeam_draws = (calcio.groupby(['HomeTeam'])['DrawEnd'].sum().reset_index().rename(columns={'HomeTeam':'Team', 'DrawEnd': 'HomeDraws'}))
AwayTeam_draws = (calcio.groupby(['AwayTeam'])['DrawEnd'].sum().reset_index().rename(columns={'AwayTeam':'Team', 'DrawEnd': 'AwayDraws'}))


# Which teams win the most home games on average per season
calcio.groupby(['HomeTeam'])['HomeTeam_wins_this_season'].agg(['count','mean']).sort_values(ascending=False, by='mean').round(1)
# Which teams win the most away games on average per season
calcio.groupby(['AwayTeam'])['AwayTeam_wins_this_season'].agg(['count','mean']).sort_values(ascending=False, by='mean').round(1)
# Which teams draw the most home games on average per season
calcio.groupby(['HomeTeam'])['HomeTeam_draws_this_season'].agg(['count','mean']).sort_values(ascending=False, by='mean').round(1)
# Which teams draw the most away games on average per season
calcio.groupby(['AwayTeam'])['AwayTeam_draws_this_season'].agg(['count','mean']).sort_values(ascending=False, by='mean').round(1)

# Assigning points to home/away wins and draws
calcio['HTWinPoints'] = '0'
calcio['ATWinPoints'] = '0'
calcio['DrawPoints'] = '0'
calcio.loc[calcio['HTWinEnd'] == 1, ['HTWinPoints']] = 3
calcio.loc[calcio['ATWinEnd'] == 1, ['ATWinPoints']] = 3
calcio.loc[calcio['DrawEnd'] == 1, ['DrawPoints']] = 1
calcio['HTWinPoints'] = calcio['HTWinPoints'].astype(str).astype(int)
calcio['ATWinPoints'] = calcio['ATWinPoints'].astype(str).astype(int)
calcio['DrawPoints'] = calcio['DrawPoints'].astype(str).astype(int)


# Creating new columns for points for hometeam and awayteam win_points/draw_points in the whole season
calcio['HomeTeam_win_points_this_season'] = calcio.groupby(['HomeTeam'])['HTWinPoints'].transform('sum')
calcio['AwayTeam_win_points_this_season'] = calcio.groupby(['AwayTeam'])['ATWinPoints'].transform('sum')
calcio['HomeTeam_drawpoints_this_season'] = calcio.groupby(['HomeTeam'])['DrawPoints'].transform('sum')
calcio['AwayTeam_drawpoints_this_season'] = calcio.groupby(['AwayTeam'])['DrawPoints'].transform('sum')


HomeTeam_win_points = calcio.groupby(['HomeTeam'])['HomeTeam_win_points_this_season'].agg(['count','mean']).round(1).reset_index()
HomeTeam_draw_points = calcio.groupby(['HomeTeam'])['HomeTeam_drawpoints_this_season'].agg(['count','mean']).round(1).reset_index()
AwayTeam_win_points = calcio.groupby(['AwayTeam'])['AwayTeam_win_points_this_season'].agg(['count','mean']).round(1).reset_index()
AwayTeam_draw_points = calcio.groupby(['AwayTeam'])['AwayTeam_drawpoints_this_season'].agg(['count','mean']).round(1).reset_index()

# FILLING THE TABLE_HOME DATAFRAME

table_home['MP'] = HomeTeam_win_points['count']
table_home['W'] = HomeTeam_wins['HomeWins']
table_home['D'] = HomeTeam_draws['HomeDraws']
table_home['L'] = table_home['MP'] - (table_home['W']+table_home['D'])
table_home['GS'] = HomeTeam_GS['HomeGS']
table_home['GC'] = HomeTeam_GC['HomeGC']
table_home['GD'] = table_home['GS'] - table_home['GC']
table_home['P'] = HomeTeam_draw_points['mean'] + HomeTeam_win_points['mean']
table_home.sort_values("P", inplace=True, ascending=False)
table_home['Rank'] = table_home['P'].rank(ascending=0,method='first')
table_home.set_index('Rank', inplace=True)

# FILLING THE TABLE_AWAY DATAFRAME

table_away['MP'] = AwayTeam_win_points['count']
table_away['W'] = AwayTeam_wins['AwayWins']
table_away['D'] = AwayTeam_draws['AwayDraws']
table_away['L'] = table_away['MP'] - (table_away['W'] + table_away['D'])
table_away['GS'] = AwayTeam_GS['AwayGS']
table_away['GC'] = AwayTeam_GC['AwayGC']
table_away['GD'] = table_away['GS'] - table_away['GC']
table_away['P'] = AwayTeam_draw_points['mean'] + AwayTeam_win_points['mean']
table_away.sort_values(by=['P','GD'], inplace=True, ascending=False)
table_away['Rank'] = table_away[['P','GD']].rank(ascending=0,method='first')
table_away.set_index('Rank', inplace=True)


# FILLING THE TABLE_TOTAL

table_total['Rank'] = range(1,21)
table_total.set_index('Rank', inplace=True)
table_total['MP'] = table_home['MP'] + table_away['MP']
table_total['W'] = table_home['W'] + table_away['W']
table_total['D'] = table_home['D'] + table_away['D']
table_total['L'] = table_home['L'] + table_away['L']
table_total['GS'] = table_home['GS'] + table_away['GS']
table_total['GC'] = table_home['GC'] + table_away['GC']
table_total['GD'] = table_home['GD'] + table_away['GD']
table_total['P'] = table_home['P'] + table_away['P']
table_total.sort_values('P', inplace=True, ascending=False)
table_total['Rank'] = table_total['P'].rank(ascending=0, method='first')
table_total.set_index('Rank', inplace=True)

table_teams = (table_home.groupby(['Teams'])['P'].agg(['mean'])).add((table_away.groupby(['Teams'])['P'].agg(['mean'])))
table_teams.sort_values(by='mean',ascending=False, inplace=True)
table_total['Teams'] = table_teams.index


print (table_total)


