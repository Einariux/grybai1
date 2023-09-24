-- SQLite

INSERT INTO regionas(pavadinimas) VALUES
('Aukštaitijos'),
('Dzūkijos'),
('Suvalkijos'),
('Žemaitijos'),
('Mažosios Lietuvos');

INSERT INTO vietove(pavadinimas, regionas_id) VALUES
('Panevėžio', 1),
('Jonavos', 1),
('Utenos', 1),
('Kėdainių', 1),
('Ukmergės', 1),
('Visagino', 1),
('Radviliškio', 1);


INSERT INTO grybas(pavadinimas, klase, vietove_id) VALUES
('Baravykas', 'Papėdgrybiai', 10),
('Baravykas', 'Papėdgrybiai', 2),
('Raudonviršis','Papėdgrybiai', 21),
('Raudonviršis','Papėdgrybiai', 19),
('Raudonviršis','Papėdgrybiai', 8),
('Gelsvoji musmirė', 'Papėdgrybiai', 3),
('Gelsvoji musmirė', 'Papėdgrybiai', 12);