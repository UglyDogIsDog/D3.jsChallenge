from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json

# Create your views here.

def index(request):
    data = {}
    
    return render(request, 'graph/index.html', data)


def task_1(request):
    df = pd.read_csv("temperature_daily.csv")
    df['month'] = df.apply(lambda row : row['date'][0 : 7], axis=1)
    df1 = df[['month', 'min_temperature']].groupby(['month']).min()
    df2 = df[['month', 'max_temperature']].groupby(['month']).max()
    df = df1.merge(df2, on=['month']).reset_index()
    data = df.to_dict(orient='records')
    
    return JsonResponse(data, safe=False)


def task_2(request):
    df = pd.read_csv("temperature_daily.csv")
    df['month'] = df.apply(lambda row : row['date'][0 : 7], axis=1)
    df = df[df['month'] > '2007']
    df_ = df.copy()
    df1 = df[['month', 'min_temperature']].groupby(['month']).min()
    df2 = df[['month', 'max_temperature']].groupby(['month']).max()
    df = df1.merge(df2, on=['month']).reset_index()
    data = df.to_dict(orient='records')

    df_['day'] = df_.apply(lambda row : int(row['date'][8 :]), axis=1)
    for record in data:
        record['detail'] = df_[df_['month'] == record['month']][['day', 'min_temperature', 'max_temperature']].to_dict(orient='records')
    
    return JsonResponse(data, safe=False)


def get_co_data():
    inp = open("HKUST_coauthor_graph.json")
    f = json.load(inp)
    data = {}
    count = {}
    id_cse = {}

    for node in f["nodes"]:
        if node["dept"] == "CSE":
            id_cse[node["id"]] = 1

    data["links"] = []
    for edge in f["edges"]:
        if id_cse.get(edge["source"], 0) == 1 and id_cse.get(edge["target"], 0) == 1:
            num = len(edge["publications"])
            count[edge["source"]] = count.get(edge["source"], 0) + num
            count[edge["target"]] = count.get(edge["target"], 0) + num
            data["links"] += [{
                "source": edge["source"],
                "target": edge["target"],
                "value": num
            }]

    data["nodes"] = []
    for p_id in count.keys():
        data["nodes"] += [{
            "id": p_id,
            "group": count[p_id]
        }]

    print(data)
    
    return data


def task_3(request):
    data = get_co_data()

    return JsonResponse(data, safe=False)