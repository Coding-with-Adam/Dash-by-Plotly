import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Load & prep data ──────────────────────────────────────────────────────────
df = pd.read_csv('Fifa_2022_world_cup_matches.csv')

# Build a "per-team" long-form dataframe for team-level stats
def team_stats(df):
    rows = []
    for _, r in df.iterrows():
        for side, opp in [('team1', 'team2'), ('team2', 'team1')]:
            rows.append({
                'team':        r[side],
                'opponent':    r[opp],
                'category':    r['category'],
                'goals_for':   r[f'number of goals {side}'],
                'goals_against': r[f'number of goals {opp}'],
                'shots':       r[f'total attempts {side}'],
                'on_target':   r[f'on target attempts {side}'],
                'possession':  int(r[f'possession {side}'].replace('%','')),
                'passes':      r[f'passes {side}'],
                'passes_completed': r[f'passes completed {side}'],
                'yellow_cards': r[f'yellow cards {side}'],
                'red_cards':   r[f'red cards {side}'],
                'fouls':       r[f'fouls against {side}'],
                'corners':     r[f'corners {side}'],
                'crosses':     r[f'crosses {side}'],
                'forced_turnovers': r[f'forced turnovers {side}'],
            })
    return pd.DataFrame(rows)

team_df = team_stats(df)
all_teams = sorted(team_df['team'].unique())

STAGE_ORDER = [
    'Group A','Group B','Group C','Group D','Group E','Group F','Group G','Group H',
    'Round of 16','Quarter-final','Semi-final','Play-off for third place','Final'
]

# Colour palette
GREEN  = '#2dc653'
GOLD   = '#f5a623'
WHITE  = '#ffffff'
BG     = '#0d1b2a'
PANEL  = '#132033'
ACCENT = '#1a73e8'
TEXT   = '#e8edf2'
MUTED  = '#8899aa'

CARD_STYLE = {
    'backgroundColor': PANEL,
    'borderRadius': '10px',
    'padding': '20px',
    'marginBottom': '16px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.4)',
}

