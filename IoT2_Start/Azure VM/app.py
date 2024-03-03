from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure
from time import sleep
from get_dht_data import get_stue_data



app = Flask(__name__)

def graph_stue_temp():
    # Get data
    timestamps, temperature, _ = get_stue_data()


    # Create figure and subplot
    fig = Figure()
    ax = fig.subplots()

    # Plot data
    ax.plot(timestamps, temperature, label='Temperature', linestyle='-', marker='o', color='r')

    # Set colors
    ax.set_facecolor('#121212')  # Set the background color to dark grey
    fig.patch.set_facecolor('#121212')  # Set the figure background color to dark grey
    ax.title.set_color('white')  # Set the title color to white
    ax.xaxis.label.set_color('white')  # Set the x-axis label color to white
    ax.yaxis.label.set_color('white')  # Set the y-axis label color to white
    ax.tick_params(colors='white')  # Set the tick parameters color to white

    # Adjust subplot parameters
    fig.subplots_adjust(bottom=0.5, left=0.2)
    ax.tick_params(axis='x', rotation=45)

    # Set labels
    ax.set_title('Temperature stue')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature')

    # Invert x-axis
    ax.invert_xaxis()

    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data_img = f"<img style='img-fluid' src='data:image/png;base64,{data}'/>"

    return data_img


def graph_stue_hum():
    timestamps, _, humidity = get_stue_data()

    fig = Figure()
    ax = fig.subplots()

    # Plot data
    ax.plot(timestamps, humidity, label='Humidity', linestyle='dashed', marker='o', color='#00FF00')

    # Adjust subplot parameters
    fig.subplots_adjust(bottom=0.5, left=0.2)
    ax.tick_params(axis='x', rotation=45)

    # Set colors
    ax.set_facecolor('#121212')  # Set the background color to dark grey
    fig.patch.set_facecolor('#121212')  # Set the figure background color to dark grey
    ax.title.set_color('white')  # Set the title color to white
    ax.xaxis.label.set_color('white')  # Set the x-axis label color to white
    ax.yaxis.label.set_color('white')  # Set the y-axis label color to white
    ax.tick_params(colors='white')  # Set the tick parameters color to white

    # Set labels
    ax.set_title('Humidity stue')
    ax.set_xlabel('Time')
    ax.set_ylabel('Humidity')

    # Invert x-axis
    ax.invert_xaxis()

    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data_img = f"<img style='img-fluid' src='data:image/png;base64,{data}'/>"

    return data_img


def graph_koekken():
    ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/stue")
def stue():
    return render_template('stue.html', data_img=graph_stue_temp(), data_img2=graph_stue_hum())

@app.route("/koekken")
def koekken():
    return render_template('koekken.html', data_img=graph_koekken())


@app.route("/vaerelse")
def vaerelse():
    # TODO
    return render_template('vaerelse.html')

@app.route("/taend/", methods=['POST'])
def taend():
    # TODO
    return render_template('vaerelse.html')

@app.route("/sluk/", methods=['POST'])
def sluk():
    # TODO
    return render_template('vaerelse.html')

@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

# app.run(debug=True, host='0.0.0.0', port=5000)