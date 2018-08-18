from app import app
import os

from model.img2seq import Img2SeqModel
from model.utils.general import Config, run
from model.utils.text import Vocab

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
MODEL_FOLDER = os.path.join(APP_ROOT, 'full')
app.config['MODEL_FOLDER'] = MODEL_FOLDER

print("loading model ...")

config_vocab = Config(os.path.join(app.config['MODEL_FOLDER'], "vocab.json"))
config_model = Config(os.path.join(app.config['MODEL_FOLDER'], "model.json"))
vocab = Vocab(config_vocab)

model = Img2SeqModel(config_model, app.config['MODEL_FOLDER'], vocab)
model.build_pred()
model.restore_session(os.path.join(app.config['MODEL_FOLDER'], "model.weights/")) 
