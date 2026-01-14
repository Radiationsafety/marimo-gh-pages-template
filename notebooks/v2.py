import marimo

__generated_with = "0.19.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Example of marimo notebook with Landweber unfolding method
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.graph_objects as go
    from bssunfold import Detector
    from bssunfold import RF_GSF
    df = pd.DataFrame.from_dict(RF_GSF, orient='columns')
    detector = Detector(df)
    return detector, go, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Input detector readings
    """)
    return


@app.cell
def _(mo):
    default_readings = {
        "0in": 3, "2in": 9, "3in": 36, "5in": 41, "6in": 219,
        "8in": 220, "10in": 172, "12in": 120, "15in": 66, "18in": 34
    }

    reading_inputs = {}
    for sphere, value in default_readings.items():
        reading_inputs[sphere] = mo.ui.number(
            value=value, label=f"{sphere}", step=1, start=0.0
        )

    ui_display = mo.hstack([
        mo.vstack([reading_inputs["0in"], reading_inputs["2in"], reading_inputs["3in"]]),
        mo.vstack([reading_inputs["5in"], reading_inputs["6in"], reading_inputs["8in"]]),
        mo.vstack([reading_inputs["10in"], reading_inputs["12in"], reading_inputs["15in"]]),
        mo.vstack([reading_inputs["18in"]])
    ])

    ui_display
    return (reading_inputs,)


@app.cell
def _(mo):
    iterations = mo.ui.slider(
        value=3000, start=100, stop=10000, step=100,
        label="Number of iterations"
    )
    return (iterations,)


@app.cell
def _(mo):
    reg_power = mo.ui.slider(
        value=-4, start=-7, stop=2, step=0.25,
        label="Regularization power 10^x"
    )
    return (reg_power,)


@app.cell
def _(iterations):
    iterations
    return


@app.cell
def _(reg_power):
    reg_power
    return


@app.cell
def _(detector, go, iterations, reading_inputs, reg_power):
    current_readings = {sphere: input.value for sphere, input in reading_inputs.items()}
    result = detector.unfold_landweber(current_readings, max_iterations=iterations.value)
    result2 = detector.unfold_cvxpy(current_readings, regularization=10**reg_power.value)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result["energy"], y=result["spectrum"], 
                           mode="lines", name="Landweber", 
                           line=dict(color="blue", width=2), fill="tozeroy"))
    fig.add_trace(go.Scatter(x=result2["energy"], y=result2["spectrum"],
                            mode="lines", name="CVXPY", 
                            line=dict(color="red", width=2), fill="tozeroy"))
    fig.update_layout(xaxis_title="Energy, MeV", height=500, 
                     template="plotly_white").update_xaxes(type="log")
    return


if __name__ == "__main__":
    app.run()
