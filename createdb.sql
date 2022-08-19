create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
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

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукты", true, "еда, магазин"),
    ("house", "дом", true, "в дом, house, home, fix price, посуда, хоз, хоз товары, туалет"),
    ("clothes", "вещи", true, "шмотки, обновки"),
    ("dinner", "обед", true, "столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("work", "работа", true, "локтар, тх, work, working"),
    ("cafe", "кафе", false, "ресторан, кофейня, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
    ("transport", "общ. транспорт", false, "метро, автобус, metro, subway, маршрутка, bus"),
    ("taxi", "такси", false, "яндекс такси, yandex taxi, taxi"),
    ("phone", "телефон", false, "билайн, связь"),
    ("books", "книги", false, "книга, литература, литра, лит-ра"),
    ("internet", "интернет", false, "инет, интернет, inet"),
    ("gifts", "подарки", false, "подарок, present, презентs"),
    ("subscriptions", "подписки", false, "подписка"),
    ("other", "прочее", true, "");
