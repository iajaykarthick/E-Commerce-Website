### Triggers 
show triggers;
# Trigger 1
# Trigger for checking user does not enter more than 10 quantity.

DROP TRIGGER IF EXISTS check_quantity_max_limit;
delimiter $$

CREATE TRIGGER  check_quantity_max_limit  BEFORE INSERT ON CART

FOR EACH ROW

BEGIN

IF NEW.quantity >10 THEN

SIGNAL SQLSTATE '45000'

SET MESSAGE_TEXT = 'ERROR: Max BookQuantity MUST BE 10!';

END IF;

END $$

delimiter ;


/*
Testing trigger 
insert into cart values(1,'0061030147',15 );
*/

DROP TRIGGER IF EXISTS after_cart_updates;
DELIMITER $$
CREATE TRIGGER after_cart_updates
AFTER INSERT
ON order_items  FOR EACH ROW
BEGIN
    DECLARE new_order_id int;
    DECLARE isbn varchar(10);
    DECLARE quantity int;
    set @new_order_id := NEW.Order_ID;
    set @isbn := NEW.ISBN;
    set @nquantity := NEW.Number_Of_Copies;
    set @store_id := (select Store_ID from ORDERS where Order_ID=@new_order_id);
    update STORE_COPIES set Number_Of_Copies= (Number_Of_Copies - @nquantity)
    where store_id = @store_id;
    
END$$

DELIMITER ;

