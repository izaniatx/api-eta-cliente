from fastapi import FastAPI

app = FastAPI(title="Zereginen APIa")

from fastapi.middleware.cors import CORSMiddleware

## ---------------- KOMANDOA: uvicorn lehen-api:app --host 0.0.0.0 --reload ------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # para clase vale; en producción pon dominios concretos
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hasiera():
    return {"mezua": "Nire apiFast-eko adibidea!"}

@app.get("/agurra")
def hasiera():
    return {"mezua": "Kaixo , Izani naiz BOMBOCLAT!"}

@app.get("/kurtsoa")
def hasiera():
    return {"mezua": "AABD - Adimen Atxega."}

@app.get("/agurra/{izena}")
def agurra(izena):
    return {"mezua": f"Kaixo, {izena}"}

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier 


# /score -> KNN batazbesteko scorea cv=5ekin


iris = load_iris()

X = iris.data
y = iris.target

emaitza = cross_val_score(KNeighborsClassifier(n_neighbors=7), X, y, cv=5, scoring="accuracy")



@app.get("/score")
def score():
    return {"score": emaitza.mean()}


modelo = KNeighborsClassifier(n_neighbors=3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo.fit(X_train, y_train)


@app.get("/predict/{largo_sepalo}/{ancho_sepalo}/{largo_petalo}/{ancho_petalo}")
def predict(largo_sepalo:float, ancho_sepalo:float, largo_petalo:float, ancho_petalo:float):

    prediccion = modelo.predict([[largo_sepalo, 
                                ancho_sepalo, 
                                largo_petalo, 
                                ancho_petalo]])


    return {"erantzuna": f"{iris.target_names[prediccion]}"}

# zeregina

from zeregina import Zeregina, ZereginBerria

zereginak: dict[int, Zeregina] = {} # memorian
hurrengo_id = 1

from fastapi import FastAPI , HTTPException , Query

@app.get("/zereginak/kopurua")
def kopurua():
    return{"kopurua" : f"{len(zereginak)}"}

@app.get("/zereginak", response_model=list[Zeregina])
def zerrenda(egina: bool | None = None, muga: int = Query(10, ge=1, le=100)):
    emaitza = list(zereginak.values())
    if egina is not None:
        emaitza = [z for z in emaitza if z.egina == egina]

    return emaitza[:muga]


@app.get("/zereginak/{zeregin_id}", response_model=Zeregina)
def bat_lortu(zeregin_id: int):
    if zeregin_id not in zereginak:
        raise HTTPException(status_code=404,
        detail="Zeregina ez da aurkitu")
    
    return zereginak[zeregin_id]

@app.post("/zereginak", response_model=Zeregina , status_code=201)
def sortu(berria: ZereginBerria):
    global hurrengo_id
    zeregina = Zeregina(id=hurrengo_id , **berria.model_dump())
    zereginak[zeregina.id] = zeregina
    hurrengo_id += 1

    return zeregina

@app.put("/zereginak/{zeregin_id}", response_model=Zeregina)
def ordezkatu(zeregin_id: int, datuak: ZereginBerria):
    if zeregin_id not in zereginak:
        raise HTTPException(status_code=404, detail="Ez da aurkitu")
    zereginak[zeregin_id] = Zeregina(id=zeregin_id , **datuak.model_dump())

    return zereginak[zeregin_id]

@app.delete("/zereginak/{zeregin_id}", status_code=204)
def ezabatu(zeregin_id: int):
    if zeregin_id not in zereginak:
        raise HTTPException(status_code=404, detail="Ez da aurkitu")
    del zereginak[zeregin_id]

