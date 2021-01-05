from typing import Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return """
        # 📅 9 décembre
        ## Stand up
        ## To do
        - [ ] Enlever les hard coded creds
        - [x] Bug datepicker SDM
        - [x] Aide Marc data export
        - [x] Générer les fichiers pour l’injection
        - [x] Bugs données de vols per flight ACA
        ## Notes

        #work/smartflows/journal/2020/12
    """
