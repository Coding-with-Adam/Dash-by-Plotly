# App Deploy to Pythonanywhere

1. Open an account on [Pythonanywhere](https://www.pythonanywhere.com/)
2. **Create web app**: Dashboard → Open "Web: Tab → Add a new web app
    - “Next” button → Flask → 3.10 → default path is ok
3. **Install necessary libraries**: Dashboard → Bash (in New Console section)
    - My personal app uses Dash and pandas and dash ag grid, so:
      - `pip install pandas`
      - `pip install dash==2.17.0` or just `pip instal dash`, but I want the latest version 
      - `pip install dash-ag-grid`
4. **Upload files**: “Files” tab → mysite → delete flask_app.py
    - Click the Upload-a-File button to add your app file and csv/excel sheet
5. **Modify how the app reads the data**: “Files” tab → mysite → [app_name].py
    - `df = pd.read_csv('/home/charmingdata2/mysite/space-mission-data.csv')`
6. **Edit WSGI file**: “Web” tab → WSGI configuration file
    - Remove last line and insert two lines instead: 
      - `from [app_name_without_.py] import app`
      - `application = app.server`
7. **Reload app**: “Web” tab → click green Reload button
