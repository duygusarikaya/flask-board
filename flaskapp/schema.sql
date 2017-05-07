drop table if exists entries;
drop table if exists feedback;

create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);


create table feedback (
  id integer primary key autoincrement,
  'name' text not null,
  surname text not null,
  email text not null,
  subject text not null,
  'text' text not null
);