from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import datetime
from . import mqtt
import pandas as pd
import os.path
from random import random
from time import sleep
import json

def carregar_dataframe():
    dataframe = pd.read_csv("fluxoagua.csv", sep='[,|;]', engine='python')
    #dataframe.drop_duplicates('data', inplace=True) # Elimina dados duplicados em relação ao momento (data, hora, minutos, segundos iguais)

    return dataframe

def retornar_comparador(valor):
    comparadores = [">", ">=", "<", "<=", "==", "!="]
    return comparadores[int(valor)]
 
def retornar_operador(valor):
    operadores = ["&", "|"]
    return operadores[int(valor)]    

def calcular_media(dataframe):
    media = dataframe.mean()
    return media
    
def calcular_desvio(dataframe):
    desvio = dataframe.std()
    return desvio
    
def calcular_mediana(dataframe):
    mediana = dataframe.median()
    return mediana

def calcular_maior(dataframe):
    maior = dataframe.max()
    return maior

def calcular_menor(dataframe):
    menor = dataframe.min()
    return menor
    
def calcular_mediana(dataframe):
    mediana = dataframe.median()
    return mediana

def calcular_moda(dataframe):
    moda = dataframe.mode()
    return moda

def analisar_consumo(request):
    dataframe = carregar_dataframe()
    tempo_inicial = request.GET.get('tempo_inicial')
    tempo_final = request.GET.get('tempo_final')
    op_inicial = request.GET.getlist('op_inicial')[0]
    op_final = request.GET.getlist('op_final')[0]
    op_logico = request.GET.getlist('op_logico')[0]
  
    print("Operadores")
    print(op_inicial, op_final, op_logico)
    if len(tempo_inicial) == 0:
        tempo_inicial = "00:00:00"
    if len(tempo_final) == 0:
        tempo_final = "00:00:00"
  
    data_inicial = datetime.datetime.strptime(request.GET.get('data_inicial') + ' ' + tempo_inicial,'%Y-%m-%d %H:%M:%S')
    data_final =  datetime.datetime.strptime(request.GET.get('data_final') + ' ' + tempo_final, '%Y-%m-%d %H:%M:%S')
  
    comp_inicial = retornar_comparador(op_inicial)
    comp_final = retornar_comparador(op_final)
    op_logico = retornar_operador(op_logico)
    
    # Convert the date to datetime64
    dataframe['data'] = pd.to_datetime(dataframe['data'], format='%d/%m/%Y %H:%M:%S')
    
    expressao_consulta = '(dataframe["data"] ' + comp_inicial + ' data_inicial) ' + op_logico + ' (dataframe["data"] ' + comp_final +  ' data_final)'
   
    print(expressao_consulta)
    selecao = (eval(expressao_consulta))
    
    print(selecao)
    dataframe = dataframe[selecao]
    
    # tratamento outlier (máximo e mínimo)
    media = calcular_media(dataframe["medida"])
    desvio = calcular_desvio(dataframe["medida"])
    outlier_max = media + desvio
    outlier_min = media - desvio
    expressao_consulta = expressao_consulta + ' & (dataframe["medida"] <= outlier_max) & (dataframe["medida"] >= outlier_min)'
    selecao = (eval(expressao_consulta))
    dataframe = dataframe[selecao]
    # fim do tratamento de outlier
    
    media = calcular_media(dataframe["medida"])
    desvio = calcular_desvio(dataframe["medida"])
    maior = calcular_maior(dataframe["medida"])
    menor = calcular_menor(dataframe["medida"])
    mediana = calcular_mediana(dataframe["medida"])
    moda = calcular_moda(dataframe["medida"])
    
    
    print("Soma: ", dataframe["medida"].sum())
    
    try:
        medidas = {
        'media': float(media),
        'desvio': float(desvio),
        'maior': float(maior),
        'menor': float(menor),
        'mediana': float(mediana),
        'moda': float(moda)
        
         }
        json_medidas = json.dumps(medidas, indent=4)
        print(medidas)
    
        print(type(data_inicial), data_final, tempo_inicial, tempo_final)
    
        return JsonResponse(json_medidas, safe=False) 
        
    except:
        
        return HttpResponse('<span id="informacao" > <strong>Sem Informações a Exibir! <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-eye-slash text-primary" viewBox="0 0 16 16"> \
  <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/> \
  <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"/> \
  <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"/>\
</svg> </strong> </span>') 
    
     
def analisar_fluxo(request):
    return render(request,"ferramentas.html")

    
