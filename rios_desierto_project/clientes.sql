-- SQLite

INSERT INTO sac_app_cliente (tipo_documento_id, numero_documento, nombre, apellido, correo, telefono, fecha_registro) VALUES
(
    1,  -- CC (id=1)
    '123456789', 
    'Ana', 
    'Pérez Gómez', -- Cliente para fidelización
    'ana.perez@example.com', 
    '3001234567', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-25 days')
), -- Cliente con futuro id=1
(
    2,  -- CE (id=2)
    'CE1122334', 
    'Carlos', 
    'Gómez Rodríguez', 
    'carlos.gomez@example.com', 
    '3109876543', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-155 days')
), -- Cliente con futuro id=2
(
    3,  -- PP (id=3)
    'PP5566778', 
    'Luisa', 
    'Martínez Vargas', 
    'luisa.martinez@example.com', 
    '3205550011', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-305 days')
), -- Cliente con futuro id=3
(
    1, -- CC (id=1)
    '445566778',
    'Javier',
    'Díaz López',
    'javier.diaz@example.com',
    '3501112233',
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-10 days')
), -- Cliente con futuro id=4
(
    2,  -- CE (id=2)
    'CE2345678', 
    'Sofia', 
    'Luna Mora', 
    'sofia.luna@example.com', 
    '3012345678', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-15 days') 
), -- Cliente con futuro id=5
(
    3,  -- PP (id=3)
    'PP8002345', 
    'Mateo', 
    'Rojas Castillo', 
    'mateo.rojas@example.com', 
    '3119876543', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-255 days')
), -- Cliente con futuro id=6
(
    1,  -- CC (id=1)
    '778899001', 
    'Valentina', 
    'Silva Pinto', 
    'valentina.silva@example.com', 
    '3215550012', 
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-8 days')
), -- Cliente con futuro id=7
(
    2, -- CE (id=2)
    'CE3456789',
    'Lucas',
    'Herrera Suárez',
    'lucas.herrera@example.com',
    '3511112234',
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-65 days')
), -- Cliente con futuro id=8
(
    3, -- PP (id=3)
    'PP9012345',
    'Isabella',
    'Cruz Forero',
    'isabella.cruz@example.com',
    '3057654321',
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-95 days')
), -- Cliente con futuro id=9
(
    1, -- CC (id=1)
    '600700800',
    'Daniel',
    'Ortiz Parra',
    'daniel.ortiz@example.com',
    '3151237890',
    strftime('%Y-%m-%d %H:%M:%S', 'now', '-405 days')
); -- Cliente con futuro id=10