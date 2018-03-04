Planned functionality

General:

Computer Status:
	Repeated reading of CompStats, and output
	Add ircchat lines to output
		Get data from .weechat/logs/irc.labitat.\#labitat.weechatlog
	Add Event lines to output
		Get data from csv file
	Change source of data from csv files to SQL.
		Find out what SQL database to use for data.
		Test Create database
		Test Write to SQL
		Test Read from SQL

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
