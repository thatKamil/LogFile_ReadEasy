######################################################################################################################
# Initialisation
######################################################################################################################
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

parameters_dict = {}  # New dictionary holding relevant data from log file.

parameters_list = ['Filter', 'Frame Averaging', 'Camera binning', 'Source Voltage (kV)',
                   'Source Current (uA)', 'Exposure (ms)', 'Rotation Step (deg)', 'Scanning position',
                   'Image Pixel Size (um)', 'Use 360 Rotation', 'Random Movement', 'Scan duration',
                   'Minimum for CS to Image Conversion', 'Maximum for CS to Image Conversion',
                   'Smoothing', 'Ring Artifact Correction', 'Beam Hardening Correction (%)']

def resource_path(relative_path):
    """ Get absolute path to resource """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Prepares information for the 'About' button.
aboutText = []
aboutPath = resource_path("about")
aboutFile = open(aboutPath, "r", encoding="utf-8")
for line in aboutFile.readlines():
    aboutText.append(line)
informationAbout = ''.join(aboutText)

# Prepares information for the 'Use Guide' button.
useText = []
usePath = resource_path("useGuide")
useFile = open(usePath, "r", encoding="utf-8")
for line in useFile.readlines():
    useText.append(line)
informationUseGuide = ''.join(useText)


######################################################################################################################
# GUI Interface Setup
######################################################################################################################

# Main windows setup
mainWindow = Tk()  # Links main window to the interpreter
mainWindow.title("LogFile_ReadEasy by Kamil_Sokolowski")
mainWindow.geometry("392x357+300+200")  # Window size and initial position
mainWindow['bg'] = 'gray98'  # Background colour

# Main text area
textArea = Text(mainWindow, width=46, height=17, borderwidth=2, bg='old lace')
textArea.place(x=10, y=50)
textArea.insert(END, "\n\n\t\t\t\n")
asciiPath = resource_path("asciiBook")
asciiBook = open(asciiPath, 'r')
asciiBookOutput = asciiBook.read()
textArea.insert(END, asciiBookOutput)

# Log file path output text area
logPath = Text(mainWindow, width=39, height=1, bg='old lace')
logPath.place(x=68, y=332)

# Labels
Label(mainWindow, text="Log Path:", bg='gray98').place(x=8, y=330)
Label(mainWindow, text="Ready to read easy?", bg='gray98', font='Helvetica').place(x=170, y=10)


######################################################################################################################
# Functions
######################################################################################################################

def openLogFileAndProcess():
    '''Main program that runs with an open GUI'''

    textArea.delete("1.0", "end")
    logPath.delete("1.0", "end")

    # Select log file
    logFilePath = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/",
        title="Open Log file",
        filetypes=(("Log Files", "*.log"),)
    )

    logPath.insert(END, logFilePath)  # Writes path address to text box in GUI

    # Opens and parses the data from log file
    with open(logFilePath, 'r') as fin:
        for line in fin:
            for i in parameters_list:
                if i in line:
                    equalSignPosition = line.find('=')
                    parameters_dict[line[:equalSignPosition]] = (line[equalSignPosition + 1:]).strip()

    # Outputs results in GUI text box
    for key, value in parameters_dict.items():
        for parameter in parameters_list:
            if parameter == key:
                if len(key) > 20:  # Longer strings are never neccesary for ID of parameter.
                    textArea.insert(END, (key[:15]) + "\t\t\t\t" + value + "\n")
                else:
                    textArea.insert(END, key + "\t\t\t\t" + value + "\n")

def dragDropOpen():
    """Main program that runs when a log file is drag and dropped onto the exe"""
    textArea.delete("1.0", "end")
    logPath.delete("1.0", "end")

    logPath.insert(END, importedLogFile)  # Writes path address to text box in GUI

    # Opens and parses the data from log file
    with open(importedLogFile, 'r') as textInput:
        for line in textInput:
            for i in parameters_list:
                if i in line:
                    position = line.find('=')
                    parameters_dict[line[:position]] = (line[position + 1:]).strip()

    # Outputs results in GUI text box
    for k, v in parameters_dict.items():
        for parameter in parameters_list:
            if parameter == k:
                if len(k) > 21:
                    textArea.insert(END, (k[:14]) + "\t\t\t\t" + v + "\n")
                else:
                    textArea.insert(END, k + "\t\t\t\t" + v + "\n")

def about():
    """Message box displays information about program"""
    messagebox.showinfo('about', message=informationAbout)

def useGuide():
    """Message box displays guide on how to use the program"""
    messagebox.showinfo('Use Guide', message=informationUseGuide)


######################################################################################################################
# Run Program
######################################################################################################################
# Main buttons
Button(mainWindow, text="Open log file & process", command=openLogFileAndProcess, height=2, width=20, bg='snow').place(x=9, y=5)
Button(mainWindow, text="About", command=about, height=1, width=6, bg='snow').place(x=330, y=23)
Button(mainWindow, text="Guide", command=useGuide, height=1, width=6, bg='snow').place(x=330, y=1)

# Gives the option of dragging and dropping a log file onto icon, or opening file and selecting log file.
if len(sys.argv) == 1:  #
    waitFlag = True
else:
    importedLogFile = sys.argv[1]  # The second argument will be the path of the log file.
    dragDropOpen()

mainWindow.mainloop()