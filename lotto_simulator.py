import random, csv, os, datetime, sqlite3, wx    

def init():   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zahlen (
            id INTEGER PRIMARY KEY,
            datum,
            zahl1,
            zahl2,
            zahl3,
            zahl4,
            zahl5,
            zahl6,
            zusatzzahl,
            superzahl)
        ''')
    
def export_csv():
    path = 'zahlen/lottozahlen.csv'
    
    cursor.execute('SELECT * from zahlen')
    
    zahlen = list()
    for i in cursor:
        zahlen.append(i)           
        
    if os.path.exists(path):
        os.remove(path)
        init()
    
    datei = open('zahlen/lottozahlen.csv', 'a')
    
    for i in zahlen:
        datei.writelines(str(i[0]) + ';' +
                         str(i[1]) + ';' +
                         str(i[2]) + ';' +
                         str(i[3]) + ';' +
                         str(i[4]) + ';' +
                         str(i[5]) + ';' +
                         str(i[6]) + ';' +
                         str(i[7]) + ';' +
                         str(i[8]) + ';' +
                         str(i[9]) + '\n')
    datei.close()

class Lottozahlen():
    def create(self):
        lottozahlen = []

        for i in range(1,6+1):
            while len(lottozahlen) < 7:
                x = random.randint(1,49)
                if x not in lottozahlen:
                    lottozahlen.append(x)
    
        superzahl = random.randint(0,9)
        lottozahlen.append(superzahl)
    
        return lottozahlen

    def add(self, x):  
        heute = datetime.date.today()
    
        cursor.execute('''
            INSERT INTO zahlen (
                datum,
                zahl1,
                zahl2,
                zahl3,
                zahl4,
                zahl5,
                zahl6,
                zusatzzahl,
                superzahl)
            VALUES 
                (?,?,?,?,?,?,?,?,?)''',(heute,x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))
        conn.commit()
        
class MainWindow(wx.Frame):            
    def __init__(self, parent, id, title):
        
        wx.Frame.__init__(self, parent, id, title, size=(175,165), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        panel = wx.Panel(self, -1)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)     
        
        panel1 = wx.Panel(panel, -1)
        
        box = wx.StaticBox(panel1, -1, 'Befehle')
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)    
        
        button_neu = wx.Button(panel1, 1, 'Neu')
        bsizer.Add(button_neu, 1, wx.DOWN, 5)
        
        button_loeschen = wx.Button(panel1, 2, 'Loeschen')
        bsizer.Add(button_loeschen, 1, wx.DOWN, 5)
        
        button_csvexport = wx.Button(panel1, 3, 'CSV-Export')
        bsizer.Add(button_csvexport, 1, wx.DOWN, 5)
        
        button_gfxexport = wx.Button(panel1, 4, 'GFX-Export')
        bsizer.Add(button_gfxexport, 1, wx.DOWN, 5)
                 
        panel1.SetSizer(bsizer)

        panel2 = wx.Panel(panel, -1)
        
        gsizer = wx.FlexGridSizer(6,3)
        
        gsizer.Add(wx.StaticText(panel2, -1, '1', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, '2', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, '3', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        
        self.txtbox1 = wx.TextCtrl(panel2, -1, size = (25, -1))
        self.txtbox2 = wx.TextCtrl(panel2, -1, size = (25, -1))
        self.txtbox3 = wx.TextCtrl(panel2, -1, size = (25, -1))
        gsizer.Add(self.txtbox1)
        gsizer.Add(self.txtbox2)
        gsizer.Add(self.txtbox3)
        
        gsizer.Add(wx.StaticText(panel2, -1, '4', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, '5', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, '6', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        
        self.txtbox4 = wx.TextCtrl(panel2, -1, size = (25, -1))
        self.txtbox5 = wx.TextCtrl(panel2, -1, size = (25, -1))
        self.txtbox6 = wx.TextCtrl(panel2, -1, size = (25, -1))
        gsizer.Add(self.txtbox4)
        gsizer.Add(self.txtbox5)
        gsizer.Add(self.txtbox6)
        
        gsizer.Add(wx.StaticText(panel2, -1, 'SZ', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, 'ZZ', (5, 5)), 0,  wx.ALIGN_CENTER | wx.TOP, 5)
        gsizer.Add(wx.StaticText(panel2, -1, ''))
        
        self.txtbox7 = wx.TextCtrl(panel2, -1, size = (25, -1))
        self.txtbox8 = wx.TextCtrl(panel2, -1, size = (25, -1))
        gsizer.Add(self.txtbox7)
        gsizer.Add(self.txtbox8)
        
        panel2.SetSizer(gsizer)
        
        self.Bind(wx.EVT_BUTTON, self.onClick_neu, button_neu)
        self.Bind(wx.EVT_BUTTON, self.onClick_loeschen, button_loeschen)
        self.Bind(wx.EVT_BUTTON, self.onClick_csv, button_csvexport)
        
        vbox.Add(panel1, 0, wx.RIGHT, 5)
        vbox.Add(panel2, 0, wx.TOP, 5)
            
        panel.SetSizer(vbox)

        self.Center()
        self.Show(True)     
        
    def onClick_neu(self,event):  
        lotto = Lottozahlen()
        zahlen = lotto.create()
        lotto.add(zahlen)
        self.txtbox1.WriteText(str(zahlen[0]))
        self.txtbox2.WriteText(str(zahlen[1]))
        self.txtbox3.WriteText(str(zahlen[2]))
        self.txtbox4.WriteText(str(zahlen[3]))
        self.txtbox5.WriteText(str(zahlen[4]))
        self.txtbox6.WriteText(str(zahlen[5]))
        self.txtbox7.WriteText(str(zahlen[6]))
        self.txtbox8.WriteText(str(zahlen[7]))
        
    def onClick_loeschen(self, event):
        self.txtbox1.Clear()
        self.txtbox2.Clear()
        self.txtbox3.Clear()
        self.txtbox4.Clear()
        self.txtbox5.Clear()
        self.txtbox6.Clear()
        self.txtbox7.Clear()
        self.txtbox8.Clear()
        
    def onClick_csv(self, event):
        export_csv()

if __name__ == '__main__':      
    conn = sqlite3.connect('zahlen/zahlen.sqlite')
    cursor = conn.cursor()                             
    app = wx.App()    
    MainWindow(None, -1, '.lotto-gen 01')
    app.MainLoop()