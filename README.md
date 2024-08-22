
# AI Search In E-Commerce Website

This example shows a Marqo image search application that performs multimodel search with weighted queries. The whole process is intended to be executed locally by deploying the Marqo docker image on your computer. All data is downloaded from S3 by Marqo and indexing will be done on the go when you start the application. The model used for the application is ```open_clip/ViT-B-32/laion2b_s34b_b79k```, but Marqo can also support hundreds of other open source embedding models

(Edit `.env.local` to add more images).

# Running Marqo

The steps and command for different devices are provided below.

### Running application
```
docker run --name marqo -p 8882:8882 marqoai/marqo
```

# Installation
### Make virutal environment
```
python -m venv venv
```
### Activate the virtual environment
Linux/Mac:
```
source venv/bin/activate
```
### Install requirements
```
pip install -r requirements.txt
```
# Indexing the Application
```
python3 index_data.py
```

# Starting the Application
```
python3 app.py
```