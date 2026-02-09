CREATE TABLE university (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    country NVARCHAR(255) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    founded INT NOT NULL,
    type NVARCHAR(255) NOT NULL,
    enrollment BIGINT NOT NULL,
    link NVARCHAR(255) NOT NULL,
    CONSTRAINT unique_combination UNIQUE (country, name)
);