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


def get_html_vis_double(description, json_record, img_num):
    str_body = ""
    for i in range(img_num):
        if i in description[0] and i in description[1]:
            description_for_show = (description[0][i] + description[1][i]).replace('\n', '\\n')
            code = ("#CODE 1\n\n" + json_record[0][i]['generator'] + "\n\n#CODE 2\n\n" + json_record[1][i]['generator']).replace('\n', '\\n')
        elif i in description[0]:
            description_for_show = description[0][i].replace('\n', '\\n')
            code = ("#CODE 1\n\n" + json_record[0][i]['generator']).replace('\n', '\\n')
        elif i in description[1]:
            description_for_show = description[1][i].replace('\n', '\\n')
            code = ("#CODE 2\n\n" + json_record[1][i]['generator']).replace('\n', '\\n')

        description_for_show = description_for_show.replace('"', "`")
        # code = ("#CODE 1\n\n" + json_record[0][i]['generator'] + "\n\n#CODE 2\n\n" + json_record[1][i]['generator']).replace('\n', '\\n')
        code = code.replace('"',"\'")
        if i != img_num - 1:
            img_str = f"""{{src1: '{i}_1_cat.png', desc1: "{description_for_show}", src2: '{i}_2_cat.png', desc2: "{code}"}},\n"""
        else:
            img_str = f"""{{src1: '{i}_1_cat.png', desc1: "{description_for_show}", src2: '{i}_2_cat.png', desc2: "{code}"}}"""
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
            max-width: 1200px;
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
            flex: 1;
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
            max-width: 1200px;
        }
        .code-container {
            flex: 1;
            padding: 20px;
            background-color: #f5f5f5;
            border-left: 1px solid #ccc;
            overflow-x: auto;
        }
        .code-container code {
            display: block;
            white-space: pre-wrap;
            background-color: #f5f5f5;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-family: 'Courier New', Courier, monospace;
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
        .choice-buttons {
            display: flex;
            justify-content: center;
            padding: 10px;
            background-color: #fff;
            border-top: 1px solid #ccc;
            width: 80%;
            max-width: 1200px;
        }
        .choice-buttons button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 5px;
            margin: 0 10px;
        }
        .score-buttons {
            display: flex;
            justify-content: center;
            padding: 10px;
            background-color: #fff;
            border-top: 1px solid #ccc;
            width: 80%;
            max-width: 1200px;
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
            max-width: 1200px;
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
    <div class="buttons">
        <button id="prevBtn" onclick="prevImage()">Previous</button>
        <button id="nextBtn" onclick="nextImage()">Next</button>
    </div>
    <div class="choice-buttons">
        <button onclick="chooseImage('left')">Left</button>
        <button onclick="chooseImage('right')">Right</button>
        <button onclick="chooseImage('both')">Both</button>
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
    <div class="container">
        <div class="image-container">
            <img id="image1" src="image1.jpg" alt="Image 1">
        </div>
        <div class="image-container">
            <img id="image2" src="image2.jpg" alt="Image 2">
        </div>
        <div class="text-container">
            <p id="description1">This is the description for image 1.</p>
        </div>
        <div class="code-container">
            <code id="description2"># This is the Python code for image 2.</code>
        </div>
    </div>
    <script>
        const images = [
"""

    str_tail = """
        ];
        let currentIndex = 0;
        const results = [];

        function updateContent() {
            const image1 = document.getElementById('image1');
            const image2 = document.getElementById('image2');
            const description1 = document.getElementById('description1');
            const description2 = document.getElementById('description2');
            image1.src = images[currentIndex].src1;
            image2.src = images[currentIndex].src2;
            description1.innerHTML = images[currentIndex].desc1.replace(/\\n/g, '<br>');
            description2.innerHTML = images[currentIndex].desc2.replace(/\\n/g, '<br>');

            const currentResult = results[currentIndex] || {};
            document.getElementById('comment').value = currentResult.comment || '';

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

        function chooseImage(choice) {
            if (!results[currentIndex]) {
                results[currentIndex] = {};
            }
            results[currentIndex].choice = choice;
            alert(`Image ${choice} chosen for page ${currentIndex + 1}`);
        }

        function scorePage(score) {
            const comment = document.getElementById('comment').value;
            if (!results[currentIndex]) {
                results[currentIndex] = {};
            }
            results[currentIndex].score = score;
            results[currentIndex].comment = comment;
            alert(`Page ${currentIndex + 1} scored as ${score}`);
            if (currentIndex < images.length - 1) {
                nextImage();
            } else {
                alert('You have scored all pages.');
            }
        }

        function downloadData() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(results, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "results.json");
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
    return str_head + str_body + str_tail