CHART_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=TEXT, family='Inter, Arial, sans-serif'),
    margin=dict(t=40, l=40, r=20, b=40),
)

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(style={'backgroundColor': BG, 'minHeight': '100vh',
                             'fontFamily': 'Inter, Arial, sans-serif', 'color': TEXT}, children=[

    # Header
    html.Div(style={'background': f'linear-gradient(135deg, #0a3d62, #1a73e8)',
                    'padding': '24px 32px', 'marginBottom': '24px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.5)'}, children=[
        html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '16px'}, children=[
            html.Span('⚽', style={'fontSize': '40px'}),
            html.Div([
                html.H1('FIFA World Cup 2022', style={'margin': 0, 'fontSize': '28px',
                        'fontWeight': '700', 'color': WHITE}),
                html.P('Qatar • 64 Matches • 32 Teams', style={'margin': '4px 0 0',
                       'color': '#a0c4ff', 'fontSize': '14px'}),
            ])
        ])
    ]),

    # Tab navigation
    html.Div(style={'padding': '0 32px 24px'}, children=[
        dcc.Tabs(id='tabs', value='overview', style={'border': 'none'},
            colors={'border': 'transparent', 'primary': ACCENT, 'background': PANEL},
            children=[
                dcc.Tab(label='📊 Tournament Overview', value='overview',
                    style={'color': MUTED, 'backgroundColor': PANEL, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0'},
                    selected_style={'color': WHITE, 'backgroundColor': ACCENT, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0', 'fontWeight': '600'}),
                dcc.Tab(label='🏆 Team Deep-Dive', value='team',
                    style={'color': MUTED, 'backgroundColor': PANEL, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0'},
                    selected_style={'color': WHITE, 'backgroundColor': ACCENT, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0', 'fontWeight': '600'}),
                dcc.Tab(label='⚔️ Head-to-Head', value='h2h',
                    style={'color': MUTED, 'backgroundColor': PANEL, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0'},
                    selected_style={'color': WHITE, 'backgroundColor': ACCENT, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0', 'fontWeight': '600'}),
                dcc.Tab(label='🔬 Scatter Explorer', value='scatter',
                    style={'color': MUTED, 'backgroundColor': PANEL, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0'},
                    selected_style={'color': WHITE, 'backgroundColor': ACCENT, 'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px 8px 0 0', 'fontWeight': '600'}),
            ]
        ),
        html.Div(id='tab-content', style={'backgroundColor': PANEL, 'borderRadius': '0 8px 8px 8px',
                                          'padding': '24px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.4)'}),
    ])
])


# ── Tab router ────────────────────────────────────────────────────────────────
@app.callback(Output('tab-content', 'children'), Input('tabs', 'value'))
def render_tab(tab):
    if tab == 'overview':   return overview_layout()
    if tab == 'team':       return team_layout()
    if tab == 'h2h':        return h2h_layout()
    if tab == 'scatter':    return scatter_layout()


# ── OVERVIEW TAB ──────────────────────────────────────────────────────────────
def overview_layout():
    total_goals = int(df['number of goals team1'].sum() + df['number of goals team2'].sum())
    avg_goals   = round(total_goals / len(df), 2)
    total_yc    = int(df['yellow cards team1'].sum() + df['yellow cards team2'].sum())
    total_rc    = int(df['red cards team1'].sum() + df['red cards team2'].sum())

    stat_card = lambda icon, label, val, color: html.Div(style={**CARD_STYLE, 'textAlign': 'center',
            'borderTop': f'4px solid {color}'}, children=[
        html.Div(icon, style={'fontSize': '32px'}),
        html.Div(str(val), style={'fontSize': '36px', 'fontWeight': '700', 'color': color, 'margin': '8px 0 4px'}),
        html.Div(label, style={'fontSize': '13px', 'color': MUTED}),
    ])

    # Goals by stage
    stage_data = []
    for _, r in df.iterrows():
        stage_data.append({'stage': r['category'], 'goals': r['number of goals team1'] + r['number of goals team2']})
    stage_df = pd.DataFrame(stage_data).groupby('stage')['goals'].agg(['sum','count','mean']).reset_index()
    stage_df.columns = ['stage','total_goals','matches','avg_goals']
    stage_df['order'] = stage_df['stage'].map({s: i for i, s in enumerate(STAGE_ORDER)})
    stage_df = stage_df.sort_values('order')

    fig_bar = px.bar(stage_df, x='stage', y='total_goals', color='avg_goals',
                     color_continuous_scale='Blues',
                     labels={'total_goals': 'Total Goals', 'stage': 'Stage', 'avg_goals': 'Avg Goals/Match'},
                     title='Goals by Tournament Stage')
    fig_bar.update_layout(**CHART_THEME)
    fig_bar.update_xaxes(tickangle=-30, gridcolor='#1e3a5a', color=MUTED)
    fig_bar.update_yaxes(gridcolor='#1e3a5a', color=MUTED)
    fig_bar.update_traces(marker_line_width=0)

    # Top scorers (team-level)
    scorer_df = team_df.groupby('team')['goals_for'].sum().reset_index().sort_values('goals_for', ascending=True).tail(15)
    fig_top = px.bar(scorer_df, x='goals_for', y='team', orientation='h',
                     color='goals_for', color_continuous_scale='Greens',
                     labels={'goals_for': 'Goals Scored', 'team': ''},
                     title='Top Goal-Scoring Teams')
    fig_top.update_layout(**CHART_THEME, coloraxis_showscale=False)
    fig_top.update_xaxes(gridcolor='#1e3a5a', color=MUTED)
    fig_top.update_yaxes(gridcolor='#1e3a5a', color=MUTED)
    fig_top.update_traces(marker_line_width=0)

    return html.Div([
        # KPI Row
        html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(4,1fr)', 'gap': '16px', 'marginBottom': '24px'}, children=[
            stat_card('⚽', 'Total Goals', total_goals, GREEN),
            stat_card('📈', 'Avg Goals / Match', avg_goals, GOLD),
            stat_card('🟨', 'Yellow Cards', total_yc, GOLD),
            stat_card('🟥', 'Red Cards', total_rc, '#e74c3c'),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=fig_bar, config={'displayModeBar': False})]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=fig_top, config={'displayModeBar': False})]),
        ])
    ])


# ── TEAM DEEP-DIVE TAB ────────────────────────────────────────────────────────
def team_layout():
    return html.Div([
        html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'alignItems': 'center'}, children=[
            html.Label('Select Team:', style={'fontWeight': '600', 'whiteSpace': 'nowrap'}),
            dcc.Dropdown(id='team-select', options=[{'label': t.title(), 'value': t} for t in all_teams],
                         value='FRANCE', clearable=False,
                         style={'flex': 1, 'backgroundColor': BG, 'color': BG}),
        ]),
        html.Div(id='team-output'),
    ])


