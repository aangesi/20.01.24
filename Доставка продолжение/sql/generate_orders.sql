-- Генерация случайных заказов
INSERT INTO `Order` (user_id, address_from_geo_lat, address_from_geo_long, address_to_geo_lat, address_to_geo_long, trackers, invoice_id)
VALUES 
(1, 55.7558, 37.6173, 59.9343, 30.3351, '1,2', 1),
(2, 48.8566, 2.3522, 52.3791, 4.9009, '3,4', 2),
-- Пример продолжается для всех заказов...
(2000, 40.7306, -73.9352, 34.0522, -118.2437, '1999,2000', 2000);
