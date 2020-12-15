-- To run these sql statements from within psql, use \i restaurant-starter-rows.sql

-- This script resets the contents of the restaurant and review tables
-- without having to drop the tables themselves.

-- Delete all the reviews first, then all the restaurants because of the dependencies,
-- i.e. the foreign key column of the review table refers to rows in the restaurant table.
-- So attempting to first delete the restaurant rows will trigger errors.

delete from review;
delete from restaurant;

-- Reset the restaurant id sequence to start at 1
alter sequence restaurant_id_seq restart with 1;

-- Insert rows into the restaurant table
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

-- Reset the review id sequence to start at 1
alter sequence review_id_seq restart with 1;

-- Insert rows into the review table
insert into review
    (author, date, rating, comment, restaurant_id)
    values ('customer-test-user@gmail.com', '2020-12-14', 4,
            'Pretty decent espresso and outstanding pastries', 2);

insert into review
    (author, date, rating, comment, restaurant_id)
    values ('customer-test-user@gmail.com', '2020-12-14', 1,
            'espresso was way too weak for my tastes, like a watered down Americano', 5);
