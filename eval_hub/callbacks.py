# Callback for user authentication
@app.callback(
        Output('user-authentication-section', 'children'),
        [Input('url', 'pathname')]
)
def display_page(pathname):
    # Simulate user login page
    return html.Div([
        html.H2('User Login'),
        dcc.Input(placeholder='Username', type='text', id='username'),
        dcc.Input(placeholder='Password', type='password', id='password'),
        html.Button('Login', id='login-button'),
        html.Div(id='login-status')
    ])


# Callback to update the comments section
@app.callback(
        Output('comments-section', 'children'),
        [Input({'type': 'show-comments', 'index': ALL}, 'n_clicks')],
        [State({'type': 'show-comments', 'index': ALL}, 'id')],
        prevent_initial_call=True
)
def update_comments(n_clicks, ids):
    if not any(n_clicks):
        return "Select a plot to see comments."

    # Find which button was clicked
    button_id = [id['index'] for n, id in zip(n_clicks, ids) if n > 0][0]

    # Fetch comments for the selected plot
    comments = comments_db.get(button_id, [])

    return html.Div([
        html.Ul([html.Li(comment) for comment in comments]),
        dcc.Textarea(id='new-comment', style={'width': '100%', 'height': '100px'}),
        html.Button('Submit Comment', id='submit-comment', n_clicks=0,
                    n_clicks_timestamp=0,
                    style={'display': 'block', 'margin': 'auto'}),
        html.Div(id={'type': 'comment-submission-status', 'index': button_id})
    ])


# Callback for comment submission
@app.callback(
        Output({'type': 'comment-submission-status', 'index': MATCH}, 'children'),
        [Input('submit-comment', 'n_clicks')],
        [State('new-comment', 'value'), State({'type': 'show-comments', 'index': MATCH}, 'id')],
        prevent_initial_call=True
)
def submit_comment(n_clicks, comment, id):
    if comment:
        plot_id = id['index']
        comments_db.setdefault(plot_id, []).append(comment)
        return "Comment submitted!"
    return "Please enter a comment."
