#!/usr/bin/python
#  Gateways Payroll Processor
#
#  Name:  Payroll_Processor.py
#
#  ***************************************************************************************  
#  Version                Details of Version       Date            Author
#  ***************************************************************************************
#  1.0                    Initial Version          27.12.2018      Craig Stewart-McDougall
#  ***************************************************************************************
#
#  Invocation:  Payroll_Processor.py  -n<<number of output batches>> -s<<input source filename>> -o<<Output Filename Pattern>>
#  
#       Where:  <<number of output batches>>       - These are the number of Batch files that payroll require for upload to chris21. The Batch number will be appended
#                                                    to each batch file name. The allowable range is 1 - 100.
#                                                    Example:  -n3 would result in batch1.DAT, batch2.DAT, batch3.DAT (assuming that the value for <<output filename
#                                                              pattern was 'batch')
#
#               <<input source filename>>          - This is the input to the program being the Carelink Export Payroll File (including path)
#                                                    Example:   F:\CARELINK\PRODUCTION\payroll_exports\unprocessed\Payroll.txt
#
#               <<Output Batch Filename Pattern>>  - This is the batch file naming pattern.
#                                                    Examples: 'batch' would result in batch1.DAT, batch2.DAT, batch3.DAT (assuming that the value for <<number of 
#                                                               output batches>> was 3)
#                                                              'stewie' would result in stewie1.DAT, stewie2.DAT, stewie3.DAT (assuming that the value for <<number of output 
#                                                               batches>> was 3)
#                                                              'B281118' would result in B2811181.DAT, B2811182.DAT, B2811183.DAT (assuming that the value for <<number of
#                                                               output batches>> was 3)  
#
#        Comments:  The result of processing by this program is:
#                   * One or more batch files ready for upload into chris21 with all lines in error removed.  Each is uniquely suffixed to identify the batch number. 
#                   * An error file containing all the rejected (in error) records that require correction in Carelink before they can be processed into chris2. Note: If
#                     once or more fatal errors are fund for a given employee, then all their records on the file are written to this error file and removed from 
#                     processing until corrected.
#                   * A log file detailing all processing with messages (Informational messages, Warning Messages and Error Messages) is written in the current
#                     directory named: Payroll.log. This file is appended to to each run of this payroll processor.
#                   * A file named Error.DAT is written contained batches of records for any staff member's data that was found to have one or more errors in the input file.
#                     This ensures that staff data with issues is segregated away from the other data that can be proceed to be processed into chris21.
#
#  Create and open input and output files
#
Log_File = open("Payroll.log","w+")

#
#  Import function libraries
#
import sys
import os
import datetime
import logging
import os.path
import re

def write_to_log_and_console(writeable_line):
       line_to_write = str(datetime.datetime.now()) + writeable_line + "\r\n"
       Log_File.write(line_to_write)
       print(line_to_write)

#
#  Set up initial values for the program
#
minimum_number_of_batches = 1
maximum_number_of_batches = 100

#
#  Ensure that there are 3 Parameters input - if not report them to the default Payroll.error file 
#  and abend
#

writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR IS STARTING  ***********************"
write_to_log_and_console(writeable_line)

if len(sys.argv) != 4:
    Number_Parameters_Input = len(sys.argv) - 1
    if Number_Parameters_Input == 0:
       writeable_line = ": ERROR - No parameters were entered"
       write_to_log_and_console(writeable_line)
    else:
       writeable_line = ": ERROR - Incorrect number of Parameters entered - " + str(Number_Parameters_Input) + " parameters were entered."
       write_to_log_and_console(writeable_line)
       writeable_line = ": ERROR - the parameters that were entered are - " + str(sys.argv[1:])
       write_to_log_and_console(writeable_line)
    writeable_line = ": ERROR - The Payroll Processor is abending"
    write_to_log_and_console(writeable_line)
    writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
    write_to_log_and_console(writeable_line)
    quit()

