# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:57:28 2020

@author: evule
"""

import pandas as pd
import numpy as np
import math
import scipy.stats as stats

df=pd.read_excel(r'C:\Users\evule\Desktop\Riesgo de Mercado\Backtesting.xlsx')
df.reset_index

FechaCalculo='2019-02-03'
#FechaCalculo=input("ingrese fecha de calculo (yyyy-mm-dd): ")


i=df[df.Fecha==FechaCalculo].index.values

x=df.iloc[np.r_[i-249:i+1]]
y=df.iloc[np.r_[i-250:i],1]
z=pd.concat([x.reset_index(drop=True).Fecha,y.reset_index(drop=True),x.reset_index(drop=True)['Perdida real']],axis=1)


z['ExcepcionHoy']=(z['Perdida real']>z.VaR)*1


b=pd.DataFrame(np.zeros(shape=(1,1)))

ExcepcionAyer=z[:-1]['ExcepcionHoy']
z['ExcepcionAyerCompleta']=pd.concat([b,ExcepcionAyer], ignore_index=True)

z['a00']=(z.ExcepcionHoy+z.ExcepcionAyerCompleta)==0
z['a10']=(z.ExcepcionHoy==0)&(z.ExcepcionAyerCompleta==1)
z['a01']=(z.ExcepcionHoy==1)&(z.ExcepcionAyerCompleta==0)
z['a11']=(z.ExcepcionHoy+z.ExcepcionAyerCompleta)==2
print(z)

Excepciones=sum(z.ExcepcionHoy)
a00=sum(z.a00)
a10=sum(z.a10)
a01=sum(z.a01)
a11=sum(z.a11)



q0=a00/(a00+a01)
q1=a10/(a10+a11)
q=(a00+a10)/(a00+a01+a10+a11)
A=((q/q0)**a00)*(((1-q)/(1-q0))**a01)*((q/q1)**a10)*(((1-q)/(1-q1))**a11)
estimador=-2*math.log(A)
gl=1
confianza=0.99
critico=stats.chi2.ppf(q=confianza,df=gl)



print("Test de Kupiec:")
if Excepciones <=4:
    print("Tiene "+str(Excepciones) + " excepciones. Se encuentra en zona verde")
elif Excepciones<=9:
    print("Tiene "+str(Excepciones) + " excepciones. Se encuentra en zona amarilla")
else:
    print("Tiene "+str(Excepciones) + " excepciones. Se encuentra en zona roja")

print("Test de Christoffersen:")
if estimador>=critico:
    print("Se rechaza el test")
else:
    print("No se rechaza el test")
