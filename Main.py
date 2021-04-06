######################################################################################################################
# Initialisation
######################################################################################################################

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

parameters_dict = {}  # New dictionary holding relevant data from log file.

parameters_list = ['Filter', 'Frame Averaging', 'Camera binning', 'Source Voltage (kV)',
                   'Source Current (uA)', 'Exposure (ms)', 'Rotation Step (deg)', 'Scanning position',
                   'Image Pixel Size (um)', 'Use 360 Rotation', 'Random Movement', 'Scan duration',
                   'Minimum for CS to Image Conversion', 'Maximum for CS to Image Conversion',
                   'Smoothing', 'Ring Artifact Correction', 'Beam Hardening Correction (%)']

######################################################################################################################
# GUI Interface Setup
######################################################################################################################

# Main windows setup
mainWindow = Tk()  # Links main window to the interpreter
mainWindow.title("LogFile_ReadEasy by Kamil_Sokolowski")
mainWindow.geometry("394x357+500+300")  # Window size and initial position
mainWindow['bg'] = 'gray98'  # Background colour

# Main text area
textArea = Text(mainWindow, width=46, height=17, borderwidth=2)
textArea.place(x=10, y=50)
textArea.insert(END, "\n\n\n\tReady to read easy?")

# Log file path output text area
logPath = Text(mainWindow, width=36, height=1)
logPath.place(x=70, y=330)

# Labels
Label(mainWindow, text="Log Path:", bg='gray98').place(x=8, y=330)
Label(mainWindow, text="LogFile_ReadEasy", bg='gray98', font='Helvetica').place(x=200, y=8)

menuBar = Menu(mainWindow, background='#ff0000', foreground='black', activebackground='gray98', activeforeground='black')
file = Menu(menuBar, tearoff=0, background='gray98', foreground='black')
file.add_command(label="Compare Two Datasets")
file.add_command(label="Additional Parameters")
file.add_command(label="Save output")
file.add_command(label="Exit", command=mainWindow.quit)
menuBar.add_cascade(label="More", menu=file)

help = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="About", menu=help)
mainWindow.config(menu=menuBar)


######################################################################################################################
# Functions
######################################################################################################################

def openLogFileAndProcess():
    textArea.delete("1.0", "end")
    logPath.delete("1.0", "end")

    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/",
        title="Open Log file",
        filetypes=(("Log Files", "*.log"),)
    )


    logPath.insert(END, tf)  # Writes path address to text box in GUI

    # Opens and parses the data from log file
    with open(tf, 'r') as fin:
        for line in fin:
            for i in parameters_list:
                if i in line:
                    equalSignPosition = line.find('=')
                    parameters_dict[line[:equalSignPosition]] = (line[equalSignPosition + 1:]).strip()

    # Outputs results in GUI text box
    for key, value in parameters_dict.items():
        for parameter in parameters_list:
            if parameter == key:
                if len(key) > 20:
                    textArea.insert(END, (key[:15]) + "\t\t\t\t" + value + "\n")
                else:
                    textArea.insert(END, key + "\t\t\t\t" + value + "\n")

def dragDropOpen():
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
    messagebox.showinfo('LogFile_ReadEasy', 'Version 2.3 6th April 2021\n\nDeveloped by Kamil Sokolowski \n'
                                            'kamil.sokolowski@tri.edu.au \n')


######################################################################################################################
# Run Program
######################################################################################################################
# Main button
Button(mainWindow, text="Open Log File & Process", command=openLogFileAndProcess, height=2, width=20, bg='snow').place(x=9, y=5)

# Gives the option of dragging and dropping a log file onto icon, or opening file and selecting log file.
if len(sys.argv) == 1:  #
    waitFlag = True
else:
    importedLogFile = sys.argv[1]  # The second argument will be the path of the log file.
    dragDropOpen()

help.add_command(label="Developer", command=about)

mainWindow.mainloop()