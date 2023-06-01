import sys
import os
sys.path.append('hifi')
sys.path.append('tacotron2')
from hparams import create_hparams
import torch
import json
from model import Tacotron2
from audio_processing import griffin_lim
from text import text_to_sequence
from env import AttrDict
from meldataset import mel_spectrogram, MAX_WAV_VALUE
from models import Generator
from scipy.io.wavfile import write
#from denoiser import Denoiser
checkpoint_path = "tacotron2/humphery-300"
hparams = create_hparams()
hparams.sampling_rate = 22050
hparams.max_decoder_steps = 3000 # Max Duration
hparams.gate_threshold = 0.25 # Model must be 25% sure the clip is over before ending generation
model = Tacotron2(hparams)
state_dict = torch.load(checkpoint_path, map_location=torch.device("cpu"))['state_dict']
model.load_state_dict(state_dict)
model.eval()  # set the model to evaluation mode
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-t', type=str, help='txt')
parser.add_argument('-f', type=str, help='file')

# Parse the arguments
args = parser.parse_args()

# Access the arguments
p1 = args.t
p2 = args.f


def generate_wav(text, output):
    sequence = np.array(text_to_sequence(text, ['english_cleaners']))[None, :]
    sequence = torch.autograd.Variable(
        torch.from_numpy(sequence)).long()
    
    # Decode text input to get mel spectrogram
    model.eval()
    _, mel_outputs_postnet, _, _ = model.inference(sequence)
    
    # Load HiFi-GAN generator
    hifi_gan_config = AttrDict(json.load(open("hifi/config_v1.json")))
    generator = Generator(hifi_gan_config)
    state_dict_g = torch.load('hifimodel_config_v1', map_location=torch.device('cpu'))
    generator.load_state_dict(state_dict_g['generator'])
    generator.eval()
    
    # Convert mel spectrogram to waveform using HiFi-GAN
    with torch.no_grad():
        mel = mel_outputs_postnet.squeeze(0)
        if len(mel.shape) == 2:
            mel = mel.unsqueeze(0)
        audio = generator(mel).squeeze()
        audio = audio * MAX_WAV_VALUE
        audio = audio.squeeze().numpy().astype('int16')
    
    # Save output waveform to .wav file
    file_name = "voice_output/" + str(output) + ".wav"
    write(file_name, hparams.sampling_rate, audio)
if p1:
    output = 1
    generate_wav(p1,output)

elif p2:
    with open(p2, 'r') as file:
        for i,line in enumerate(file):
            generate_wav(line,i)

else:
    generate_wav("yes,prime minister.","sample")
