
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import json
from pandas import json_normalize
import re

file_path = './finished/'
file_name = 'war20240914.json'

full_path = os.path.join(file_path, file_name)

with open(full_path, 'r') as json_file:
    response = json.load(json_file)

data = json_normalize(response, record_path=['clan', 'members'])

members_df = json_normalize(response, record_path=['clan', 'members'], meta=[])
total_members_df = members_df.copy()

try:
    attacks_df = json_normalize(
        members_df.to_dict(orient='records'),  # Convert DataFrame to dicts
        record_path='attacks',
        meta=['name'],
        meta_prefix='member_'
    )

except KeyError:
    attacks_df = pd.DataFrame(columns=[
        'attackerTag', 'defenderTag', 'stars', 'destructionPercentage',
        'order', 'duration', 'member_name'
    ])

attacks_df['attack_num'] = attacks_df.groupby('member_name').cumcount() + 1
attacks_df['total_attacks'] = attacks_df.groupby(
    'member_name')['attack_num'].transform('max')


total_attacks_df = attacks_df[[
    'member_name', 'total_attacks']].drop_duplicates().set_index('member_name')


pivot_df = attacks_df.pivot_table(
    index=['member_name'],
    columns='attack_num',
    values=[
        'attackerTag',
        'defenderTag',
        'stars',
        'destructionPercentage',
        'order',
        'duration'],
    aggfunc='first'
)
pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]

def extract_text_and_number(column_name):
    match = re.match(r'(.+?)_(\d+)', column_name)
    return (int(match.group(2)), match.group(
        1)) if match else (float('inf'), column_name)

sorted_columns = sorted(
    pivot_df.columns,
    key=lambda x: extract_text_and_number(x))

pivot_df = pivot_df[sorted_columns]
final_df = pivot_df.join(total_attacks_df)

new_name_df = final_df
new_name_df['Avg %'] = new_name_df[[
    'destructionPercentage_1', 'destructionPercentage_2']].mean(axis=1)
new_name_df['Total Stars'] = new_name_df[["stars_1", "stars_2"]].sum(axis=1)

new_order = ['total_attacks', 'Avg %', 'destructionPercentage_1', 'destructionPercentage_2',
             'stars_1', 'stars_2', 'Total Stars']
new_name_df = new_name_df[new_order]
final_name_df = new_name_df.rename(columns={'destructionPercentage_1': 'Attack 1 %', 'destructionPercentage_2': 'Attack 2 %',
                                            'stars_1': 'Attack 1 Stars', 'stars_2': 'Attack 2 Stars', 'total_attacks': 'Total Attacks'})

try:
    total_members_df = total_members_df.set_index('name')
except KeyError:
    pass

final_name_df["Total Clan Stars"] = final_name_df['Total Stars'].sum()
combined_df = final_name_df.reindex(total_members_df.index)
combined_df.fillna(0, inplace=True)
combined_df.sort_values(
    ["Total Attacks", 'Total Stars', 'Avg %'], ascending=False, inplace=True)

def colors(row):
    if row['Total Attacks'] == 2.0:
        # color = "rgb(0,255,0)" # For Online Viewer
        color = "green"  # For Excel
    elif row['Total Attacks'] == 1.0:
        color = "yellow"
    else:
        color = "red"
    return [f'color: {color}'] * len(row)

styled_df = combined_df.style.apply(colors, axis=1).format('{:.1f}')
new_file = file_name.replace('.json', '.xlsx')
styled_df.to_excel(f'./charts/{new_file}', engine='openpyxl', index=True)
# combined_df.to_csv('./charts/data.csv', index=True)
# combined_df.to_json('./charts/data.json', orient='records', lines=True, index=True)
# combined_df.to_json('./charts/datai.json', orient='index')
# combined_df.to_json('./charts/datas.json', orient='split')
# combined_df.to_json('./charts/datat.json', orient='table')
# combined_df.to_html('./charts/data.html', index=True)
