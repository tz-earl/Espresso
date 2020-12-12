-- To run these sql statements from within psql, use \i restaurant-starter-rows.sql

-- This script resets the contents the restaurant table without having to
-- drop the table itself.

-- Delete all existing rows from the restaurant table
delete from restaurant;

-- Reset the id sequence to start at 1
alter sequence restaurant_id_seq restart with 1;

-- Insert five rows
insert into restaurant
    (name, street, suite, city, state, zip_code, phone_num, website, email, date_established, creator)
    values ('Herbal', '448 Larkin St', null, 'San Francisco', 'CA', '94102', '(415) 896-4839',
            'https://www.herbalrestaurant.com/', null, 'August 2020', 'barista-test-user@outlook.com');

insert into restaurant
    (name, street, suite, city, state, zip_code, phone_num, website, email, date_established, creator)
    values ('Chutney', '511 Jones St', null, 'San Francisco', 'CA', '94102', '(415) 931-5541',
            'https://www.chutneysanfrancisco.com/', null, 'Pre 2004', 'barista-test-user@outlook.com');

insert into restaurant
    (name, street, suite, city, state, zip_code, phone_num, website, email, date_established, creator)
    values ('Banana Island', '273 Lake Merced Blvd', null, 'Daly City', 'CA', '94015', '(650) 756-6868',
            'http://www.bananaislandrestaurant.com/', null, '2002', 'barista-test-user@outlook.com');

insert into restaurant
    (name, street, suite, city, state, zip_code, phone_num, website, email, date_established, creator)
    values ('Sorabol', '5959 Shellmound St', null, 'Emeryville', 'CA', '94608', '(510) 601-5959',
            'http://sorabolrestaurants.com/', null, null, 'barista-test-user@outlook.com');

insert into restaurant
    (name, street, suite, city, state, zip_code, phone_num, website, email, date_established, creator)
    values ('The Hummus & Pita Co.', '616 8th Ave', null, 'New York', 'NY', '10018', '(212) 510-7405',
            'https://www.hummusandpitas.com/', 'contact@HummusAndPitas.com', null, 'barista-test-user@outlook.com');

