import argparse
import os
import sys
import subprocess as sp
import filecmp

defaultStuDirPath = "./students"
defaultIntermediatePath = "lab1"
defaultWorkName = "LogicGate.circ"
defaultJarPath = "../logisim-generic-2.7.1.jar"
defaultCheckerPath = "./main-tester.circ"
defaultKeyPath = "./correct-circuit.circ"
defaultOutputPath = "./stuOut"
defaultReportPath = "./report.txt"
correctOutputFileName = "CorrectOutput.txt"

error_count = 0
error_limit = 5

parser = argparse.ArgumentParser(description='Logisim Grading Script')
parser.add_argument('-sd', '--studir', default=defaultStuDirPath, metavar='studir', help=f'Path to directory containing the student folders (default="{defaultStuDirPath}")', )
parser.add_argument('-ip', '--interpath', default='lab1', help=f'Intermediate path from student folders directory to directory containing student work (default="{defaultIntermediatePath}")', metavar='--interpath')
parser.add_argument('-wn', '--workname', default=defaultWorkName, help=f'File name of student work (default="{defaultWorkName}")', metavar="--workname")
parser.add_argument('-jp', '--jarpath', default=defaultJarPath, help=f'Path to the Logisim jar file (default="{defaultJarPath}")', metavar='--jarpath')
parser.add_argument('-cp', '--checkerpath', default=defaultCheckerPath, help=f'Path to the checker circuit file (default="{defaultCheckerPath}")', metavar='--checkerpath')
parser.add_argument('-kp', '--keypath', default=defaultKeyPath, help=f'Path to the correct (sub)circuit loaded in the checker circuit file (default="{defaultKeyPath}")', metavar="--keypath")
parser.add_argument('-od', '--outputdir', default=defaultOutputPath, help=f'Directory path in which to save student output (default="{defaultOutputPath}")', metavar="--outputdir")
parser.add_argument('-rp', '--reportpath', default=defaultReportPath, help=f'Path to the report file to be written, doesn\'t have to exist (default="{defaultReportPath}")', metavar='--reportpath')
args = parser.parse_args()

def cleanString(string):
    if isinstance(string, bytes):
        string = string.decode('utf-8')
    while '\r' in string:
        index = string.index('\r')
        string = string[0:index] + string[index+1:]
    return string

def checkValidPath(path):
    if not os.path.isdir(path):
        return False
    return True

def checkValidFile(path):
    if not os.path.isfile(path):
        return False
    return True

def exitWithError(message):
    print(message)
    print("Exiting...")
    sys.exit(1)

if not args.studir:
    exitWithError("The -sd or --studir argument cannot be empty!\nPlease enter the directory path containing student folders using -sd or --studir argument.")
else:
    path_studir = os.path.abspath(args.studir)
    if not checkValidPath(path_studir):
        exitWithError(f'The following path is not a directory!:\n\t"{path_studir}"\nPlease enter the correct directory path containing student folders using -sd or --studir argument.')

if not args.jarpath:
    exitWithError("The -jp or --jarpath argument cannot be empty!\nPlease enter the path for the Logisim jar file.")
else:
    path_jar = os.path.abspath(args.jarpath)
    if not checkValidFile(path_jar):
        exitWithError(f'Cannot find a file at "{path_jar}".\nPlease check the jarpath argument!')

stuFileName = args.workname
if not stuFileName:
    exitWithError(f'The -wn or --workname argument cannot be empty!\nPlease enter the name of the circuit file to grade for -wn or -workname.')
elif stuFileName[-5:] != '.circ':
    stuFileName += '.circ'

if not args.checkerpath:
    exitWithError(f'The -cp or --checkerpath argument cannot be empty!\nPlease enter the path to the checker circuit file.')
