# 이미지 받고 텍스트로 변환해서 이미지 생성하기

from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from diffusers import StableDiffusionPipeline
import torch
import requests
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

app = Flask(__name__)

def setup_model():
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return model, feature_extractor, tokenizer, device

def predict_step(image_paths, model, feature_extractor, tokenizer, device):
    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    images = []
    for image_path in image_paths:
        i_image = Image.open(image_path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")

        images.append(i_image)

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    
    return preds
 
@app.route('/submit', methods=['POST'])
def submit():

    f = request.files['file']
    file_path = 'D:/stable/' + secure_filename(f.filename)
    f.save(file_path)

    model, feature_extractor, tokenizer, device = setup_model()
    text=predict_step([file_path], model, feature_extractor, tokenizer, device)
    print(text)
    
    model_id = "artificialguybr/freedom"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    prompt = "cute cartoon sticker " + ','.join(text)
    image = pipe(prompt).images[0]    
    image.save("D:/stable/out/0001.png")
    print(prompt)

    model_id=0
    pipe=0

    model_id2 = "runwayml/stable-diffusion-v1-5"
    pipe2 = StableDiffusionPipeline.from_pretrained(model_id2, torch_dtype=torch.float16)
    pipe2 = pipe2.to("cuda")

    image = pipe2(prompt).images[0]    
    image.save("D:/stable/out/0002.png")

    model_id2=0
    pipe2=0

    model_id3 = "stablediffusionapi/anything-v5"
    pipe3 = StableDiffusionPipeline.from_pretrained(model_id3, torch_dtype=torch.float16)
    pipe3 = pipe3.to("cuda")
       
    image = pipe3(prompt).images[0]    
    image.save("D:/stable/out/0003.png")

    file_paths = ['D:/stable/out/0001.png', 'D:/stable/out/0002.png', 'D:/stable/out/0003.png']
    files = [('files', (open(file, 'rb'))) for file in file_paths]

    # POST 요청을 보냅니다.
    res = requests.post('http://192.168.0.65:8080/test/multipart3', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


