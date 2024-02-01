# DetectiveEye 
___
#### API for detecting objects on video and return human readable results

## 🔧 Technologies used:
___
* [X] FastAPI
* [X] PostgreSQL
* [X] OpenCV
* [X] Detectron2
* [X] Redis
* [X] Celery
* [X] Docker

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

#### 4. 🐳 Run it with DOCKER:
- DOCKER should be installed and opened.
```shell
docker-compose up --build
```
- And open in your browser "http://127.0.0.1:8000/docs/"


# 🕶 DEMO
### Documentation with all endpoints:
![sample_DOCUMENTATION](samples/sample_DOCUMENTATION.PNG)
