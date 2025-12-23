# AgeEst

Dash/Plotly web application for deploying machine learning models for skeletal age-at-death estimation.

- Live demo: https://ageest.onrender.com/
- Paper (FSI: Reports, 2023): https://doi.org/10.1016/j.fsir.2023.100317
- Model-training notebooks: https://github.com/cconsta1/age-estimation-notebook

## What this repository is

This repository contains a self-contained Dash web app ([app.py](app.py)) plus pre-trained model artifacts ([models/](models/)) that:

- Accepts standard skeletal scoring inputs from commonly used osteological methods.
- Runs **two ML model families** per method:
	- **Classification** into three broad adult age groups.
	- **Regression** age prediction (years) with an uncertainty term derived from the model RMSE.
- Displays the predictions in a simple UI suitable for interactive use.

The ML models shipped here are trained using the companion notebook repository and then exported as serialized scikit-learn objects (`.dat`) alongside human-readable performance summaries (`.txt`).

Background (from the paper): the models were developed using a contemporary documented skeletal collection from Greece (Athens Collection; 140 individuals: 81 males, 59 females) and standard scoring procedures for widely used pelvic and cranial age markers. A key observed limitation is that, while young and old adults are often classified well, **middle-aged individuals can be misclassified at higher rates**, reflecting both marker and model biases.

## Output definitions

The app reports two outputs:

- **Classification**: 3 adult age groups
	- class 0: 18–34
	- class 1: 35–49
	- class 2: 50+
  
	It also shows the predicted **class probabilities**.

- **Regression**: a point prediction (years) with an uncertainty term shown as $\pm\mathrm{RMSE}$.
	- RMSE values are parsed from the corresponding `models/*_regression_right_<method>.txt` files.


## Supported input methods (left sidebar)

In the UI left sidebar you can select one of the following variable sets. Each selection maps to a matching pair of classification + regression models.

These correspond to commonly adopted markers based on the morphology of the pubic symphysis, iliac auricular surface, and cranial sutures, as described in the associated publication.

- **Brooks & Suchey 1990 (BS)**
	- Input: `Right Phase Suchey` (1–6)

- **Meindl & Lovejoy 1985 (ML)**
	- Inputs (0–3):
		- `Right 1-midlamdoid`, `2-lambda`, `3-obelion`, `4-anterior sagital`, `5-bregma`,
			`Right 6-midcoronal`, `Right 7-pterion`, `Right 8-sphenofrontal`,
			`Right 9-inferior sphenotemporal`, `Right 10-superior sphenotemporal`

- **Lovejoy et al. 1995 (L)**
	- Input: `Right Phase` (1–8)

- **Buckberry & Chamberlain 2002 (BC)**
	- Inputs (1–5):
		- `Right Transverse organization`, `Right Surface texture`, `Right Microposity`,
			`Right Macroporositty`, `Right Apical changes`

- **Combined variable sets**
	- **BS & L** (2 inputs)
	- **BS & BC** (6 inputs)
	- **All (BS & ML & L & BC)** (17 inputs)

## Repository contents

- [app.py](app.py): Dash application (UI + inference logic)
- [models/](models/): model artifacts and their metrics
	- `classification_right_<method>.dat`: scikit-learn classification model
	- `ann_classification_right_<method>.dat`: scikit-learn MLP-based classifier
	- `regression_right_<method>.dat`: scikit-learn regression model
	- `ann_regression_right_<method>.dat`: scikit-learn MLP-based regressor
	- `*_right_<method>.txt`: training/evaluation summaries (RMSE/MAE/R², etc.)
- [setup.yml](setup.yml): pinned conda environment used for the Dash app
- [requirements.txt](requirements.txt): pip requirements (used by Dockerfile)
- [Dockerfile](Dockerfile): container build/run configuration (Gunicorn)

What is `setup.yml`?

`setup.yml` is a Conda environment specification that pins the major runtime versions used to develop and test this app (for example `python=3.10.8` and specific versions of `numpy`, `pandas`, `plotly`, `dash`, and `scikit-learn`). Using `conda env create -f setup.yml` will create an environment that closely matches the developer environment and is the recommended way to reproduce the runtime used during development.

## Run locally (recommended: conda)

The pinned environment in [setup.yml](setup.yml) is the most reliable way to match the versions used when this app was packaged.

```bash
conda env create -f setup.yml
conda activate env_dash
python app.py
```

Then open `http://127.0.0.1:8050/`.

## Run with pip

If you prefer a plain pip environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Note: [setup.yml](setup.yml) pins versions; `requirements.txt` is intentionally looser.

## Run with Docker

Build:

```bash
docker build -t ageest .
```

Run:

```bash
docker run --rm -p 8050:8050 ageest
```

Open `http://127.0.0.1:8050/`.

The container uses Gunicorn to serve the Dash app via `app:server`.

## Deployment notes (Render / Gunicorn)

The Dash app exposes a WSGI server object as `server = app.server` in [app.py](app.py). For most PaaS providers you can run it with:

```bash
gunicorn -b 0.0.0.0:$PORT app:server
```

If your platform uses a fixed port (e.g., 8050), replace `$PORT` accordingly.

## Security note about model files

The model artifacts in [models/](models/) are Python pickles (`.dat`) loaded with `pickle.load(...)`. As with any pickle, **do not load untrusted files**. Only run this app with model artifacts you trust and that come from a trusted source.

## Citation

If you use AgeEst in academic work, please cite:

Constantinou, C., Chovalopoulou, M.-E., & Nikita, E. (2023). *AgeEst: an open access web application for skeletal age-at-death estimation employing machine learning*. Forensic Science International: Reports, 7, 100317. https://doi.org/10.1016/j.fsir.2023.100317

The article is open access under a Creative Commons license (see the publisher page for the specific license text).

This repository also includes a citation metadata file: [CITATION.cff](CITATION.cff).

BibTeX:

```bibtex
@article{constantinou2023ageest,
	title={AgeEst: an open access web application for skeletal age-at-death estimation employing machine learning},
	author={Constantinou, Chrysovalantis and Chovalopoulou, Maria-Eleni and Nikita, Efthymia},
	journal={Forensic Science International: Reports},
	volume={7},
	pages={100317},
	year={2023},
	publisher={Elsevier},
	doi={10.1016/j.fsir.2023.100317}
}
```

## Contributing data

To improve generalizability (and to help address issues like age mimicry and middle-age misclassification), the authors invite colleagues to share raw data from other skeletal collections so the training dataset can be expanded. If you have relevant datasets and are interested in collaborating, please open an issue describing what variables you have recorded and under what sharing constraints.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
