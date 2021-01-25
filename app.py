from flask import Flask, render_template, request, redirect
from flask_scss import Scss
import requests 
import os

app = Flask(__name__)
Scss(app, static_dir='static/css', asset_dir='assets')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def get_homepage():
  # get product listings from API
  try:
    url = 'http://localhost:5001/products'
    response = requests.get(url)
  except Exception as e:
    # display error page if connection to API failed
    return render_template('error_page.html', message='Internal Server Error', status_code=500)

  # display error if API response status code was not 2xx
  if response.status_code < 200 or response.status_code >= 300:
    return render_template('error_page.html', message='Internal Server Error', status_code=500)

  # display homepage with products
  products = response.json()
  return render_template('homepage.html', products=products)

@app.route('/products/add')
def get_add_product():
  # display add product page
  return render_template('add_product.html')

@app.route('/products/<id>')
def get_product_details(id):
  try:
    # get product details from API
    url = 'http://localhost:5001/products/' + id
    response = requests.get(url)
  except Exception as e:
    # display error page if connection to API failed
    return render_template('error_page.html', message='Internal Server Error', status_code=500)

  # display error if API response status code was not 2xx
  if response.status_code < 200 or response.status_code >= 300:
    if response.status_code == 404:
      status_code = 404
      error_message = 'Page Not Found'
    else:
      status_code = 500
      error_message = 'Internal Server Error'
    return render_template('error_page.html', message=error_message, status_code=status_code)

  # display product detail page
  product = response.json()
  return render_template('product_details.html', product=product)

@app.route('/products/add', methods=['POST'])
def post_add_product():
  # get file from request
  f = request.files['image']

  # get file extension from filename
  if f.filename.rfind('.') != -1:
      extension = f.filename[f.filename.rfind('.'):]
  else:
      extension = ''

  # use API to save product
  try:
    url = 'http://localhost:5001/products'
    data = {
      'name': request.form['name'],
      'description': request.form['description'],
      'price': request.form['price'],
      'imageExtension': extension
    }
    response = requests.post(url, json=data)
  except Exception as e:
    # display error page if connection to API failed
    return render_template('error_page.html', message='Internal Server Error', status_code=500)

  # display error if API response status code was not 2xx
  if response.status_code < 200 or response.status_code >= 300:
    return render_template('error_page.html', message='Internal Server Error', status_code=500)
  
  # get data from response
  new_product = response.json()
  
  # save image to static/images folder
  f.save(f'./static/images/product{new_product["id"]}{extension}')

  # redirect to homepage
  return redirect('/')

@app.route('/products/<id>/delete')
def get_delete_product(id):
  # use API to delete product
  try:
    url = 'http://localhost:5001/products/' + id
    response = requests.delete(url)
    deleted_product = response.json()
  except Exception as e:
    # display error if API response status code was not 2xx
    if response.status_code < 200 or response.status_code >= 300:
      if response.status_code == 404:
        status_code = 404
        error_message = 'Page Not Found'
      else:
        status_code = 500
        error_message = 'Internal Server Error'
      return render_template('error_page.html', message=error_message, status_code=status_code)

  # delete product image
  try:
    os.remove(f'./static/images/product{id}{deleted_product["imageExtension"]}')
  except Exception as e:
    pass

  # redirect to homepage
  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