@app.callback(Output('team-output', 'children'), Input('team-select', 'value'))
def update_team(team):
    t = team_df[team_df['team'] == team].copy()
    wins   = int((t['goals_for'] > t['goals_against']).sum())
    draws  = int((t['goals_for'] == t['goals_against']).sum())
    losses = int((t['goals_for'] < t['goals_against']).sum())
    gf     = int(t['goals_for'].sum())
    ga     = int(t['goals_against'].sum())
    avg_poss = round(t['possession'].mean(), 1)
    pass_acc = round((t['passes_completed'] / t['passes'] * 100).mean(), 1)

    stat_mini = lambda label, val, color=TEXT: html.Div(style={**CARD_STYLE, 'textAlign': 'center',
            'padding': '14px'}, children=[
        html.Div(str(val), style={'fontSize': '28px', 'fontWeight': '700', 'color': color}),
        html.Div(label, style={'fontSize': '12px', 'color': MUTED, 'marginTop': '4px'}),
    ])

    # Match-by-match goals chart
    t2 = t.copy()
    t2['match'] = t2.apply(lambda r: f"vs {r['opponent'].title()}", axis=1)
    t2['result'] = t2.apply(lambda r: 'Win' if r['goals_for'] > r['goals_against']
                            else ('Draw' if r['goals_for'] == r['goals_against'] else 'Loss'), axis=1)
    color_map = {'Win': GREEN, 'Draw': GOLD, 'Loss': '#e74c3c'}

    fig_match = go.Figure()
    for res, grp in t2.groupby('result'):
        fig_match.add_trace(go.Bar(name=res, x=grp['match'], y=grp['goals_for'],
                                    marker_color=color_map[res], text=grp['goals_for'],
                                    textposition='outside'))
    fig_match.add_trace(go.Scatter(x=t2['match'], y=t2['goals_against'], mode='lines+markers',
                                   name='Goals Conceded', line=dict(color='#e74c3c', dash='dot'),
                                   marker=dict(size=8)))
    fig_match.update_layout(**CHART_THEME, title=f'{team.title()} — Goals per Match',
                             barmode='stack', legend=dict(orientation='h', y=1.12))
    fig_match.update_xaxes(tickangle=-25, gridcolor='#1e3a5a', color=MUTED)
    fig_match.update_yaxes(gridcolor='#1e3a5a', color=MUTED)

    # Radar chart
    cats = ['Possession %', 'Pass Accuracy %', 'Shot Accuracy %', 'Corners', 'Forced Turnovers']
    vals = [
        avg_poss,
        pass_acc,
        round((t['on_target'] / t['shots'].replace(0,1) * 100).mean(), 1),
        round(t['corners'].mean(), 1) * 5,   # scaled for radar
        round(t['forced_turnovers'].mean(), 1) * 3,
    ]
    fig_radar = go.Figure(go.Scatterpolar(r=vals, theta=cats, fill='toself',
                          line=dict(color=ACCENT), fillcolor=f'rgba(26,115,232,0.25)'))
    fig_radar.update_layout(**CHART_THEME, polar=dict(
        bgcolor='rgba(0,0,0,0)',
        radialaxis=dict(visible=True, gridcolor='#1e3a5a', color=MUTED),
        angularaxis=dict(gridcolor='#1e3a5a', color=TEXT),
    ), title='Performance Radar')

    return html.Div([
        html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(7,1fr)', 'gap': '12px', 'marginBottom': '20px'}, children=[
            stat_mini('Wins', wins, GREEN),
            stat_mini('Draws', draws, GOLD),
            stat_mini('Losses', losses, '#e74c3c'),
            stat_mini('Goals For', gf, GREEN),
            stat_mini('Goals Against', ga, '#e74c3c'),
            stat_mini('Avg Possession', f'{avg_poss}%', ACCENT),
            stat_mini('Pass Accuracy', f'{pass_acc}%', GOLD),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '2fr 1fr', 'gap': '16px'}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=fig_match, config={'displayModeBar': False})]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=fig_radar, config={'displayModeBar': False})]),
        ])
    ])


