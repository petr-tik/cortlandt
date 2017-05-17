#! /usr/bin/env python3

import pygsheets

G_SHEETS_ID = "1MPAu6ZwIZ_0ABh4jCfFbmXEhwyCkfCgYzzj44m_CtsQ"

gc = pygsheets.authorize(service_file='service_creds.json')

sht1 = gc.open_by_key(G_SHEETS_ID)
wks = sht1.worksheet_by_title("Sheet1")
