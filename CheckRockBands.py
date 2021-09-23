import webbrowser

bands = {"August Burns Red": "https://en.wikipedia.org/wiki/August_Burns_Red",
         "Converge": "https://en.wikipedia.org/wiki/Converge_(band)",
         "Korn": "https://en.wikipedia.org/wiki/Korn",
         "Marilyn Manson": "https://en.wikipedia.org/wiki/Marilyn_Manson_(band)",
         "Parkway Drive": "https://en.wikipedia.org/wiki/Parkway_Drive",
         "Slipknot": "https://en.wikipedia.org/wiki/Slipknot_%28band%29",
         "System of a Down": "https://en.wikipedia.org/wiki/System_of_a_Down",
         "Tool": "https://en.wikipedia.org/wiki/Tool_(band)"
         }

for band in bands:
    webbrowser.open(bands[band], new=2)
