# from .models import Pet, Event

# import datetime as dt
# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np


# def get_sleep_or_nap(event, sleep_or_nap):
#     if event == "wake":
#         return 0
#     elif event == sleep_or_nap:
#         return 1
#     else:
#         return None


# def convert_time_to_timeslot(time_column):
#     return np.floor(pd.to_timedelta(time_column).dt.total_seconds() / 60 / 30) / 2


# def get_sleep_heatmap():
#     from_date = dt.date.today() - dt.timedelta(days=7)
#     raw_data = Event.objects.raw(
#         f"""SELECT
#             id,
#             date,
#             time,
#             event,
#             (SUBSTR(time, 1, 2) * 60 + SUBSTR(time, 4, 2) * 1)/30/2.0 AS time_slot,
#             LAG(
#                 CASE
#                     WHEN event = 'sleep' THEN 2
#                     WHEN event = 'nap' THEN 1
#                     WHEN event = 'wake' THEN 0
#                     ELSE NULL
#                 END
#             ) OVER (ORDER BY date, time) AS sleep_nap
#         FROM pet_event
#         WHERE date >= '{from_date}'
#         ORDER BY date, time"""
#     )

#     df = pd.DataFrame(
#         [(row.date, row.time_slot, row.sleep_nap) for row in raw_data],
#         columns=["date", "time_slot", "sleep_nap"],
#     ).sort_values(["date", "time_slot"])
#     df["sleep_nap"] = df["sleep_nap"].fillna(method="ffill")
#     df = df.groupby(["date", "time_slot"], as_index=False).max()

#     # np.floor(pd.to_timedelta(hm_df["time"]).dt.total_seconds()/60/30)/2
#     time_slots = pd.date_range(start=from_date, end=dt.datetime.now(), freq="0.5H")

#     filled_df = pd.DataFrame()
#     filled_df["date"] = time_slots.map(lambda x: x.date)
#     filled_df["time"] = time_slots.map(lambda x: str(x.time()))
#     filled_df["time_slot"] = (
#         np.floor(pd.to_timedelta(filled_df["time"]).dt.total_seconds() / 60 / 30) / 2
#     )

#     filled_df = filled_df.merge(df, on=["date", "time_slot"], how="left")
#     filled_df = filled_df.sort_values(["date", "time_slot"])
#     filled_df["sleep_nap"] = filled_df["sleep_nap"].fillna(method="ffill")
#     filled_df = filled_df.query("sleep_nap == sleep_nap")
#     print(filled_df.head(10))

#     fig = go.Figure(
#         data=go.Heatmap(
#             z=filled_df["sleep_nap"],
#             x=filled_df["time_slot"],
#             y=filled_df["date"],
#             colorscale="sunset",
#         )
#     )
#     return fig.to_html()


# def import_csv(csv_path):
#     temp_data = pd.read_csv(csv_path)
#     events = [
#         Event(
#             date=dt.datetime.strptime(row["date"], "%d/%m/%Y").strftime("%Y-%m-%d"),
#             time=row["time"],
#             pet=Pet.objects.first(),
#             event=row["event"],
#         )
#         for index, row in temp_data.iterrows()
#     ]
#     Event.objects.bulk_create(events)


# def train_model(df):
#     from sklearn.ensemble import RandomForestClassifier

#     df["lag_event"] = df["event"].shift(1)
#     df["prev_timestamp"] = df.groupby("event")["timestamp"].transform(
#         lambda x: x.shift(1)
#     )
#     df["from_prev"] = df["timestamp"] - df["prev_timestamp"]
#     ml_df = df.copy()
#     ml_df = ml_df.query("event != 'other' and from_prev == from_prev")
#     ml_df["time_slot"] = (
#         np.floor(pd.to_timedelta(ml_df["time"]).dt.total_seconds() / 60 / 30) / 2
#     )

#     ml_df = ml_df.sort_values("timestamp")
#     x_cols = [
#         "timestamp",
#         "time_slot",
#         "from_sleep",
#         "from_nap",
#         "sleep",
#         "nap",
#         "lag_event",
#         "from_prev",
#     ]
#     y_col = "event"
#     ml_df = ml_df[x_cols + [y_col]]
#     ml_df = (
#         pd.concat(
#             [ml_df, pd.get_dummies(ml_df["lag_event"], prefix="lag_event")], axis=1
#         )
#         .fillna(-1)
#         .drop("lag_event", axis=1)
#     )
#     model = RandomForestClassifier()
#     x = [c for c in ml_df.columns if c != y_col and c != "timestamp"]
#     model.fit(ml_df[x], ml_df[y_col])

#     current_time_slot = (
#         np.floor((dt.datetime.now().hour * 60 + dt.datetime.now().minute) / 30) / 2
#     )

#     last_row = ml_df.iloc[-1]
#     to_predict = [
#         [
#             current_time_slot,
#         ]
#     ]
