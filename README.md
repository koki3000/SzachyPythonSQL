Aplikacja potrzebuje sqlalchemy oraz PostgreSQL. Tabela w bazie danych "szachownica" ma 9 kolumn id oraz od a do h, oraz 8 rzędów o id od 1 do 8.

Kod sql do stworzenia tabeli:
CREATE TABLE szachownica (
    id SERIAL PRIMARY KEY,
    a VARCHAR,
    b VARCHAR,
    c VARCHAR,
    d VARCHAR,
    e VARCHAR,
    f VARCHAR,
    g VARCHAR,
    h VARCHAR
);
