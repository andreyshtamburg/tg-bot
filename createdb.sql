create table budget(
    codename varchar(255) primary key,
    budget_amount real
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    inside_budget boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount real,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, inside_budget, aliases)
values
    ("REMOVALS", "Household Goods Shipping", true, "hhgs, bolongings shipping, goods shipping, sending belongings"),
    ("PETS", "Pet Shipping", true, "pet shipping, pets shipping"),
    ("SERVICEDAPARTMENT", "Temporary Accommodation", true, "temp accommodation, housing, airbnb"),
    ("BROKERFEE", "Broker Fee", true, "broker fee"),
    ("TRAVEL", "Travel", true, "plane tickets, flights, travel, taxi, cab, uber, bolt, lyft"),
    ("TAXMEETING", "Tax Return Preparation Assistance", false, "taxes, accountant, tax return assistance"),
    ("HOMESEARCH", "Home Search", false, "home search, house search"),
    ("IMMIGRATION", "Immigration", false, "immigration, visa fee"),
    ("CROSSCULTURALTRAINING", "Cross Cultural Training", false, "culture, cross cuclutal training");


insert into budget(codename, budget_amount) values ('budget', 10000);
