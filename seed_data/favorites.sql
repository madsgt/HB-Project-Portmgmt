-- PostgreSQL-create table to store clicks information for each symbol for all time

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(6) NOT NULL REFERENCES stocks,
    counter INTEGER NOT NULL DEFAULT 0
    CHECK (counter>0)
);

#included a check constraint to create table only when counter for the symbol is more than 0


-- Materialized view example
/*May not need this file*/


