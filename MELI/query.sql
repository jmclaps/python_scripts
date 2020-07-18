-- ## Ejercicio - SQL + Propuesta

-- **1.** Obtener para el mes 1 cuánto costaría enviar con cada carrier la totalidad de los envíos 
-- mencionados en "Cantidad de envíos" sin tener en cuenta la capacidad del carrier


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

-- **2.** ¿Qué propuesta harías considerando un presupuesto de $3.000.000 y los datos del mes 1?

-- Si considero que el capacity es mensual pero no por zona (es decir que los 10.000 del Carrier 1 es 
-- su cuota máxima independiente de la zona) solo puedo entregar 23.000 envíos del total 150.000 envíos 
-- que tengo que realizar y hay múltiples maneras de imputarlo dependiendo de lo que querramos:
-- 1) Por Costos asignaría la mayor cantidad de envíos al carrier según el precio
--     * Por ejemplo los 10.000 del Carrier 1 se asignarían a AMBA y así con cada uno
-- 2) Sí quisiera distribuir en todas las regiones hay que analizar los límites zonales de los Carrier
--     * Por ejemplo el Carrier 3 solo entrega en AMBA así que su capacidad iría ahí y el resto por costos
-- 3) Podría querer minimizar los tiempos de entrego y por tanto todo se entregaría en AMBA de nuevo
--     * Básicamente porque todos los Carrier entregan más rápido en AMBA
    
-- Siendo que la única manera de gastarme todo el presupuesto es suponer capacidades infinitas de los 
-- carrier lo que haría es ir asignarlas por costo mínimo de zona

-- **3.** ¿Qué query utilizaste?

--- En sí no utilizaría una única query porque lo veo más como un análisis, descartando los primeros 
-- puntos (suposición de limite en capacidad) porque supongo que el ejercicio no iba por ahí una de las 
-- querys que haría es:

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

-- La diferencia de entre los 4,3 millones de costo mínimo teórico y los 3 millones dependerá de que se 
-- desea priorizar, pero siendo que probablemente sea la mayor cantidad de entregas al menor costo 
-- posible sin contemplar la zona lo mejor sería descontar de la zona Resto envíos ya que presenta el 
-- mayor costo de entrega.