Planned functionality

General:

Computer Status:
	Repeated reading of CompStats, and output
	

Changlog.

1.00     : Define namedtuple for ComputerStatus data (CompStats)
                Fields in namedtuple are:
                    STR         ComputerName
                    STR         ComputerDescription
                    STR         ComputerOS
                    STR         Location
                    STR         IPInternal
                    STR         IPExternal
                    DateTime    LastOnlineDateTime
                    INT         UpdateIntervalSec
                    INT         CPUUtilization
                    INT         DiskUtilization
            Write compstats.csv file with test data.
            Read ComputerStatus from csv file and print to terminal
			Make output to terminal use urwid.
			Add keyboard handling for q to quit

			
THANKS TO : 
