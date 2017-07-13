import boto3
from chalice import Chalice, NotFoundError, Response
import requests


app = Chalice(app_name='chalice-app')
app.debug = True # disable for prod

BUCKET = 'soft-brush-images'

index_html= """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<body>

<body>
    <form method="post" enctype="multipart/form-data" action="upload">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>

</body>
</html>"""

image_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<body>

<body>
    <img src="https://s3.us-east-2.amazonaws.com/soft-brush-images/test.png">
</body>

</body>
</html>"""


@app.route('/')
def index():
    return {'status': 'ok'}


@app.route('/recipe/{food}', methods=['GET'])
def recipe(food):
    """Connect to recipe puppy api, use keyword food to find recipes"""
    response = requests.get("http://www.recipepuppy.com/api/?q={}&p=1".format(food))
    response.raise_for_status()
    data = response.json()
    output = """<html><head>
          <title>Recipes</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
          </head><body><h3>Here are the search results for: {}</h3>""".format(food)
    for number, recipe in enumerate(data['results']):
        output += '<br><br><a href={0}><img src="{1}" alt="{3}"><br>{2}. {3}</a>'.format(
            recipe['href'], recipe['thumbnail'], number+1,  recipe['title'])
    output += '</body></html>'
    return Response(body=output,
                    status_code=200,
                    headers={'Content-Type': 'text/html'})

# http://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-post-example.html
@app.route('/upload', methods=['GET'])
def get():
    """show form to upload image file"""
    return Response(body=index_html,
                    status_code=200,
                    headers={'Content-Type': 'text/html'})

"""
file_name = 'test.png'
with open(file_name, 'rb') as f:
    r = requests.post('http://localhost:8000/upload', files={file_name: f})
"""
@app.route('/upload', methods=['POST'], content_types=['multipart/form-data'])
def post():
    """upload image file to boto s3"""
    S3 = boto3.resource('s3')
    data = app.current_request.raw_body
    S3.Bucket(BUCKET).put_object(Key='test.png',
                                 Body=data,
                                 ACL='public-read',
                                 ContentType='image/png')
    return Response(body=image_html,
                    status_code=200,
                    headers={'Content-Type': 'text/html'})
