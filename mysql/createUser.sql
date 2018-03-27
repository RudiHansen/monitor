/*************************************
*Author..: Rudi Hansen <rsh@obtain.dk>
*Purpose.: Create Database for computerStatus
*Used by.: Admins
*Version.: 1.00
**************************************/
DROP USER 'compstatus';
CREATE USER 'compstatus' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON computerStatus.* TO 'compstatus';

FLUSH PRIVILEGES;
