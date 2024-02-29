# # https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application

from flask import Flask, render_template, send_file, make_response, request
import datetime

import base64
from io import BytesIO
from matplotlib.figure import Figure
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("/home/javier/testapp/dht11.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def hello():
    return render_template(
        "index.html", utc_dt=datetime.datetime.now().strftime("%B %d %Y - %H:%M:%S")
    )


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/comments/")
def comments():
    comments = [
        "This is the first comment.",
        "This is the second comment.",
        "This is the third comment.",
        "This is the fourth comment.",
    ]

    return render_template("comments.html", comments=comments)


@app.route("/graph/") #Øvelse 1
def graph():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()  # tilader flere plots i samme figur
    # ax.plot([1, 2]) #Defaults y and increments 1 on x axis

    x1 = [0, 2, 4, 6, 8, 10, 12, 14]
    y1 = [0, 8, 1, 3, 0, 10, 5, 4]

    x2 = [0, 2, 4, 6, 8, 10, 12, 14]
    y2 = [0, 2, 8, 10, 4, 2, 8.5, 4]

    ax.set_facecolor("#000")  # inner plot background color HTML black
    fig.patch.set_facecolor("#000")  # outer plot background color HTML black
    ax.plot(
        x1,
        y1,
        linestyle="dashed",
        c="#eb34d8",
        linewidth="1.5",
        marker="D",
        mec="yellow",
        ms=10,
        mfc="yellow",
    )  # mec = marker edge color, mfc = marker face color
    ax.plot(
        x2,
        y2,
        linestyle="dashed",
        c="#FFFFFF",
        linewidth="1.5",
        marker="*",
        mec="red",
        ms=10,
        mfc="white",
    )  # mec = marker edge color, mfc = marker face color
    ax.set_xlabel("X-axis ")  # setting up X-axis label
    ax.set_ylabel("Y-axis ")  # setting up Y-axis label
    ax.xaxis.label.set_color("red")  # setting up X-axis label color to hotpink
    ax.yaxis.label.set_color("yellow")  # setting up Y-axis label color to hotpink
    ax.tick_params(axis="x", colors="red")  # setting up X-axis tick color to white
    ax.tick_params(axis="y", colors="yellow")  # setting up Y-axis tick color to white
    ax.spines["left"].set_color("#34ebe5")  # setting up Y-axis tick color to blue
    ax.spines["top"].set_color("#eb34d8")  # setting up above X-axis tick color to blue
    ax.spines["bottom"].set_color(
        "#34ebe5"
    )  # setting up above X-axis tick color to blue
    ax.spines["right"].set_color(
        "#eb34d8"
    )  # setting up above X-axis tick color to blue
    # 34ebe5 = turquesa
    # eb34d8 = pink

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    graph_data = f"<img src='data:image/png;base64,{data}'/>"

    return render_template("plot.html", graph_data=graph_data)





@app.route("/sensor_data/")
def sensor_data():
    conn = get_db_connection()
    sensor_data = conn.execute("select * from vejr").fetchall()
    conn.close()
    return render_template("sensor_data.html", sensor_data=sensor_data)


@app.route("/sensor_temp/")
def sensor_temp():

    conn = get_db_connection()
    sensor_data = conn.execute("select datetime, temperature from vejr LIMIT 26").fetchall()

    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(10, 8.5)) #
    ax = fig.subplots()  # tilader flere plots i samme figur
    # ax.plot([1, 2]) #Defaults y and increments 1 on x axis

    x1 = []
    y1 = []
# Example data string: 2024-02-05 13:05:25.882754: 22.0 / 23.0


    for data in sensor_data:
        x1.append(data[0][11:19])  # datetime
        y1.append(data[1])  # temperature


    ax.set_facecolor("#000")  # inner plot background color HTML black
    fig.patch.set_facecolor("#000")  # outer plot background color HTML black
    ax.plot(
        x1,
        y1,
        linestyle="dashed",
        c="#eb34d8",
        linewidth="1.5",
        marker="D",
        mec="yellow",
        ms=10,
        mfc="yellow",
    )  # mec = marker edge color, mfc = marker face colo
    ax.set_xticks(x1)
    ax.set_xticklabels(x1, rotation=90)  # Rotate x-axis labels 90 degrees
    ax.set_xlabel("Datetime")  # setting up X-axis label
    ax.set_ylabel("Temperature (C°)")  # setting up Y-axis label
    ax.xaxis.label.set_color("red")  # setting up X-axis label color to hotpink
    ax.yaxis.label.set_color("yellow")  # setting up Y-axis label color to hotpink
    ax.tick_params(axis="x", colors="red")  # setting up X-axis tick color to white
    ax.tick_params(axis="y", colors="yellow")  # setting up Y-axis tick color to white
    ax.spines["left"].set_color("#34ebe5")  # setting up Y-axis tick color to blue
    ax.spines["top"].set_color("#eb34d8")  # setting up above X-axis tick color to blue
    ax.spines["bottom"].set_color(
        "#34ebe5"
    )  # setting up above X-axis tick color to blue
    ax.spines["right"].set_color(
        "#eb34d8"
    )  # setting up above X-axis tick color to blue
    # 34ebe5 = turquesa
    # eb34d8 = pink

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    graph_data = f"<img src='data:image/png;base64,{data}'/>"

    return render_template("sensor_temp.html", graph_data=graph_data)



@app.route("/sensor_humidity/")
def sensor_humidity():

    conn = get_db_connection()
    sensor_data = conn.execute("select datetime, humidity from vejr LIMIT 25").fetchall()

    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(10, 8.5))
    ax = fig.subplots()  # tilader flere plots i samme figur
    # ax.plot([1, 2]) #Defaults y and increments 1 on x axis

    x1 = []
    y1 = []

    for data in sensor_data:
        x1.append(data[0][11:19])  # datetime
        y1.append(data[1])  # temperature


    ax.set_facecolor("#000")  # inner plot background color HTML black
    fig.patch.set_facecolor("#000")  # outer plot background color HTML black
    ax.plot(
        x1,
        y1,
        linestyle="dashed",
        c="#eb34d8", #pink
        linewidth="1.5",
        marker="D",
        mec="yellow",
        ms=10,
        mfc="yellow",
    )  # mec = marker edge color, mfc = marker face color
    ax.set_xticks(x1)
    ax.set_xticklabels(x1, rotation=90)  # Rotate x-axis labels 90 degrees
    ax.title.set_text("Humidity")  # setting up plot title
    ax.set_xlabel("Datetime")  # setting up X-axis label
    ax.set_ylabel("Humidity %")  # setting up Y-axis label
    ax.xaxis.label.set_color("red")  # setting up X-axis label color to hotpink
    ax.yaxis.label.set_color("yellow")  # setting up Y-axis label color to hotpink
    ax.tick_params(axis="x", colors="red")  # setting up X-axis tick color to white
    ax.tick_params(axis="y", colors="yellow")  # setting up Y-axis tick color to white
    ax.spines["left"].set_color("#34ebe5")  # setting up Y-axis tick color to blue
    ax.spines["top"].set_color("#eb34d8")  # setting up above X-axis tick color to blue
    ax.spines["bottom"].set_color(
        "#34ebe5"
    )  # setting up above X-axis tick color to blue
    ax.spines["right"].set_color(
        "#eb34d8"
    )  # setting up above X-axis tick color to blue
    # 34ebe5 = turquesa
    # eb34d8 = pink

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    graph_data = f"<img src='data:image/png;base64,{data}'/>"

    return render_template("sensor_humidity.html", graph_data=graph_data)