def index(request):
    return render(request,"index.html", context={"text":"Hello world"})
   

    
def ler_fluxo(request):
    dataframe = carregar_dataframe()
    print(dataframe)
    dataframe = dataframe.tail(20)
    
    tabela = dataframe[::-1].to_html(index=False)
    return JsonResponse(tabela, safe=False )

    
# TARIFAS DE AGUA SANOR RESOLUÇÃO ARES-PCJ N 489, 28/04/2023
# CATEGORIA RESIDENCIAL NORMAL - RN
# transforma de mililitros para m3
def transformar_ml_m3(ml):
    m3 = ml * 10e-6
    return m3

def transformar_l_m3(l):
    m3 = l * 10e-4
    return m3
    
# calcula a tarifa de agua da Sanor para RN
def calcular_conta_agua(unidade=0,categoria="RN"):
    m3 = transformar_l_m3(unidade)
    if m3 <=10:
        return 26.83
    elif m3 >= 11 and m3 <= 20:
        return  m3 * 3.74
    elif m3 >= 21 and m3 <= 50:
        return m3 * 5.76
    else:
        return m3 * 6.88
        
def escrever_arquivo(dados):
    data = datetime.datetime.today()
    data = data.strftime("%d/%m/%Y %H:%M:%S")
    
    if os.path.exists("fluxoagua.csv"):
        with open("fluxoagua.csv","a") as file:
            file.writelines("{:.2f},".format(dados))
            file.writelines(f"{data}")
            file.writelines("\n")
            sleep(1)
    else:
        with open("fluxoagua.csv","x") as file:
            file.writelines("medida,data\n")
            file.writelines("{:.2f},".format(dados))
            file.writelines(f"{data}")
            file.writelines("\n")
            sleep(1)
            
def graf_conta(request):
    json_conta = grafico_consumo_conta()
    
    return JsonResponse(json_conta[1], safe=False)


# Retorna uma lista consumo na posição 0, conta na posição 1
def grafico_consumo_conta():
    dataframe = carregar_dataframe()
    hoje = datetime.datetime.today()
    mes  = hoje.month
    ano = hoje.year
    consumo = {}
    conta = {}
    lst_json = []
    
    # Convert the date to datetime64
    dataframe['data'] = pd.to_datetime(dataframe['data'], format='%d/%m/%Y %H:%M:%S')
    dataframe['mes'] = dataframe['data'].dt.month 
    dataframe['ano'] = dataframe['data'].dt.year 
    
    selecao = (dataframe["mes"] == mes) &  (dataframe["ano"] == ano)
    
    json_medida_mes = dataframe[selecao].groupby(dataframe["mes"])["medida"].sum().to_json()
    dicionario  = json.loads(json_medida_mes)
    
    print(dicionario)
    mes_nome = retornar_nome_mes(mes)
    consumo[f'{mes_nome}'] = dicionario[str(mes)]
    json_consumo = json.dumps(consumo)
    total_mm = dicionario[f'{mes}']
    conta[f'{mes_nome}'] = calcular_conta_agua(total_mm)
    json_conta = json.dumps(conta)
    
    lst_json.append(json_consumo)
    lst_json.append(json_conta)
    
    return lst_json
     
def graf_consumo(request):

    json_consumo = grafico_consumo_conta()
    
    return JsonResponse(json_consumo[0], safe=False)
         
total_fluxo = 0.0               
# salva o fluxo em um arquivo csv
def salvar_fluxo(msg_fluxo):
   
    global total_fluxo 
    
    total_fluxo = total_fluxo + float(msg_fluxo)
    print("Fluxo",msg_fluxo)
    if msg_fluxo > 0.0:
        escrever_arquivo(msg_fluxo)
                
        # sei que o arquivo mudou, pois o msg_fluxo > 0, sendo assim linhas serão escritas no arquivo              
    return total_fluxo

def retornar_nome_mes(mes):
    meses = {1:"Janeiro", 2:"Fevereiro", 3:"Março", 
             4:"Abril", 5:"Maio", 6:"Junho", 7:"Julho", 8:"Agosto", 
             9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"
             }
    for m in meses:
        if(m == mes):
            return (meses[m])