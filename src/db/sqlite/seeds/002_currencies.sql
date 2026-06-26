-- ============================================================
-- SEED - CURRENCIES
-- ============================================================

INSERT OR IGNORE INTO currencies (
    code,
    name,
    symbol,
    iso_numeric,
    decimals,
    sort_order
)
VALUES
    ('EUR', 'Euro', 'EUR', 978, 2, 10),
    ('USD', 'US Dollar', '$', 840, 2, 20),
    ('GBP', 'Pound Sterling', 'GBP', 826, 2, 30),
    ('CHF', 'Swiss Franc', 'CHF', 756, 2, 40),
    ('JPY', 'Japanese Yen', 'JPY', 392, 0, 50),

    ('CAD', 'Canadian Dollar', 'CAD', 124, 2, 60),
    ('AUD', 'Australian Dollar', 'AUD', 036, 2, 70),
    ('NZD', 'New Zealand Dollar', 'NZD', 554, 2, 80),

    ('SEK', 'Swedish Krona', 'SEK', 752, 2, 90),
    ('NOK', 'Norwegian Krone', 'NOK', 578, 2, 100),
    ('DKK', 'Danish Krone', 'DKK', 208, 2, 110),

    ('HKD', 'Hong Kong Dollar', 'HKD', 344, 2, 120),
    ('SGD', 'Singapore Dollar', 'SGD', 702, 2, 130),
    ('CNY', 'Yuan Renminbi', 'CNY', 156, 2, 140),
    ('KRW', 'South Korean Won', 'KRW', 410, 0, 150),

    ('MXN', 'Mexican Peso', 'MXN', 484, 2, 160),
    ('BRL', 'Brazilian Real', 'BRL', 986, 2, 170),
    ('ZAR', 'South African Rand', 'ZAR', 710, 2, 180),

    ('PLN', 'Polish Zloty', 'PLN', 985, 2, 190),
    ('CZK', 'Czech Koruna', 'CZK', 203, 2, 200),
    ('HUF', 'Hungarian Forint', 'HUF', 348, 2, 210),
    ('RON', 'Romanian Leu', 'RON', 946, 2, 220);
