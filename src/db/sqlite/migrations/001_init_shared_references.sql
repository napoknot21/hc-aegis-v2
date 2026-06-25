CREATE TABLE IF NOT EXISTS quotes (

    id_quote        INTEGER PRIMARY KEY AUTOINCREMENT,

    category        TEXT    NOT NULL,
    author          TEXT    NOT NULL,
    quote           TEXT    NOT NULL,

    is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    sort_order      INTEGER NOT NULL DEFAULT 100,

    created_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (category, author, quote)

);

CREATE INDEX IF NOT EXISTS idx_quotes_category
ON quotes(category);

CREATE INDEX IF NOT EXISTS idx_quotes_author
ON quotes(author);

CREATE INDEX IF NOT EXISTS idx_quotes_active
ON quotes(is_active);

CREATE INDEX IF NOT EXISTS idx_quotes_sort_order
ON quotes(sort_order);

CREATE TABLE IF NOT EXISTS currencies (

    id_ccy          INTEGER PRIMARY KEY AUTOINCREMENT,

    code            TEXT    NOT NULL,
    name            TEXT    NOT NULL,

    symbol          TEXT,

    iso_numeric     INTEGER,
    decimals        INTEGER NOT NULL DEFAULT 2 CHECK (decimals BETWEEN 0 AND 8),

    is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    sort_order      INTEGER NOT NULL DEFAULT 100,
    created_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_currency_code_upper CHECK (code = UPPER(code)),

    UNIQUE (code),
    UNIQUE (iso_numeric)

);


CREATE INDEX IF NOT EXISTS idx_currencies_active 
ON currencies(is_active);

CREATE INDEX IF NOT EXISTS idx_currencies_sort_order 
ON currencies(sort_order);
