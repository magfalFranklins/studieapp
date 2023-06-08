CREATE_USER_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS {table} 
    (id SERIAL, user_name TEXT PRIMARY KEY, password TEXT, active_pw TEXT, alias TEXT, school TEXT, program TEXT, birth TIMESTAMP, points INTEGER, achievments TEXT [], created TIMESTAMP);
    """
)

CREATE_TODO_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS {table} 
    (id SERIAL, user_name TEXT, todo TEXT, type_of_excersice TEXT, priority INTEGER, deadline TIMESTAMP, est_time INTEGER, calender BOOL, created TIMESTAMP, 
    FOREIGN KEY(user_name) 
    REFERENCES user_table(user_name) 
    ON DELETE CASCADE);
    """
)

CREATE_STUDY_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS {table} 
    (id SERIAL, user_name TEXT, subject TEXT, study_time INTEGER, memo_text TEXT, effectivity INTEGER, created TIMESTAMP, 
    FOREIGN KEY(user_name) 
    REFERENCES user_table(user_name) 
    ON DELETE CASCADE);
    """
)

DROP_TABLE = "DROP TABLE IF EXISTS {table}"

INSERT_USER = (
    """
    INSERT INTO user_table 
    (user_name, password, active_pw, alias, school, program, birth, points, achievments, created) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    RETURNING id
    """
)

INSERT_TODO = (
    """
    INSERT INTO todo_table 
    (user_name, todo, type_of_excersice, priority, deadline, est_time, calender, created) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
    RETURNING (user_name, todo)
    """
)

INSERT_STUDY = (
    """
    INSERT INTO study_table 
    (user_name, subject, study_time, memo_text, effectivity, created) 
    VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING user_name
    """
)

GET_ALL = "SELECT * FROM {table} WHERE {variable} = (%s)"

GET_VALUE = "SELECT {data} FROM {table} WHERE {variable} = (%s)"

UPDATE_VALUE = (
    """
    UPDATE {table} 
    SET {variable} = (%s) 
    WHERE user_name = (%s) 
    RETURNING * 
    """
)

DELETE_VALUE = "DELETE FROM {table} WHERE id = (%s)"