# ── HEAD-TO-HEAD TAB ──────────────────────────────────────────────────────────
def h2h_layout():
    return html.Div([
        html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'alignItems': 'center',
                        'flexWrap': 'wrap'}, children=[
            html.Div(style={'flex': 1, 'minWidth': '180px'}, children=[
                html.Label('Team A:', style={'fontWeight': '600', 'display': 'block', 'marginBottom': '6px'}),
                dcc.Dropdown(id='h2h-team1', options=[{'label': t.title(), 'value': t} for t in all_teams],
                             value='FRANCE', clearable=False,
                             style={'backgroundColor': BG, 'color': BG}),
            ]),
            html.Div('⚔️', style={'fontSize': '28px', 'paddingTop': '20px'}),
            html.Div(style={'flex': 1, 'minWidth': '180px'}, children=[
                html.Label('Team B:', style={'fontWeight': '600', 'display': 'block', 'marginBottom': '6px'}),
                dcc.Dropdown(id='h2h-team2', options=[{'label': t.title(), 'value': t} for t in all_teams],
                             value='ARGENTINA', clearable=False,
                             style={'backgroundColor': BG, 'color': BG}),
            ]),
        ]),
        html.Div(id='h2h-output'),
    ])


@app.callback(Output('h2h-output', 'children'),
              Input('h2h-team1', 'value'), Input('h2h-team2', 'value'))
def update_h2h(t1, t2):
    if t1 == t2:
        return html.P('Please select two different teams.', style={'color': MUTED})

    d1 = team_df[team_df['team'] == t1].copy()
    d2 = team_df[team_df['team'] == t2].copy()

    metrics = ['goals_for', 'shots', 'on_target', 'possession', 'passes_completed',
               'corners', 'yellow_cards', 'fouls', 'forced_turnovers']
    labels  = ['Goals', 'Total Shots', 'On-Target', 'Avg Possession %',
               'Passes Completed', 'Corners', 'Yellow Cards', 'Fouls', 'Forced Turnovers']

    v1 = [round(d1[m].mean(), 1) for m in metrics]
    v2 = [round(d2[m].mean(), 1) for m in metrics]

    fig = go.Figure()
    fig.add_trace(go.Bar(name=t1.title(), y=labels, x=[-v for v in v1], orientation='h',
                         marker_color=ACCENT, text=[str(v) for v in v1], textposition='outside'))
    fig.add_trace(go.Bar(name=t2.title(), y=labels, x=v2, orientation='h',
                         marker_color=GREEN, text=[str(v) for v in v2], textposition='outside'))
    fig.update_layout(**CHART_THEME, barmode='overlay',
                      title=f'{t1.title()} vs {t2.title()} — Avg Per Match Comparison',
                      xaxis=dict(tickvals=[], gridcolor='#1e3a5a'),
                      yaxis=dict(gridcolor='#1e3a5a', color=TEXT),
                      legend=dict(orientation='h', y=1.08))
    fig.add_vline(x=0, line_color=MUTED, line_width=1)

    return html.Div(style=CARD_STYLE, children=[
        dcc.Graph(figure=fig, config={'displayModeBar': False}, style={'height': '480px'})
    ])


