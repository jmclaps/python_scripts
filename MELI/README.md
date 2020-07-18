# Manuel de uso de script

## Ejercicio - Análisis / Investigación
Los llamados a la API están hechos en Python 3.7 dentro de un jupyter notebook y utiliza las siguientes librerías:
  pandas 1.0.1
  requests 2.22.0

1. Para poder ejecutarlo sería necesario tener instalado Anaconda en la maquina.</br>
[Anaconda MacOS](https://repo.anaconda.com/archive/Anaconda3-2020.02-MacOSX-x86_64.pkg)</br>
[Anaconda Win64](https://repo.anaconda.com/archive/Anaconda3-2020.02-Windows-x86_64.exe)</br>
[Como instalar Anaconda](https://docs.anaconda.com/anaconda/install/windows/)
2. Luego de seguir las instrucciones del link solo restaría ejecutar el siguiente comando en el directorio donde este el script:
<pre><code>jupyter notebook</code></pre>

Como alternativa dejo también un archivo test_MELI.py que ejecuta fuera de Jupyter solo con Python y las librerías ya mencionadas.

El Script hace una conexión buscando los artículos y después por cada artículo busca el nombre de la categoría en el que está publicado.

## Ejercicio - SQL + Propuesta

**1.** Obtener para el mes 1 cuánto costaría enviar con cada carrier la totalidad de los envíos mencionados en "Cantidad de envíos" sin tener en cuenta la capacidad del carrier

<pre><code>
select 
      cr.Name as carrier
      ,SUM(ce.[Cantidad de envíos]*cs.Costo) as costoTotalEnvios
from 
      [Cantidad de envíos] as ce
      inner join Costos as cs on cs.Zona = ce.Zona
      inner join Carrier as cr on cr.CarrierID = cs.CarrierID
where
      ce.Mes = 1
group by
      cr.Name
</code></pre>

**2.** ¿Qué propuesta harías considerando un presupuesto de $3.000.000 y los datos del mes 1?

Si considero que el capacity es mensual pero no por zona (es decir que los 10.000 del Carrier 1 es su cuota máxima independiente de la zona) solo puedo entregar 23.000 envíos del total 150.000 envíos que tengo que realizar y hay múltiples maneras de imputarlo dependiendo de lo que querramos:
1) Por Costos asignaría la mayor cantidad de envíos al carrier según el precio
    * Por ejemplo los 10.000 del Carrier 1 se asignarían a AMBA y así con cada uno
2) Sí quisiera distribuir en todas las regiones hay que analizar los límites zonales de los Carrier
    * Por ejemplo el Carrier 3 solo entrega en AMBA así que su capacidad iría ahí y el resto por costos
3) Podría querer minimizar los tiempos de entrego y por tanto todo se entregaría en AMBA de nuevo
    * Básicamente porque todos los Carrier entregan más rápido en AMBA
    
Siendo que la única manera de gastarme todo el presupuesto es suponer capacidades infinitas de los carrier lo que haría es ir asignarlas por costo mínimo de zona

**3.** ¿Qué query utilizaste?

En sí no utilizaría una única query porque lo veo más como un análisis, descartando los primeros puntos (suposición de limite en capacidad) porque supongo que el ejercicio no iba por ahí una de las querys que haría es:

<pre><code>
select
    SUM(ce.[Cantidad de envíos]*cs.Costos) as costoMinTeorico
from
    Costos as cs
    inner join (select
                    cs.Zona, MIN(cs.Costo) as minCost
                from 
                    Costos as cs) as minCostZona on minCostZona.Zona = cs.Zona
    inner join [Cantidad de envíos] as ce on ce.Zona = cs.Zona
where
    minCostZona.minCost = cs.Costo
</code></pre>

La diferencia de entre los 4,3 millones de costo mínimo teórico y los 3 millones dependerá de que se desea priorizar, pero siendo que probablemente sea la mayor cantidad de entregas al menor costo posible sin contemplar la zona lo mejor sería descontar de la zona Resto envíos ya que presenta el mayor costo de entrega.
