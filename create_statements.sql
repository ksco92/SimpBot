create table users
(
  discord_user_id varchar(30),
  custom_nickname varchar(30),
  primary key (discord_user_id)
);

insert into users (discord_user_id, custom_nickname)
values ('ksco92#3832', 'rodrigo');
insert into users (discord_user_id, custom_nickname)
values ('Fusukok#6888', 'charlie');
insert into users (discord_user_id, custom_nickname)
values ('zion_89#3240', 'rick');
insert into users (discord_user_id, custom_nickname)
values ('4ll_F1ct10n#4422', 'adam');
insert into users (discord_user_id, custom_nickname)
values ('notfelipe#7884', 'feli');

drop table feli_point_transactions;
create table feli_point_transactions
(
  transaction_id       serial,
  discord_user_id      varchar(30),
  type                 varchar(15),
  amount               bigint,
  transaction_datetime timestamp default current_timestamp,
  given_by             varchar(30),
  primary key (transaction_id),
  foreign key (discord_user_id) references users (discord_user_id),
  foreign key (given_by) references users (discord_user_id)
);

create or replace view feli_point_balance as
select u.custom_nickname,
       sum(case
             when fpt.type = 'add'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 27 and
                    current_date - extract(dow from current_date)::integer - 22
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 27 and
                    current_date - extract(dow from current_date)::integer - 22
               then amount
             else 0 end) as week_minus_4,
       sum(case
             when fpt.type = 'add'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 21 and
                    current_date - extract(dow from current_date)::integer - 15
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 21 and
                    current_date - extract(dow from current_date)::integer - 15
               then amount
             else 0 end) as week_minus_3,
       sum(case
             when fpt.type = 'add'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 14 and
                    current_date - extract(dow from current_date)::integer - 8
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               and
                  fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 14 and
                    current_date - extract(dow from current_date)::integer - 8
               then amount
             else 0 end) as week_minus_2,
       sum(case
             when fpt.type = 'add'
               and fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 7 and
                    current_date - extract(dow from current_date)::integer - 1
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               and fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer - 7 and
                    current_date - extract(dow from current_date)::integer - 1
               then amount
             else 0 end) as week_minus_1,
       sum(case
             when fpt.type = 'add'
               and fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer and
                    current_date + 1
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               and fpt.transaction_datetime::date between current_date - extract(dow from current_date)::integer and
                    current_date + 1
               then amount
             else 0 end) as current_week,
       sum(case
             when fpt.type = 'add'
               then amount
             else 0 end) -
       sum(case
             when fpt.type = 'remove'
               then amount
             else 0 end) as total_balance
from feli_point_transactions fpt
       join users u
            on fpt.discord_user_id = u.discord_user_id
group by 1