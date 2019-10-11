import os
import mcdata

from colorama import Fore
from colorama import init

from os import system
from nbt.nbt import NBTFile
from http.server import BaseHTTPRequestHandler, HTTPServer

init(convert=True) if os.name == 'nt' else init()

print(Fore.MAGENTA + '\nMinecraft Schematic Info')
print(Fore.WHITE + 'Developed by Drew Snow\n')

#Get all files and not folders
folder = 'Schematics/'
files = [f for f in os.listdir(folder) if os.path.isfile(folder + f)]

print(Fore.GREEN + 'Found ' + str(len(files)) + ' schematic(s)\n')

table = []
schems = []

#Scan all files for NBT data
i = 0
while i < len(files):
    f = files[i]

    if os.name == 'nt':
        system('title Current File: ' + f + ' ^| Files left: ' +
               str(len(files) - i))

    try:
        data = NBTFile(folder + f)

        blocks = list(filter(lambda x: x != 0, data['Blocks']))
        usedMaterials = mcdata.findBlocks(blocks)
        materials = []
        realistic = True;

        for j in usedMaterials:
            materials.append(mcdata.blockFromID(j)['name'])
            if mcdata.isUnrealistic(j): realistic = False
        
        array = []

        array.append(os.path.splitext(f)[0])
        array.append(str(data['Width']))
        array.append(str(data['Height']))
        array.append(str(data['Length']))
        array.append(str(len(blocks)))
        array.append(', '.join(materials))
        array.append(str(realistic))

        table.append(array)
        schems.append([
            os.path.splitext(f)[0], data['Width'], data['Height'],
            data['Length'],
            len(blocks)
        ])

        print(Fore.CYAN + 'Parsed schematic file ' + Fore.YELLOW + f)
    except:
        print(Fore.RED + 'Unable to read file ' + Fore.YELLOW + f)

    i += 1

print(Fore.GREEN + '\nChecking for duplicates')

#Check scanned schematics for duplicates
seen = []
for x in schems:
    x = list(map(str, x))
    for y in seen:
        if x[1] == y[1] and x[2] == y[2] and x[3] == y[3] and x[4] == y[4]:
            print(Fore.YELLOW + x[0], Fore.CYAN + 'and', Fore.YELLOW + y[0], Fore.CYAN + 'seem to be the same')

    seen.append(x)

#Create HTML for server
content = '''<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width">
	<title>Schematic Info</title>
    <link href="https://unpkg.com/tabulator-tables@4.4.3/dist/css/tabulator.min.css" rel="stylesheet">
	<style>
        /*Theme the Tabulator element*/
        #table {
            box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.4);
            font-family: Arial, Roboto, Verdana;
            background-color: #575757;
            border: 1px solid #b5b5b5;
            border-radius: 5px;
        }

        /*Theme the header*/
        #table .tabulator-header {
            border-bottom: 2px solid #fc4103;
            background-color: #000;
            color: #000;
        }

        /*Allow column header names to wrap lines*/
        #table .tabulator-header .tabulator-col,
        #table .tabulator-header .tabulator-col-row-handle {
            white-space: normal;
        }

        /*Color the table rows*/
        #table .tabulator-tableHolder .tabulator-table .tabulator-row{
            background-color: #d1d1d1;
            color: #000;
        }

        /*Color even rows*/
        #table .tabulator-tableHolder .tabulator-table .tabulator-row:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>

<body>
    <div id="table"></div>
    <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.4.3/dist/js/tabulator.min.js"></script>
	<script>
        var tabledata = %s;

        tabledata = tabledata.map(array => {
            return {
                'name': array[0] || 'Unknown',
                'width': array[1] || null,
                'height': array[2] || null,
                'length': array[3] || null,
                'blocks': array[4] || null,
                'materials': array[5] || null,
                'realistic': array[6] || null
            };
        });

        var table = new Tabulator('#table', {
        height: ((tabledata.length * 24) + 24 + 8) > window.innerHeight > 516 ? window.innerHeight - 16 : null, 
        data: tabledata,
        groupBy: 'realistic',
        groupHeader: function (value, count, data, group) {
            let title = 'Unrealistic'
            if (value == 'True') title = 'Realistic';
            return `${title}<span style='color:#d00; margin-left:10px;'>(${count} item)</span>`;
        },
        layout: 'fitColumns', 
        columns:[
            {title: 'Name', field: 'name', sorter: 'string'},
            {title: 'Width', field: 'width', sorter: 'number'},
            {title: 'Height', field: 'height', sorter: 'number'},
            {title: 'Length', field: 'length', sorter: 'number'},
            {title: 'Blocks', field: 'blocks', sorter: 'number'},
            {title: 'Realistic', field: 'realistic', sorter: 'string'},
            {title: 'Materials', field: 'materials', sorter: 'string'}
        ]
    });
    </script>
</body>

</html>
''' % (str(table))

port = 8000

#Server handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))
        return

server = HTTPServer(('', port), handler)
print(Fore.GREEN + '\nStarted server on port', port)
server.serve_forever()

print(Fore.BLUE + '\nDone.')