#  Validate the first parameter (number of batches) 
Parameter_1 = sys.argv[1]
Parameter_1_switch = Parameter_1[:2]
if Parameter_1_switch != "-n":
   writeable_line = ": ERROR - First Parameter for number of batches requires -n switch. Parameter entered was: " + str(sys.argv[1])
   write_to_log_and_console(writeable_line)
   writeable_line = ": ERROR - The Payroll Processor is abending"
   write_to_log_and_console(writeable_line)
   writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
   write_to_log_and_console(writeable_line)
   quit()
else:
   Parameter_1_value = Parameter_1[2:]
   Parameter_1_value = int(Parameter_1_value)
   if Parameter_1_value >= minimum_number_of_batches and Parameter_1_value <= maximum_number_of_batches:
       writeable_line = ": INFO  - Number of batches selected is " + str(Parameter_1_value)
       write_to_log_and_console(writeable_line)
   else:
       writeable_line = ": ERROR - Number of batches selected is " + str(Parameter_1_value) + " and is invalid"
       write_to_log_and_console(writeable_line)
       writeable_line = ": ERROR - The number of batches selected must be in the range " + str(minimum_number_of_batches) + " to " + str(maximum_number_of_batches)
       write_to_log_and_console(writeable_line)
       writeable_line = ": ERROR - The Payroll Processor is abending"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - The Payroll Processor has now ended"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
       write_to_log_and_console(writeable_line)
       quit()
           
#  Validate the second parameter (input source file)
Parameter_2 = sys.argv[2]
Parameter_2_switch = Parameter_2[:2]
if Parameter_2_switch != "-s":
   writeable_line = ": ERROR - Second Parameter for input file name requires -s switch. Parameter entered was: " + str(sys.argv[2])
   write_to_log_and_console(writeable_line)
   writeable_line = ": ERROR - The Payroll Processor is abending"
   write_to_log_and_console(writeable_line)
   writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
   write_to_log_and_console(writeable_line)
   quit()
else:
   Parameter_2_value = Parameter_2[2:]
#
#  Need to test if any filename was supplied........
#    
   if Parameter_2_value is None:
       writeable_line = ": ERROR - No input source file was specified for the -s switch"
       write_to_log_and_console(writeable_line)
       writeable_line = ": ERROR - The Payroll Processor is abending"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - The Payroll Processor has now ended"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
       write_to_log_and_console(writeable_line)
       quit()
   else:
#  Test if the file name supplied has the correct extension of .DAT   
       if Parameter_2_value.endswith('.DAT'):
          writeable_line = ": INFO  - The source input file has been supplied with correct extension of .DAT"
          write_to_log_and_console(writeable_line)
       else:
          writeable_line = ": ERROR - The source input file name supplied does not have an extension of .DAT and is invalid"
          write_to_log_and_console(writeable_line)
          writeable_line = ": ERROR - The source input file name supplied was: " + Parameter_2_value
          write_to_log_and_console(writeable_line)
          writeable_line = ": ERROR - The Payroll Processor is abending"
          write_to_log_and_console(writeable_line)
          writeable_line = ": INFO  - The Payroll Processor has now ended"
          write_to_log_and_console(writeable_line)
          writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
          write_to_log_and_console(writeable_line)
          quit()
#  Need to test if the source filename actually exists in the current directory

current_working_directory = os.getcwd()
path = os.path.join(current_working_directory, Parameter_2_value)
if os.path.exists(path):
      writeable_line = ": INFO  - The source input file " + Parameter_2_value + " has been confirmed as existing"
      write_to_log_and_console(writeable_line)
else:
      writeable_line = ": ERROR - The source input file " + Parameter_2_value + " does not exist"
      write_to_log_and_console(writeable_line)             
      writeable_line = ": ERROR - The Payroll Processor is abending"
      write_to_log_and_console(writeable_line)
      writeable_line = ": INFO  - The Payroll Processor has now ended"
      write_to_log_and_console(writeable_line)
      writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
      write_to_log_and_console(writeable_line)
      quit()

