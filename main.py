import numpy as np
import pandas as pd
import math

# Часть заданий закоменчены, так как их вывод мне мешался

# Подзадание 1
data = pd.read_csv('data.csv', delimiter=',')

# Подзадание 2
# Выведем некоторые статистические сведения о выборке
# print(data.describe())

# Подзадание 3
# Выведем первых n челиков. По умолчанию 5, но я более явно это указал
# print(data.head(5))

# Выведем последних n челиков. По умолчанию 5, но я более явно это указал
# print(data.tail(5))

# Подзадание 4
# Id - 32- или 64-битный integer (numpy выберет 64-битный)
# SeriousDlqin2yrs - 32- или 64-битный интегер (numpy выберет 64-битный) - Но почему не bool?
# RevolvingUtilizationOfUnsecuredLines - float64
# age - int
# NumberOfTime30-59DaysPastDueNotWorse - int 
# DebtRatio - float
# MonthlyIncome - int
# NumberOfOpenCreditLinesAndLoans - int
# NumberOfTimes90DaysLate - int
# NumberRealEstateLoansOrLines - int 
# NumberOfTime60-89DaysPastDueNotWorse - int
# NumberOfDependents - int
# Все остальные вроде тоже int'ы. Но можно проверить, например, так: print(type(data['NumberRealEstateLoansOrLines'][0]))

# Подзадание 6
data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
# Переименовали в Debt

# Подзадание 5
data.loc[data['MonthlyIncome'].notnull(), "Debt"] = data.loc[data['MonthlyIncome'].notnull(), "Debt"] * data.loc[data['MonthlyIncome'].notnull(), "MonthlyIncome"]
# Перевели относительный долг в абсолютный
print(data[["Debt", "Id"]])
# Проверили, что всё удалось

# Подзадание 7
mean = data.loc[data['MonthlyIncome'].notnull(), "MonthlyIncome"].mean()
# Вычислили среднее
data.loc[data['MonthlyIncome'].isnull(), "MonthlyIncome"] = mean
# Установили MonthlyIncome у людей с "по нулям" как среднее арифметическое по зп

# Подзадание 8
print(data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean())
# самая рискованная группа - люди с двумя иждивенцами (вероятно одинокие матери и отцы)

print(data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean())

# самые рискованные группы - люди с шестью ипотеками. Вероятно у нас просто нет данных о людях с пятью ипотеками (поэтому ноль). 
# Можно предположить, что если у человека больше 2-ух ипотек - он в группе риска

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
zeroDebts = data.loc[data["SeriousDlqin2yrs"] == 0]
zeroDebts = zeroDebts.loc[zeroDebts["MonthlyIncome"] != mean]
moreThanZeroDebts = data.loc[data["SeriousDlqin2yrs"] > 0]
#  удалили людей, которым назначили среднюю зарплату
moreThanZeroDebts = moreThanZeroDebts.loc[moreThanZeroDebts["MonthlyIncome"] != mean]


ax.scatter(zeroDebts['age'], zeroDebts["Debt"], c="blue")
ax.scatter(moreThanZeroDebts['age'], moreThanZeroDebts["Debt"], c="red")
#plt.scatter(zeroDebts['age'], zeroDebts['Debt'])
plt.show()

fig, ax = plt.subplots()
plt.xlim([0, 25000])
plt.title('Зарплата')
zeroDebts['MonthlyIncome'].plot.kde(ax=ax, label="Без серьезных задолжностей", color="#76D6FF")
moreThanZeroDebts['MonthlyIncome'].plot.kde(ax=ax, label="С серьезными задолжностями", color="#FF7E79")
plt.show()


incomeNoMoreThan25K = data.loc[data["MonthlyIncome"] <= 25000]
incomeNoMoreThan25K = data.loc[data["MonthlyIncome"] != mean]
#  удалили людей, которым назначили среднюю зарплату

plt.title("Взаимосвязь возраста и зарплаты")
# судя по данным отсутствует
plt.xlim([16, 100])
plt.ylim([0, 25000])
plt.plot(incomeNoMoreThan25K['age'],incomeNoMoreThan25K['MonthlyIncome'], 'o')
plt.show()

plt.title("Взаимосвязь возраста и числа иждивенцев")
# супер интересно (нет). Но похоже на Гауссово распределение
plt.xlim([16, 100])
plt.ylim([0, 20])
yint = range(int(incomeNoMoreThan25K['NumberOfDependents'].min()), int(incomeNoMoreThan25K['NumberOfDependents'].max())+20)
plt.yticks(yint)
plt.plot(incomeNoMoreThan25K['age'],incomeNoMoreThan25K['NumberOfDependents'], 'o')
plt.show()

plt.title("Взаимосвязь зарплаты и числа иждивенцев")
# судя по данным отсутствует
plt.xlim([0, 25000])
plt.ylim([0, 20])
yint = range(int(incomeNoMoreThan25K['NumberOfDependents'].min()), int(incomeNoMoreThan25K['NumberOfDependents'].max())+20)
plt.yticks(yint)
plt.plot(incomeNoMoreThan25K['MonthlyIncome'],incomeNoMoreThan25K['NumberOfDependents'], 'o')
plt.show()
