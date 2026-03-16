-- Saldo promedio por cliente y variación por segmento
SELECT
    c.segmento,
    COUNT(DISTINCT c.cliente_id) AS total_clientes,
    AVG(t.monto) AS monto_promedio_transaccion
FROM
    clientes c
LEFT JOIN
    transacciones t ON c.cliente_id = t.cliente_id
GROUP BY 
    c.segmento;

-- Productos de ayor adopción en clientes jovenes vs mayores
SELECT
    CASE
        WHEN c.edad < 30 THEN 'Joven (18-29)'
        WHEN c.edad BETWEEN 30 AND 45 THEN 'Adulto (30-45)'
        WHEN c.edad BETWEEN 46 AND 60 THEN 'Maduro (46-60)'
        ELSE 'Senior (60+)'
    END AS rango_edad,
    p.producto,
    COUNT(*) AS total_clientes
FROM productos p
JOIN clientes c ON p.cliente_id = c.cliente_id
GROUP BY rango_edad, p.producto
ORDER BY rango_edad, total_clientes DESC;

-- Evolución del uso de app móvil en los últimos 6 meses (con window functions)
WITH uso_mensual AS (
    SELECT
        strftime('%Y-%m', fecha_hora) AS mes,
        COUNT(DISTINCT cliente_id) AS usuarios_activos
    FROM canales
    WHERE accion = 'Login'
    GROUP BY mes
)

SELECT 
    mes,
    usuarios_activos,
    LAG(usuarios_activos) OVER (ORDER BY mes) as mes_anterior,
    ROUND(100.0 * (usuarios_activos - LAG(usuarios_activos) OVER (ORDER BY mes)) / 
    LAG(usuarios_activos) OVER (ORDER BY mes), 2) as crecimiento_pct
FROM
    uso_mensual
ORDER BY 
    mes DESC
LIMIT 6;

-- Clientes con alta probabilidad de abandono (churn)
WITH ultimo_login AS (
    SELECT 
        cliente_id,
        MAX(fecha_hora) as ultima_vez
    FROM canales
    GROUP BY cliente_id
)

SELECT 
    c.cliente_id,
    c.edad,
    c.segmento,
    julianday('2025-01-01') - julianday(ul.ultima_vez) as dias_sin_actividad
FROM 
    clientes c
LEFT JOIN 
    ultimo_login ul ON c.cliente_id = ul.cliente_id
WHERE 
    julianday('2025-01-01') - julianday(ul.ultima_vez) > 30 
    OR ul.ultima_vez IS NULL
ORDER BY 
    dias_sin_actividad DESC;