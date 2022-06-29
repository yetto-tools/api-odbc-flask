test = """
SELECT
    DAYOFWEEK(fecha) as dia,
    fecha,
    qsys_codigo_cliente,
    IF(
        qsys_codigo_cliente <> 000001,
        (
            SELECT
                DISTINCT(
                    TRIM(
                        REPLACE(
                            REPLACE(REPLACE(UPPER(nombre), " ", "{}"), "}{", ""),
                            "{}",
                            " "
                        )
                    )
                )
            FROM
                cxc_cliente
            WHERE
                cliente = qsys_codigo_cliente
        ),
        TRIM(
            REPLACE(
                REPLACE(REPLACE(nombre, " ", "{}"), "}{", ""),
                "{}",
                " "
            )
        )
    ) AS Nombre,
    sum(monto) as Monto,
    IF(credito, "CREDITO", "CONTADO") AS forma_pago
FROM
    inf_pedido pedido
WHERE
    '01'
    AND fecha BETWEEN ?
    AND ?
    AND qsys_vendedor = '332'
    AND credito = ?
    AND estado <> 9
GROUP BY
    fecha,
    Nombre
ORDER BY
    nombre,
    dia,
    fecha
"""




ESPECIALES_2_DEFAULT_CROM = """
            SELECT
            serie,pedido,
            fecha,qsys_codigo_cliente,
            nombre,monto,
            IF(credito,"CREDITO","CONTADO") AS forma_pago,
            factura_serie,
            factura,qsys_pedido
            FROM inf_pedido
            WHERE '01'
            AND fecha BETWEEN ? AND ?
            AND qsys_vendedor = 332
            AND estado <> 9
            ORDER BY fecha, nombre
            """

FILTRO_ESPECIALES2 = """
SELECT TRIM(REPLACE(REPLACE(REPLACE(nombre," ", "{}"),"}{", ""), "{}"," ")) as nombre, 
    dia,
    fecha,
    cliente,
    monto,
    ruta,
    consolidacion,
    forma_pago,
    qsys_nombre_cliente,
    num_dia
FROM 
    (SELECT
        DISTINCT(TRIM(p.nombre)) as nombre,
        UPPER(DAYNAME(cons.fecha)) as dia,
        cons.fecha,
        p.cliente,
        cons.monto,
        qsys_vendedor as ruta,
        cons.consolidacion,
        IF(credito, "CREDITO", "CONTADO") AS forma_pago,
        TRIM(qsys_nombre_cliente) as qsys_nombre_cliente,
        cons.num_dia
    FROM
        inf_pedido p
    INNER JOIN (
        SELECT
            TRIM(nombre) as nombre,
            fecha,
            COUNT(*) AS consolidacion,
            cliente,
            (SELECT DISTINCT(UPPER(nombre)) FROM cxc_cliente WHERE cliente = p.cliente) as qsys_nombre_cliente,
            SUM(CAST(monto as DECIMAL(18,2))) AS monto, 
            DAYOFWEEK(fecha)as num_dia
        FROM
            inf_pedido p
        where
            '01'
            AND qsys_vendedor = 332
            AND fecha BETWEEN ?
            AND ?
            AND credito = ?
        GROUP BY
            nombre,
            fecha,
            num_dia
    ) cons ON cons.nombre = p.nombre
    
WHERE
    '01'
    AND p.fecha BETWEEN ?
    AND ?
    AND qsys_vendedor = 332
    AND estado <> 9 -- ORDER by cons.fecha, p.nombre
ORDER BY
    p.nombre,
    cons.fecha) AS ESPECIEALES;

"""



ESPECIALES_2_TO_EXCEL ="""
SELECT
    fecha,
    DAYOFWEEK(fecha) as dia,
    qsys_codigo_cliente,
        IF( qsys_codigo_cliente <> 000001, (SELECT DISTINCT(UPPER(TRIM(TRIM(REPLACE(REPLACE(REPLACE(nombre," ", "{}"),"}{", ""), 
        "{}"," "))))) FROM cxc_cliente WHERE cliente = inf_pedido.cliente), TRIM(REPLACE(REPLACE(REPLACE(nombre," ", "{}"),"}{", ""), 
        "{}"," "))) AS nombre_de_cliente,
    monto,
    IF(credito, "CREDITO", "CONTADO") AS forma_pago
FROM
    inf_pedido
WHERE
    '01'
    AND fecha BETWEEN ?
    AND ?
    AND qsys_vendedor = 332
    AND credito = ?
    AND estado <> 9
ORDER BY
    nombre_de_cliente,fecha
"""


PAGOS_FACTURAS =            """
            SELECT 
                (SELECT nombre FROM sis_empresa WHERE empresa = f.empresa) AS empresa,
                f.serie, 
                f.factura, 
                f.fecha, 
                f.monto, 
                f.cliente, 
                f.nit, 
                f.nombre, 
                f.direccion, 
                f.qsys_codigo_cliente,
                f.fel_fecha AS fecha_pago,
                f.forma_pago 
            FROM inf_factura AS f
            WHERE factura = ?  -- 69650 -- 23657
                AND forma_pago = 2
                AND FECHA > ?       -- '2022-01-01'
                AND estado <>9;
            """