-- SQLite

INSERT INTO regionai(id, pavadinimas) VALUES
(1, 'Aukštaitijos'),
(2, 'Dzūkijos'),
(3, 'Suvalkijos'),
(4, 'Žemaitijos'),
(5, 'Mažosios Lietuvos');

INSERT INTO vietoves(id, pavadinimas, regionai_id) VALUES
(1, 'Panevėžio', 1),
(2, 'Jonavos', 1),
(3, 'Utenos', 1),
(4, 'Kėdainių', 1),
(5, 'Ukmergės', 1),
(6, 'Visagino', 1),
(7, 'Radviliškio', 1);