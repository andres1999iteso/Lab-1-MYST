from matplotlib import pyplot as plt
import main

#Pasivo
#Grafica de rendimientos

fig0, ax = plt.subplots()
ax.plot(main.df_pasiva['Date'],main.df_pasiva['Rendimiento'] )
plt.xlabel('Fecha')
plt.ylabel('Rendimiento')
plt.grid()
plt.show()

#Evolución de portafolio
fig1, ax = plt.subplots()
ax.plot(main.df_pasiva['Date'],main.df_pasiva['Valor portafolio'] )
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.grid()
plt.show()

#Activo

#Grafica de rendimientos

fig2, ax = plt.subplots()
ax.plot(main.df_activa['Date'],main.df_activa['Rendimiento'] )
plt.xlabel('Fecha')
plt.ylabel('Rendimiento')
plt.grid()
plt.show()

#Evolución de portafolio
fig3, ax = plt.subplots()
ax.plot(main.df_activa['Date'],main.df_activa['Valor portafolio'] )
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.grid()
plt.show()

#EMV
fig4 = plt.subplots()

plt.scatter(main.portafolios['Vol'],main.portafolios['Media'],c=main.portafolios['RS'],
           cmap='RdYlBu', label='Portafolios simulados')
plt.colorbar()

plt.plot(main.port_EMV_montecarlo['Vol'],main.port_EMV_montecarlo['Media'],'*r',ms=10,label='Portafolio EMV')
plt.xlabel('Volatilidad')
plt.ylabel('Rendimeinto')
plt.grid()
plt.show()