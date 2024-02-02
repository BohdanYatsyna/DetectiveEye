# DetectiveEye 
___
#### API for detecting objects on video and returning human-readable results

## 🔧 Technologies used:
___
* [X] FastAPI
* [X] PostgreSQL
* [X] OpenCV
* [X] Detectron2
* [X] Redis
* [X] Celery
* [X] Docker
___
# 🕶 Project Architecture
![project_architecture](samples_for_readme/project_architecture.png)


### 💾 Installation:
___
#### 1. Clone the repository:
```shell
git clone https://github.com/BohdanYatsyna/DetectiveEye.git
cd DetectiveEye
```
#### 2. Create and activate virtual environment with requirements install:
🖥 Windows:
```shell
python -m venv venv
venv\Scripts\activate
```
💻 Linux/MacOS:
```shell
python -m venv venv
source venv/bin/activate
```
#### 3. 🗝 Set up environment variables (using .env):
- Create an empty .env file in the root folder of the project.
- Copy the entire content of the .env.sample to your .env file.
- Modify the placeholders in the .env file with your preferable environment variables.
- Modify file ./alembic.ini line 63 ('sqlalchemy.url = postgresql://POSTGRES:PASSWORD@db/postgres') in accordance with .env variables to pass db migrations with ease.

#### 4. 🐳 Run it with DOCKER:
- DOCKER should be installed and opened.
```shell
docker-compose up --build
```
- And open in your browser "http://127.0.0.1:8000/docs/"

#### 🗝 ENDPOINTS:  
#### Note that only authenticated users can detect objects on video and see own results

- **User creating** - send a POST request to /register/  
- **Login** - send a POST request to /login/
- **Logout** - send a POST request to /logout/

- **Start objects detection by uploading video file** - send a POST request to /detect_objects/  
- **See all detection result** - send a GET request to /detection_results/
- **See single detection result by {task_id}** - send a GET request /detection_results/{task_id}


#### 🗝 Important note.
#### For using GPU (CUDA support required) with Detectron2 it is needed to update:
-         In ./objects_detection/detector.py self.configurations.MODEL.DEVICE set to "gpu"
-         Replace in ./Dockerfile "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu" with "pip3 install torch torchvision torchaudio"
-         self.configurations.MODEL.DEVICE set to "gpu" in ./objects_detection/detector.py

# 🕶 DEMO
### Documentation with all endpoints:
![sample_DOCUMENTATION](samples_for_readme/sample_DOCUMENTATION.png)
