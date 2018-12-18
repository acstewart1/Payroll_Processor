#!/usr/bin/python
#  Gateways Payroll Processor
#
#  Name:  Payroll_Processor.py
#
#  ***************************************************************************************  
#  Version                Details of Version       Date            Author
#  ***************************************************************************************
#  1.0                    Initial Version          02.12.2018      Craig Stewart-McDougall
#  ***************************************************************************************
#
#  Invocation:  Payroll_Processor.py  -n<<number of output batches>> -s<<input source filename>> -o<<Output Filename Pattern>> -e<<error file>> -l<<log filename>> 
#  
#       Where:  <<number of output batches>>       - These are the number of Batch files that payroll require for upload to chris21. The Batch number will be appended
#                                                    to each batch file name.
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
#               <<error file>>                     - This is the error file (including path) containing all the error records (if any) extracted from the input file.
#                                                    Example:  'e281118.log' (default location is the same directory as the inpout file)
#
#               <<log file>>                       - This is the log file (including path) detailing processing performed and messages (Informational, Warning and Error)
#                                                    Example:  'e281118.log' (default location is the same directory as the inpout file) 
# 
#        Comments:  The result of processing by this program is:
#                   * One or more batch files ready for upload into chris21 with all lines in error removed.  Each is uniquely suffixed to identify the batch number. 
#                   * An error file containing all the rejected (in error) records that require correction in Carelink before they can be processed into chris2. Note: If
#                     once or more fatal errors are fund for a given employee, then all their records on the file are written to this error file and removed from 
#                     processing until corrected.
#                   * A log file detailing all processing with messages (Informational messages, Warning Messages and Error Messages)

#
#  Create and open the default Log File Payroll.log ready to be written to
#
Log_File = open("Payroll.log","w+")

#
#  Read Input Arguments, Validate and set up Variables
#
import sys

#
#  Ensure that there are 5 Parameters input - if not report them to the default Payroll.error file 
#  and abend
#

if len(sys.argv) != 6:
    Number_Parameters_Input = len(sys.argv) - 1
    print ("Number of parameters entered was ",str(Number_Parameters_Input))
    if Number_Parameters_Input == 0:
       Log_File.write(str(datetime.now()),": ERROR - No parameters were entered")
       Log_File.write(str(datetime.now()),": ERROR - The Payroll Processor is abending")      
    else:
       Log_File.write(str(datetime.now()),": ERROR - Incorrect number of Parameters entered - ", str(Number_Parameters_Input), " parameters were entered.")
       counter = 2
       for counter in sys.argv:
           Log_File.write(str(datetime.now()),": ERROR - Parameter ",counter,"entered was: ",str(sys.argv[counter]))
    Log_File.write(str(datetime.now()),": ERROR - The Payroll Processor is abending"))
    import sys
    sys.exit()

#  Validate the first parameter
   Parameter_1 = sys.argv(2):
   Parameter_1_switch = Parameter_1[:2]
   if Parameter_1_switch != "-n":
      Log_File.write(str(datetime.now()),": ERROR - First Parameter for number of batches requires -n switch. Parameter entered was: ",str(sys.argv[1]))
      Log_File.write(str(datetime.now()),": ERROR - The Payroll Processor is abending")
      import sys
      sys.exit()
   else:
      print ("end for now")
           
   

# 
#     
#
#  Create and open the Log File ready to be written to
#


#
#  Create Unsplit Payroll File with no Errors - write lines for employees with errors to error file
#  Write informational, Warning and Error messages to the log file
#

#
#  Split the Unsplit Payroll file with no errors into the requested number of batches
#

#
#  Conclude the program with relevent messages
#

print("Program concluding")