else:
    path_checker = os.path.abspath(args.checkerpath)
    if path_checker[-5:] != '.circ':
        path_checker += '.circ'
    if not checkValidFile(path_checker):
        exitWithError(f'The file cannot be found:\n\t{path_checker}\nPlease check the checkerpath argument.')

if not args.keypath:
    exitWithError(f'The -kp or --keypath argument cannot be empty!\nPlease enter the name of the loaded library in the checker file.')
else:
    path_key = os.path.abspath(args.keypath)
    if path_key[-5:] != ".circ":
        path_key += '.circ'
    if not checkValidFile(path_key):
        exitWithError(f'The file cannot be found:\n\t{path_key}\nPlease give the correct path to the loaded library file for keypath argument.')

if not args.outputdir:
    exitWithError('The -od or --outputdir argument cannot be empty!\nPlease enter the path to the directory to save student output in.')
else:
    path_output = os.path.abspath(args.outputdir)
    if not checkValidPath(path_output):
        exitWithError(f'Cannot find directory {path_output}\nPlease check the -od or --output dir!')

if not args.reportpath:
    exitWithError('The -rp or --reportpath argument cannot be empty!\nPlease enter the path to file to be written.')
else:
    path_report = os.path.abspath(args.reportpath)
    # check if the report file can be generated
    try:
        with open(path_report, 'w+') as report:
            pass
    except Exception:
        exitWithError(f'Could not make a file at {path_report}\nPlease make sure you have write permission in specified directory')

# generate the correct output
run_command = f'java -jar "{path_jar}" "{path_checker}" -tty table'
process = sp.Popen(run_command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
try:
    (output, error) = process.communicate(timeout=30)
    if process.poll() != 0:
        exitWithError("Error occurred while generating the correct output.\nThe error was " + error.decode('utf-8'))
    else:
        print(f"Success! The output was \n{output.decode('utf-8')}")
        correctOutputFile = os.path.join(path_output, correctOutputFileName)
        with open(correctOutputFile, 'w+') as correctOut:
            correctOut.write(cleanString(output))
except sp.TimeoutExpired:
    exitWithError(f'Timed out while generating the correct output\nThe command used was "{run_command}"')

# check the students
for student in os.listdir(path_studir):
    print(f"\nWorking on student: {student}")
    
    stuPath = os.path.join(path_studir, student, args.interpath)
    if not checkValidPath(stuPath):
        print(f'The following path is not a directory!: "{stuPath}"\nMight want to check the --interpath argument.\nSkipping the student...')
        continue
    
    if not checkValidFile( os.path.join(stuPath, stuFileName) ):
        print(f'There is no file named "{stuFileName}" in "{stuPath}".\nCheck the --interpath and --workname arguments!\nSkipping the student...')
        continue

    # get the output of the student work
    run_command = f'java -jar "{path_jar}" "{path_checker}" -tty table -sub {path_key} {stuFileName}'
    # print(f'run command is {run_command}')
    process = sp.Popen(run_command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, cwd=stuPath)
    try:
        (output, error) = process.communicate(timeout=30)
        if process.poll() != 0:
            error_count += 1
            output = error.decode('utf-8')
        else:
            output = output.decode('utf-8')
    except sp.TimeoutExpired:
        error_count += 1
        output = "Timed out while running"

    # save output
    workname = stuFileName[:-5]
    outputFile = os.path.join(path_output, workname + '_' + student + '.txt')
    with open(outputFile, 'w+') as student_out:
        student_out.write(cleanString(output))

    # compare output with correct output
    if process.poll() == 0:
        if filecmp.cmp(correctOutputFile, outputFile, shallow=False):
            resultMessage = f"{student}:\tMatches the correct answer!\n"
        else:
            resultMessage = f"{student}:\tDoes not match the correct answer :(\n"
        print(resultMessage)
        with open(path_report, 'a+') as report:
            report.write(resultMessage)

    # quit script if there are too many errors in running the script
    if error_count >= error_limit:
        exitWithError("Error count reached.")
    