# ── SCATTER EXPLORER TAB ──────────────────────────────────────────────────────
NUMERIC_METRICS = {
    'goals_for': 'Goals Scored',
    'goals_against': 'Goals Conceded',
    'shots': 'Total Shots',
    'on_target': 'On-Target Shots',
    'possession': 'Possession %',
    'passes': 'Total Passes',
    'passes_completed': 'Passes Completed',
    'yellow_cards': 'Yellow Cards',
    'fouls': 'Fouls',
    'corners': 'Corners',
    'forced_turnovers': 'Forced Turnovers',
}

def scatter_layout():
    opts = [{'label': v, 'value': k} for k, v in NUMERIC_METRICS.items()]
    return html.Div([
        html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px',
                        'alignItems': 'center', 'flexWrap': 'wrap'}, children=[
            html.Div(style={'flex': 1, 'minWidth': '160px'}, children=[
                html.Label('X-Axis:', style={'fontWeight': '600', 'display': 'block', 'marginBottom': '6px'}),
                dcc.Dropdown(id='sc-x', options=opts, value='possession', clearable=False,
                             style={'backgroundColor': BG, 'color': BG}),
            ]),
            html.Div(style={'flex': 1, 'minWidth': '160px'}, children=[
                html.Label('Y-Axis:', style={'fontWeight': '600', 'display': 'block', 'marginBottom': '6px'}),
                dcc.Dropdown(id='sc-y', options=opts, value='goals_for', clearable=False,
                             style={'backgroundColor': BG, 'color': BG}),
            ]),
            html.Div(style={'flex': 1, 'minWidth': '160px'}, children=[
                html.Label('Colour by:', style={'fontWeight': '600', 'display': 'block', 'marginBottom': '6px'}),
                dcc.Dropdown(id='sc-color', options=opts, value='shots', clearable=False,
                             style={'backgroundColor': BG, 'color': BG}),
            ]),
        ]),
        html.Div(style=CARD_STYLE, children=[dcc.Graph(id='sc-graph', config={'displayModeBar': True})]),
    ])


@app.callback(Output('sc-graph', 'figure'),
              Input('sc-x', 'value'), Input('sc-y', 'value'), Input('sc-color', 'value'))
def update_scatter(x, y, color):
    agg = team_df.groupby('team')[[x, y, color]].mean().reset_index()
    fig = px.scatter(agg, x=x, y=y, color=color, text='team',
                     color_continuous_scale='Plasma', size_max=20,
                     labels={x: NUMERIC_METRICS[x], y: NUMERIC_METRICS[y], color: NUMERIC_METRICS[color]},
                     title=f'{NUMERIC_METRICS[x]} vs {NUMERIC_METRICS[y]} (avg per match, coloured by {NUMERIC_METRICS[color]})')
    fig.update_traces(textposition='top center', marker=dict(size=12, line=dict(width=1, color='white')))
    fig.update_layout(**CHART_THEME, height=540,
                      xaxis=dict(gridcolor='#1e3a5a', color=MUTED),
                      yaxis=dict(gridcolor='#1e3a5a', color=MUTED))
    return fig


if __name__ == '__main__':
    app.run(debug=True, port=8050)
