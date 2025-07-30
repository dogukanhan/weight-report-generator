
import plotly.express as px

def group_by_type(df):
    data = df.groupby('Type').size().reset_index(name='Count')
    fig = px.bar(data, x='Type', y='Count', color='Type')
    div = fig.to_html(full_html=False)
    return div

def group_by_date(df):
    data = df.groupby('Date').size().reset_index(name='Count')
    fig = px.bar(data, x='Date', y='Count', color='Date')
    div = fig.to_html(full_html=False)
    return div

def type_bumble_chart(df):
    fig = px.scatter(df, x='Date', y='Weight', size='Repetition')
    div = fig.to_html(full_html=False)
    return div

def type_fail_chart(df):
    fig = px.bar(df, x='Weight', y='Missing')
    div = fig.to_html(full_html=False)
    return div

def type_training_days(df):
    fig = px.bar(df, x='Date', y='Weight')
    fig.update_layout(yaxis_title='Weight')
    div = fig.to_html(full_html=False)
    return div

def type_rpe_chart(df):
    fig = px.line(df, x='Date', y='RPE')
    div = fig.to_html(full_html=False)
    return div

def type_analysis_chart(df,result):
    fig = px.bar(df, x='Repetition', y='Weight')
   
    fig.add_vline(
        x=8,
        line_dash="dash",
        line_color="red",
        annotation_text="%80 of 1 RM",
        annotation_position="top",
        annotation_font_color="red"
    )

    if("oneRm" in result):
        fig.add_hline(
            y=result["oneRm"] * 0.8,
            line_dash="dash",
            line_color="red",
            annotation_text="%80 of 1 RM",
            annotation_position="top",
            annotation_font_color="red"
        )

    div = fig.to_html(full_html=False)
    return div


def date_type_weight_chart(df):
    fig = px.bar(df, x='Type', y='Weight', color='Date')
    div = fig.to_html(full_html=False)
    return div