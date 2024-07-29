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
    <title>Image and Text Slider with Scoring</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
        }
        .container {
            display: flex;
            width: 80%;
            max-width: 800px;
            background-color: #fff;
            border: 1px solid #ccc;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .image-container {
            flex: 1;
            text-align: center;
            border-right: 1px solid #ccc;
            padding: 20px;
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
            width: 80%;
            max-width: 800px;
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
        .score-buttons {
            display: flex;
            justify-content: center;
            padding: 10px;
            background-color: #fff;
            border-top: 1px solid #ccc;
            width: 80%;
            max-width: 800px;
            margin-bottom: 20px;
        }
        .score-buttons button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            margin: 0 10px;
        }
        .comment-box {
            width: 80%;
            max-width: 800px;
            padding: 10px;
            margin-top: 10px;
            background-color: #fff;
            border: 1px solid #ccc;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .comment-box textarea {
            width: 100%;
            height: 80px;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .download-button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            margin-top: 10px;
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
    <div class="score-buttons">
        <button onclick="scorePage('bad')">Bad</button>
        <button onclick="scorePage('ok')">OK</button>
        <button onclick="scorePage('good')">Good</button>
    </div>
    <div class="comment-box">
        <textarea id="comment" placeholder="Enter your comment here..."></textarea>
    </div>
    <button class="download-button" onclick="downloadData()">Download Data</button>

    <script>
        const images = [
    """
               
    html_body = """
            ];
        let currentIndex = 0;
        const scores = new Map();

        function updateContent() {
            const image = document.getElementById('image');
            const description = document.getElementById('description');
            image.src = images[currentIndex].src;
            description.innerHTML = images[currentIndex].desc.replace(/\\n/g, '<br>');

            const currentScore = scores.get(currentIndex);
            document.getElementById('comment').value = currentScore ? currentScore.comment : '';

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

        function scorePage(score) {
            const comment = document.getElementById('comment').value;
            scores.set(currentIndex, { score, comment });
            alert(`Page ${currentIndex + 1} scored as ${score}`);
            if (currentIndex < images.length - 1) {
                nextImage();
            } else {
                alert('You have scored all pages.');
            }
        }

        function downloadData() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(Array.from(scores.entries()), null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "scores.json");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }

        // Initial content update
        updateContent();
    </script>
</body>
</html>
    """
    return str_head + str_body + html_body