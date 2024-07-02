import marimo

__generated_with = "0.6.24"
app = marimo.App(width="full", app_title="Science")


@app.cell
def __():
    from enum import IntEnum
    from pathlib import Path

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import marimo as mo
    from interpret.glassbox import ExplainableBoostingRegressor

    from data_model import TrialData, ChassisLength, WheelSize, BodyStyle

    return (
        BodyStyle,
        ChassisLength,
        ExplainableBoostingRegressor,
        IntEnum,
        Path,
        TrialData,
        WheelSize,
        mo,
        np,
        pd,
        px,
    )


@app.cell
def __(IntEnum, TrialData):
    def convert_data(data):

        def convert_field_value(field):
            val = getattr(data, field)
            if isinstance(val, IntEnum):
                return val.name
            return val

        def convert_field_name(name):
            s = name.replace("_", " ").title()
            s = s.replace(" Sec", " (sec)")
            return s

        return {
            convert_field_name(field): convert_field_value(field)
            for field in TrialData.model_fields
        }

    return (convert_data,)


@app.cell
def __(TrialData, convert_data, pd):
    # Load raw pandas DataFrame from csv
    raw_df = pd.read_csv("data/data.csv").sort_values(
        by="average_time_to_finish_sec", ascending=True
    )
    # Convert to Pydantic data model
    trial_datas = [
        convert_data(TrialData(**d)) for d in raw_df.to_dict(orient="records")
    ]
    # Re-convert to Pandas DataFrame
    df = pd.DataFrame(trial_datas)
    return df, raw_df, trial_datas


@app.cell
def __(df, mo):
    mo.vstack(
        [
            mo.center(mo.md("# All Cars")),
            mo.ui.table(df),
        ]
    )
    return


@app.cell
def __(df, mo):
    # Find the best trial
    mo.callout(
        mo.vstack(
            [
                mo.md("# Fastest Car"),
                mo.ui.table(
                    [df.loc[df["Average Time To Finish (sec)"].idxmin()].to_dict()]
                ),
            ]
        ),
        kind="success",
    )
    return


@app.cell
def __(Path, df, dropdowns, enum_classes, enum_names, mo, np):
    selection_values = [
        enum_class[dropdown.value]
        for dropdown, enum_class in zip(dropdowns, enum_classes)
    ]
    image_filename = "".join([str(int(v)) for v in selection_values]) + ".jpg"
    image_path = Path("assets/car_images") / image_filename

    if image_path.is_file():
        selected_image = mo.image(
            src=str(image_path),
            width=400,
            height=400,
            rounded=True,
        )
    else:
        selected_image = mo.callout(
            "No image exists for the selected configuration.", kind="info"
        )

    selected_cimage = mo.center(selected_image)

    mask = np.logical_and.reduce(
        [df[field] == dropdown.value for field, dropdown in zip(enum_names, dropdowns)]
    )
    selected_df = df[mask].head(1)

    selected_table = mo.ui.table(selected_df.reset_index(drop=True))

    mo.vstack(
        [
            mo.center(mo.md("# Select a Car")),
            mo.hstack(dropdowns),
            selected_cimage,
            selected_table,
        ]
    )
    return (
        image_filename,
        image_path,
        mask,
        selected_cimage,
        selected_df,
        selected_image,
        selected_table,
        selection_values,
    )


@app.cell
def __(df, px):
    px.parallel_categories(
        df,
        color="Average Time To Finish (sec)",
        color_continuous_scale=px.colors.diverging.Portland,
        color_continuous_midpoint=df["Average Time To Finish (sec)"].mean(),
    )
    return


@app.cell
def __(ExplainableBoostingRegressor, df):
    # Define features and label
    X = df[["Chassis Length", "Wheel Size", "Body Style"]]
    y = df["Average Time To Finish (sec)"]

    # Train an explainable boosting model, a type of linear regression model.
    # See https://interpret.ml/docs/ebm.html for algorithmic details.
    model = ExplainableBoostingRegressor()
    model.fit(X, y)
    model.explain_global().visualize()
    return X, model, y


@app.cell
def __(BodyStyle, ChassisLength, WheelSize, mo):
    enum_classes = [ChassisLength, WheelSize, BodyStyle]
    enum_names = ["Chassis Length", "Wheel Size", "Body Style"]

    dropdowns = mo.ui.array(
        [
            mo.ui.dropdown(
                options=enum_class.__members__,
                value=next(iter(enum_class.__members__)),
                label=enum_name,
                allow_select_none=False,
            )
            for enum_class, enum_name in zip(enum_classes, enum_names, strict=True)
        ]
    )
    return dropdowns, enum_classes, enum_names


@app.cell
def __(mo):
    mo.vstack(
        [
            mo.center(
                mo.md(
                    """
    # BONUS: `30 Sound.mp3`

    *An mp3 from the nascent internet of the early 2000s.*
    """
                )
            ),
            mo.center(mo.audio(src="assets/tunes/30 Sound.mp3")),
            mo.center(
                mo.md(
                    """
    I have very little information regarding this file. My recollection is that I visited a website that contained a raw `.mid` file, and I recorded the streaming audio output from Windows Media Player to generate the `.mp3` file. It was located adjacent to the science project files in my filesystem, and I couldn't resist including it.

    The actual name of the song is ["Pennsylvania 6-5000"](https://en.wikipedia.org/wiki/Pennsylvania_6-5000_(song)). An original recording can be found on [YouTube](https://youtu.be/AGOUldTrk-A?si=eIwp5FEYq_n-xY2r).
    """
                )
            ),
        ]
    )

    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