#  Need to test if the file has any data in it
if os.stat(Parameter_2_value).st_size == 0:
   writeable_line = ": ERROR - The source input file " + Parameter_2_value + " is empty"
   write_to_log_and_console(writeable_line)             
   writeable_line = ": ERROR - The Payroll Processor is abending"
   write_to_log_and_console(writeable_line)
   writeable_line = ": INFO  - The Payroll Processor has now ended"
   write_to_log_and_console(writeable_line)
   writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
   write_to_log_and_console(writeable_line)
   quit()        

#  Validate the third parameter (output file pattern)
Parameter_3 = sys.argv[3]
Parameter_3_switch = Parameter_3[:2]
if Parameter_3_switch != "-o":
   writeable_line = ": ERROR - Third Parameter for output file pattern requires -o switch. Parameter entered was: " + str(sys.argv[2])
   write_to_log_and_console(writeable_line)
   writeable_line = ": ERROR - The Payroll Processor is abending"
   write_to_log_and_console(writeable_line)
   writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
   write_to_log_and_console(writeable_line)
   quit()
else:
   Parameter_3_value = Parameter_3[2:]
#
#  Need to test if any filename was supplied........
#    
   if Parameter_3_value is None:
       writeable_line = ": ERROR - No input source file was specified for the -o switch"
       write_to_log_and_console(writeable_line)
       writeable_line = ": ERROR - The Payroll Processor is abending"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - The Payroll Processor has now ended"
       write_to_log_and_console(writeable_line)
       writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
       write_to_log_and_console(writeable_line)
       quit()
   else:
#  Test if the file name pattern supplied has any illegal characters in it
      if re.match("^[A-Za-z0-9_-]*$", Parameter_3_value):
         writeable_line = ": INFO  - The output filename pattern is fine and has been supplied without any illegal characters"
         write_to_log_and_console(writeable_line)
      else:
         writeable_line = ": ERROR - The output filename pattern contains illegal characters and is invalid. Only alphanumerics are allowed"
         write_to_log_and_console(writeable_line)
         writeable_line = ": ERROR - The output filename pattern supplied was: " + Parameter_3_value
         write_to_log_and_console(writeable_line)
         writeable_line = ": ERROR - The Payroll Processor is abending"
         write_to_log_and_console(writeable_line)
         writeable_line = ": INFO  - The Payroll Processor has now ended"
         write_to_log_and_console(writeable_line)
         writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
         write_to_log_and_console(writeable_line)
         quit()

writeable_line = ": INFO  - All input parameters have been validated and are correct"
write_to_log_and_console(writeable_line)
writeable_line = ": INFO  - Parameters entered are:"
write_to_log_and_console(writeable_line)
writeable_line = ": INFO  -     Number of batches to split data into: " + str(Parameter_1_value)
write_to_log_and_console(writeable_line)
writeable_line = ": INFO  -     Input source file name is: " + Parameter_2_value
write_to_log_and_console(writeable_line)
writeable_line = ": INFO  -     Output finename pattern is: " + Parameter_3_value
write_to_log_and_console(writeable_line)
#
#  Create Unsplit Payroll File with no Errors - write lines for employees with errors to error file
#  Write informational, Warning and Error messages to the log file
#
#
#  Open the input file ready to read from
#
#  Record_Number = 0
#  Number_of_Records_Missing_Employee_Number = 0
#  Readnext_Record:
#       Record_Number = Record_Number + 1
#       Read Record
#       If Employee_Number is blank
#          Turn on Fatal_Error Switch
#          Write Error message to Logfile with Record_Number
#          If No more Records:
#             Write Error Message to Logfile indicating number of records with no employee number
#             Write Error Message to Logfile advising that processing is terminated due to fatal errors and requires correction
#             quit()
#          Else
#             Goto Readnext_Record
#  Fatal_Ending:
#       If Fatal_Error swith is true:
#             Write Error Message to Logfile indicating number of records with no employee number
#             Write Error Message to Logfile advising that processing is terminated due to fatal errors and requires correction
#             quit()
#           
#             
#      
#
#  Split the Unsplit Payroll file with no errors into the requested number of batches
#

#
#  Conclude the program with relevent messages
#
writeable_line = ": INFO  - *************************  PAYROLL PROCESSOR HAS ENDED  ***********************"
write_to_log_and_console(writeable_line)
