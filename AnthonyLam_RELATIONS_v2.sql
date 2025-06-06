CREATE TABLE Business (
    business_id VARCHAR(30),
    name VARCHAR(100),
    city CHAR(30),
    state CHAR(2),
    zipcode INTEGER,
    address VARCHAR(100),
    review_count INTEGER,
    num_checkins INTEGER,
    reviewRating FLOAT,
    stars FLOAT,
    PRIMARY KEY (business_id),
    FOREIGN KEY (zipcode) REFERENCES zipcodeData(zipcode)
)

CREATE TABLE Reviews (
    review_id VARCHAR(30),
    review_stars FLOAT,
    date DATE,
    text VARCHAR(1000),
    useful_vote INTEGER,
    funny_vote INTEGER,
    cool_vote INTEGER,
    business_id VARCHAR(30) NOT NULL,
    PRIMARY KEY (review_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
)

CREATE TABLE Checkins (
    day CHAR(30),
    time VARCHAR(30),
    count INTEGER,
    business_id VARCHAR(30),
    PRIMARY KEY (business_id, day, time),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
)

CREATE TABLE Attributes (
    attr_name VARCHAR(30),
    value BOOLEAN,
    business_id VARCHAR(30),
    PRIMARY KEY (business_id, attr_name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
)

CREATE TABLE Categories (
    category_name VARCHAR(100),
    business_id VARCHAR(30),
    PRIMARY KEY (business_id, category_name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
)

CREATE TABLE zipcodeData (
    zipcode INTEGER,
    medianIncome INTEGER,
    meanIncome INTEGER,
    population INTEGER,
    PRIMARY KEY (zipcode)
)