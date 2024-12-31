from flask import Flask, request, render_template, send_file
from flask_cors import CORS  # Import CORS
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
# CORS(app,origins=["https://frontend-j1h26ux4r-dhwani-jains-projects.vercel.app/"]) 
CORS(app) 

# @app.route('/')
# def home():
#     return render_template('form.html')  # Use the HTML form above

# @app.route('/generate-ticket', methods=['POST'])
# def generate_ticket():
#     name = request.form['name']
    
#     # Open existing ticket template
#     img = Image.open('ticket_template.png')  # Ensure the template image is in the project directory
#     d = ImageDraw.Draw(img)
#     font = ImageFont.truetype('bebas_neue.ttf', 90)  # Use Bebas Neue font with 30px size
#     d.text((540, 190), f"{name}", fill=(1, 1, 1), font=font)

#     # Save ticket to a BytesIO stream
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)

#     return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"{name}_ticket.png")
@app.route('/generate-ticket', methods=['POST'])
def generate_ticket():
    name = request.form['name']
    
    # Open existing ticket template
    img = Image.open('ticket_template.png')
    d = ImageDraw.Draw(img)
    
    # Create a temporary image for the text
    font = ImageFont.truetype('bebas_neue.ttf', 160)  # Use Bebas Neue font with 30px size
    text_img = Image.new('RGBA', img.size, (255, 255, 255, 0))  # Transparent background
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((180, 560), f"{name}", fill=(255, 255, 255, 255), font=font)

    # Rotate the text image
    rotated_text_img = text_img.rotate(10, resample=Image.BICUBIC, center=(140, 90))  # Tilt by 10 degrees

    # Composite the rotated text onto the original ticket
    img = Image.alpha_composite(img.convert('RGBA'), rotated_text_img)

    # Save ticket to a BytesIO stream
    buffer = BytesIO()
    img.convert('RGB').save(buffer, format="PNG")  # Convert to 'RGB' to save as PNG
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"{name}_ticket.png")

if __name__ == '__main__':
    app.run(debug=True)