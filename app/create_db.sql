CREATE TABLE states (
        id INTEGER NOT NULL, 
        name VARCHAR(100), 
        PRIMARY KEY (id)
);
CREATE TABLE businesses (
        id INTEGER NOT NULL, 
        restaurant VARCHAR(100), 
        sales FLOAT, 
        city VARCHAR(100), 
        yoy_sales VARCHAR(100), 
        state_id INTEGER, 
        detail VARCHAR(100), 
        PRIMARY KEY (id), 
        FOREIGN KEY(state_id) REFERENCES states (id)
);
CREATE TABLE crimes_vs_person (
        id INTEGER NOT NULL, 
        assault_offenses INTEGER, 
        homicide_offenses INTEGER, 
        human_trafficking INTEGER, 
        kidnapping_abduction INTEGER, 
        sex_offenses INTEGER, 
        state_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(state_id) REFERENCES states (id)
);
CREATE TABLE crimes_vs_property (
        id INTEGER NOT NULL, 
        number_of_participating_agencies INTEGER, 
        population_covered INTEGER, 
        arson INTEGER, 
        bribery INTEGER, 
        burglary_breaking_entering INTEGER, 
        counterfeiting_forgery INTEGER, 
        destruction_damage_vandalism INTEGER, 
        embezzlement INTEGER, 
        extortion_blackmail INTEGER, 
        fraud_offenses INTEGER, 
        larceny_theft_offenses INTEGER, 
        motor_vehicle_theft INTEGER, 
        robbery INTEGER, 
        stolen_property_offenses INTEGER, 
        state_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(state_id) REFERENCES states (id)
);
CREATE TABLE crimes_vs_society (
        id INTEGER NOT NULL, 
        animal_cruelty INTEGER, 
        drug_narcotic_offenses INTEGER, 
        gambling_offenses INTEGER, 
        pornography_obscene_material INTEGER, 
        prostitution_offenses INTEGER, 
        weapon_law_violations INTEGER, 
        state_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(state_id) REFERENCES states (id)
);

