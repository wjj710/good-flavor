/*
myuser表的触发器
*/
CREATE OR REPLACE FUNCTION trg_myuser() RETURNS trigger AS $trg_myuser$
    BEGIN
        DELETE FROM myuser
        WHERE "id"= NEW."id";
        return NEW;
    END;
$trg_myuser$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER myuserBeforeInsertOrUpdate
BEFORE INSERT ON myuser
FOR EACH ROW 
EXECUTE FUNCTION trg_myuser();

/*
search表的触发器
*/
CREATE OR REPLACE FUNCTION trg_search() RETURNS trigger AS $trg_search$
    BEGIN
        DELETE FROM search
        WHERE "id"= NEW."id";
        return NEW;
    END;
$trg_search$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER searchBeforeInsertOrUpdate
BEFORE INSERT ON search
FOR EACH ROW 
EXECUTE FUNCTION trg_search();

/*
taste表的触发器
*/
CREATE OR REPLACE FUNCTION trg_taste() RETURNS trigger AS $trg_taste$
    BEGIN
        DELETE FROM taste
        WHERE "id"= NEW."id";
        return NEW;
    END;
$trg_taste$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tasteBeforeInsertOrUpdate
BEFORE INSERT ON taste
FOR EACH ROW 
EXECUTE FUNCTION trg_taste();


