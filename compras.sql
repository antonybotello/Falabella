
-- Compras para Ana Pérez (asumiendo cliente_id=1) - Califica para Fidelización
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(1, '2025-04-24 10:30:00', 3000000.00, 'Equipo de cómputo avanzado'),
(1, '2025-04-26 15:45:00', 2500000.00, 'Licencias de software especializado'),
(1, '2025-03-10 11:00:00', 1000000.00, 'Consultoría de marzo'); -- Fuera del mes de reporte

-- Compras para Carlos Gómez (asumiendo cliente_id=2) - No califica (monto bajo en abril)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(2, '2025-04-10 09:15:00', 1500000.00, 'Mobiliario de oficina estándar'),
(2, '2025-05-02 14:00:00', 500000.00, 'Servicio de mantenimiento preventivo'); -- Fuera del mes de reporte

-- Compras para Luisa Martínez (asumiendo cliente_id=3) - No califica (fecha fuera de abril para monto alto)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(3, '2025-03-20 16:00:00', 6000000.00, 'Desarrollo web integral (marzo)'),
(3, '2025-05-08 12:30:00', 200000.00, 'Hosting y dominio mayo');

-- Compras para Javier Díaz (asumiendo cliente_id=4)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(4, '2025-04-25 18:00:00', 750000.00, 'Material publicitario impreso'),
(4, '2025-02-05 10:00:00', 300000.00, 'Diseño de logo');

-- Compras para Sofia Luna (asumiendo cliente_id=5)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(5, '2025-04-20 11:00:00', 250000.00, 'Suscripción mensual software A'),
(5, '2025-04-28 14:20:00', 300000.00, 'Capacitación online'); -- Total Abril: 550,000

-- Compras para Mateo Rojas (asumiendo cliente_id=6)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(6, '2025-02-15 14:30:00', 150000.00, 'Accesorios varios'),
(6, '2025-03-22 09:00:00', 300000.00, 'Repuestos y consumibles');

-- Compras para Valentina Silva (asumiendo cliente_id=7)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(7, '2025-01-10 16:45:00', 50000.00, 'Diagnóstico técnico inicial'); -- Compra antigua y pequeña

-- Compras para Lucas Herrera (asumiendo cliente_id=8)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(8, '2025-05-03 11:30:00', 750000.00, 'Renovación de servicio X'),
(8, '2025-04-01 09:00:00', 400000.00, 'Soporte técnico abril');

-- Compras para Isabella Cruz (asumiendo cliente_id=9)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(9, '2025-04-03 17:10:00', 1200000.00, 'Componentes electrónicos'),
(9, '2025-04-15 12:00:00', 800000.00, 'Instalación y configuración'), -- Total Abril: 2,000,000
(9, '2025-02-10 13:00:00', 500000.00, 'Plan de datos febrero');

-- Compras para Daniel Ortiz (asumiendo cliente_id=10)
INSERT INTO sac_app_compra (cliente_id, fecha_compra, monto_compra, descripcion) VALUES
(10, '2023-11-05 09:30:00', 4500000.00, 'Implementación de sistema (antiguo)'),
(10, '2025-01-20 10:15:00', 200000.00, 'Actualización menor sistema');