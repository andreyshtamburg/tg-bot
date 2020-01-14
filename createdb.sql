create table budget(
    codename varchar(255) primary key,
    budget_amount integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    inside_budget boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created date,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, inside_budget, aliases)
values
    ("REMOVALS", "Household Goods Shipping", true, "hhgs, bolongings shipping"),
    ("PETS", "Pet Shipping", true, "pet shipping, pets"),
    ("SERVICEDAPARTMENT", "Temporary Accommodation", true, "temp accommodation, housing, airbnb"),
    ("BROKERFEE", "Broker Fee", true, "broker, broker fee"),
    ("TRAVEL", "Travel", true, "uber, plane tickets, plane, flights, travel"),
    ("TAXMEETING", "Tax Return Preparation Assistance", false, "taxes, accountant"),
    ("HOMESEARCH", "Home Search", false, "home search"),
    ("IMMIGRATION", "Immigration", false, "visa, immigration, visa fee"),
    ("CROSSCULTURALTRAINING", "Cross Cultural Training", false, "cultural training, culture");


insert into budget(codename, budget_amount) values ('base', 10000);
