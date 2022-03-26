import subprocess
import pandas as pd

# capture output from command "ps aux"
res = subprocess.run('ps aux', shell=True, capture_output=True, text=True).stdout

# split text in rows by delimeter "/n"
list1 = res.split('\n')

# split every row in columns
list2 = [i.split(maxsplit=10) for i in list1]

# create pandas DataFrame as we have tabular data
df = pd.DataFrame(list2[1:], columns=list2[0])

# remove None processes
df = df[df.USER.notna()]

# Пользователи системы: 'root', 'user1', ...
users = list(df.USER.unique())

# Процессов запущено: 833
cnt_ps = df.shape[0]

# Пользовательских процессов:
# root: 533
# user1: 231
user_proccesses = df.USER.value_counts().reset_index().rename(columns={'index': 'user', 'USER': 'cnt_proccess'})

# Всего памяти используется: 5.3 %
df['%MEM'] = df['%MEM'].astype(float)
memory_usage = df['%MEM'].sum()

# Всего CPU используется: 33.2%
df['%CPU'] = df['%CPU'].astype(float)
cpu_usage = df['%CPU'].sum()

# Больше всего памяти использует: (%имя процесса, первые 20 символов если оно длиннее)
max_memory_usage = df[df['%MEM'] == df['%MEM'].max()].iloc[0, 10][:20]

# Больше всего CPU использует: (%имя процесса, первые 20 символов если оно длиннее)
max_cpu_usage = df[df['%CPU'] == df['%CPU'].max()].iloc[0, 10][:20]

template = f'''
Отчёт о состоянии системы:
Пользователи системы: {users}
Процессов запущено: {cnt_ps}
Пользовательских процессов:
{user_proccesses}

Всего памяти используется: {memory_usage:.1f}%
Всего CPU используется: {cpu_usage:.1f}%
Больше всего памяти использует: {max_memory_usage}
Больше всего CPU использует: {max_cpu_usage}
'''

# save in file: report.txt
with open('report.txt', 'w') as f:
    print(template, file=f)

# print in console
print(template)