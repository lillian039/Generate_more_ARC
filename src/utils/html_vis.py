def get_html_vis(description, img_num):
    str_body = ""
    for i in range(img_num):
        description_for_show = description[i].replace('\n', '\\n')
        description_for_show = description_for_show.replace('"', "`")
        if i != img_num - 1:
            img_str = f"""{{ src: '{i}_1_cat.png', desc: "{description_for_show}" }},\n"""
        else:
            img_str = f"""{{ src: '{i}_1_cat.png', desc: "{description_for_show}" }}"""
        str_body += img_str
    str_head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image and Text Slider</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            .container {
                display: flex;
                width: 80%;
                max-width: 800px;
                background-color: #fff;
                border: 1px solid #ccc;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .image-container {
                flex: 1;
                text-align: center;
                border-right: 1px solid #ccc;
            }
            .image-container img {
                max-width: 100%;
                height: auto;
            }
            .text-container {
                flex: 2;
                padding: 20px;
                overflow-wrap: break-word;
                word-wrap: break-word;
                hyphens: auto;
            }
            .buttons {
                display: flex;
                justify-content: space-between;
                padding: 10px;
                background-color: #fff;
                border-top: 1px solid #ccc;
            }
            .buttons button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            .buttons button:disabled {
                background-color: #ccc;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="image-container">
                <img id="image" src="image1.jpg" alt="Image">
            </div>
            <div class="text-container">
                <p id="description">This is the description for image 1.</p>
            </div>
        </div>
        <div class="buttons">
            <button id="prevBtn" onclick="prevImage()">Previous</button>
            <button id="nextBtn" onclick="nextImage()">Next</button>
        </div>

        <script>
            const images = [
    """
               
    html_body = """
            ];
            let currentIndex = 0;

            function updateContent() {
                const image = document.getElementById('image');
                const description = document.getElementById('description');
                image.src = images[currentIndex].src;
                description.textContent = images[currentIndex].desc;
                description.innerHTML = images[currentIndex].desc.replace(/\\n/g, '<br>');

                document.getElementById('prevBtn').disabled = currentIndex === 0;
                document.getElementById('nextBtn').disabled = currentIndex === images.length - 1;
            }

            function prevImage() {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateContent();
                }
            }

            function nextImage() {
                if (currentIndex < images.length - 1) {
                    currentIndex++;
                    updateContent();
                }
            }

            // Initial content update
            updateContent();
        </script>
    </body>
    </html>
    """
    return str_head + str_body + html_body