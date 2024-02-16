# NBIB-TO-BIB

The objective of the api is to simply convert .nbib files to .bib using python and fastAPI

#### 1ª Cloning repository
```bash
git clone https://github.com/Escritha/nbib-to-bib.git
cd nbib-to-bib
```

#### 2ª Creating virtual environment and installing packages
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### 3ª Running the api
```bash
uvicorn main:app --reload
```

### Endpoints

#### POST

`/upload`

Receives as a parameter one or several files with the .nbib extension and converts it to .bib

#### GET

`/download`

Rescue the converted .bieber content

## License

This project is licensed under MIT.
