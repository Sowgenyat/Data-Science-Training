import pandas as pd
import numpy as np
attendance_df = pd.read_csv("attendance.csv")
tasks_df = pd.read_csv("tasks.csv")
attendance_df.dropna(subset=['clock_in', 'clock_out'], inplace=True)
attendance_df['clock_in'] = pd.to_datetime(attendance_df['clock_in'])
attendance_df['clock_out'] = pd.to_datetime(attendance_df['clock_out'])
attendance_df['work_hours'] = (attendance_df['clock_out'] - attendance_df['clock_in']).dt.total_seconds() / 3600
work_summary = attendance_df.groupby('employee_id')['work_hours'].sum().reset_index()
task_summary = tasks_df[tasks_df['status'].str.lower() == 'completed'] \
                    .groupby('employee_id').size().reset_index(name='tasks_completed')
summary_df = pd.merge(work_summary, task_summary, on='employee_id', how='left')
summary_df['tasks_completed'] = summary_df['tasks_completed'].fillna(0)
summary_df['productivity_score'] = summary_df['tasks_completed'] / summary_df['work_hours']
summary_df['work_hours'] = summary_df['work_hours'].round(2)
summary_df['productivity_score'] = summary_df['productivity_score'].round(2)
summary_df.to_csv("week2_productivity_report.csv", index=False)
print(summary_df.sort_values(by='productivity_score', ascending=False))
