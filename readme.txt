Planned functionality

General:
    Refractor out_compstats.py
    
Computer Status:
    
    
Changlog.

1.00     : Define namedtuple for ComputerStatus data (CompStats)
                Fields in namedtuple are:
                    STR     60      ComputerName
                    STR     250     ComputerDescription
                    STR     60      ComputerOS
                    STR     60      Location
                    STR     30      IPInternal
                    STR     30      IPExternal
                    DateTime        LastOnlineDateTime
                    INT             UpdateIntervalSec
                    INT             CPUUtilization
                    INT             DiskUtilization
            Write compstats.csv file with test data.
            Read ComputerStatus from csv file and print to terminal
            Make output to terminal use urwid.
            Add keyboard handling for q to quit
            Write eventlines.csv file with test data
            Repeated reading of CompStats, and output
            Add Header to output
            Add console size checking to output
            Add ircchat lines to output 
                Get data from .weechat/logs/irc.labitat.\#labitat.weechatlog
                Define namedtuple for Chat Lines data (ChatLines)
                    Field in namedtuple are:
                        DateTime        DateTime
                        STR             UserName
                        STR             ChatText
            Add Event lines to output
                Get data from csv file
                Define namedtuple for EventLines data (EventLines)
                    Field in namedtuple are:
                        DateTime        DateTime
                        STR             SenderName
                        STR             EventText
            Refractor method printCompStats - formatListToOutput
                This method must be moved to a library, so it should be able to handle
                any list with output records, and format them correctly for output.
        
                Function parameters
                    List of lines to work on                                        (inputList)
                    Array with column headers                                       (columnHeaders[])
                    Array with column width, 0 = Needs to be calculated             (columnWidth[])
                Function does this
                    Calculate column width                                          (columnWidth[x])
                    Calculate output lines                                          (outputLineNums)
                    Set Header for output                                           (outputList[0])
                    Get last (outputLineNums) lines from inputList                  (inputList)
                    Fix lenghts of fields in inputList, wordwrap field x            (inputList)
                    Get last (outputLineNums) lines from inputList                  (inputList)
                    Remove top lines from inputList that has no data in column x
                Function returns
                    outputList
            Change source of data from csv files to SQL.
                Changed for out_compstats.py /MySQL Db firemane4:computerStatus/ComputerStatus
                Changed for out_eventlines.py /MySQL Db firemane4:webLogSql/WebLogTable
            Compress ComputerStatus table admin_compressComputerStatus.py                
            
THANKS TO : 
