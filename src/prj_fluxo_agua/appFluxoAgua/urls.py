from django.urls import path, re_path
from .views import index,ler_fluxo, graf_consumo, graf_conta, analisar_fluxo, analisar_consumo


urlpatterns = [
    path("",index,name="inicial"),
    path("lerfluxo",ler_fluxo, name="lerfluxo"),
    path("grafconsumo", graf_consumo, name="grafconsumo"),
    path("grafconta", graf_conta, name="grafconta"),
    path("analisarfluxo", analisar_fluxo, name="analisarfluxo"),
    path("analisarconsumo", analisar_consumo, name="analisarconsumo")

]


