import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Initialize the initial values of the toggle buttons
flag_status = 0
first_status = 0
redzone_status = 0
title_status = 0
possession_status = 0
touchdown_status = 0  # 1 for HOME, 2 for AWAY
Htimeouts = 3  # Initial timeouts for the home team
Vtimeouts = 3  # Initial timeouts for the visiting team

# Create an initial XML structure
root = ET.Element('info')
flag_elem = ET.SubElement(root, 'flag')
first_elem = ET.SubElement(root, 'first')
redzone_elem = ET.SubElement(root, 'redzone')
title_elem = ET.SubElement(root, 'title')
possession_elem = ET.SubElement(root, 'possession')
touchdown_elem = ET.SubElement(root, 'touchdown')
Htimeouts_elem = ET.SubElement(root, 'Htimeouts')
Vtimeouts_elem = ET.SubElement(root, 'Vtimeouts')

def reset_touchdown():
    global touchdown_status
    time.sleep(5)  # Delay for 5 seconds, adjust as needed
    touchdown_status = 0
    touchdown_elem.text = str(touchdown_status)
    tree = ET.ElementTree(root)
    tree.write('dashboard_data.xml')  # Update the XML file

def background_task():
    # Add any background tasks you may have here
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    global flag_status, first_status, redzone_status, title_status, possession_status, touchdown_status, Htimeouts, Vtimeouts

    if request.method == 'POST':
        if 'flag' in request.form:
            flag_status = int(request.form['flag'])
            flag_elem.text = str(flag_status)
        
        if request.method == 'POST':
            if 'first' in request.form:
                first_status = int(request.form['first'])
                first_elem.text = str(first_status)

        if 'redzone' in request.form:
            redzone_status = int(request.form['redzone'])
            redzone_elem.text = str(redzone_status)

        if 'title' in request.form:
            title_status = int(request.form['title'])
            title_elem.text = str(title_status)

        if 'possession' in request.form:
            selected_value = int(request.form['possession'])

            if possession_status == selected_value:
                possession_status = 0
            else:
                possession_status = selected_value

            possession_elem.text = str(possession_status)

        if 'homeTouchdown' in request.form:
            touchdown_status = 1
            touchdown_elem.text = str(touchdown_status)
            threading.Thread(target=reset_touchdown).start()  # Start the touchdown reset timer

        if 'awayTouchdown' in request.form:
            touchdown_status = 2
            touchdown_elem.text = str(touchdown_status)
            threading.Thread(target=reset_touchdown).start()  # Start the touchdown reset timer

        if 'HtimeoutUp' in request.form and Htimeouts < 3:
            Htimeouts += 1
            Htimeouts_elem.text = str(Htimeouts)

        if 'HtimeoutDown' in request.form and Htimeouts > 0:
            Htimeouts -= 1
            Htimeouts_elem.text = str(Htimeouts)

        if 'VtimeoutUp' in request.form and Vtimeouts < 3:
            Vtimeouts += 1
            Vtimeouts_elem.text = str(Vtimeouts)

        if 'VtimeoutDown' in request.form and Vtimeouts > 0:
            Vtimeouts -= 1
            Vtimeouts_elem.text = str(Vtimeouts)

        tree = ET.ElementTree(root)
        tree.write('dashboard_data.xml')

    return render_template('football_dash.html', flag=flag_status, first=first_status, redzone=redzone_status, title=title_status, possession=possession_status, touchdown=touchdown_status, Htimeouts=Htimeouts, Vtimeouts=Vtimeouts)

if __name__ == '__main__':
    app.run(debug=True)
