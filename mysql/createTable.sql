/*************************************
*Author..: Rudi Hansen <rsh@obtain.dk>
*Purpose.: Create tables for computerStatus
*Used by.: Admins
*Version.: 1.00
**************************************/
USE computerStatus;

/*DROP TABLE ComputerStatus*/
CREATE TABLE ComputerStatus ( LogDate               DATETIME,
                              ComputerName          VARCHAR(60),
                              ComputerDescription   VARCHAR(250),
                              ComputerOS            VARCHAR(60),
                              Location              VARCHAR(60),
                              IPInternal            VARCHAR(30),
                              IPExternal            VARCHAR(30),
                              UpdateIntervalSec     INT,
                              CPUUtilization        INT,
                              DiskUtilization       INT,
                              PRIMARY KEY ( ComputerName,LogDate ));

