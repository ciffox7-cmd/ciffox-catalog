from typing import List, Dict
import csv
from jinja2 import Template
import os

_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>Product Catalog - Editable</title>
<style>
body { font-family: Arial, sans-serif; margin: 24px; background-color: #f5f5f5; }
.header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
#q { width: 360px; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
.controls { margin: 10px 0; }
.btn { background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-right: 10px; }
.btn:hover { background: #0056b3; }
.btn-success { background: #28a745; }
.btn-danger { background: #dc3545; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card img { width: 100%; height: auto; border-radius: 6px; margin-bottom: 10px; }
.card h3 { margin: 0 0 10px 0; color: #333; }
.meta { font-size: 12px; color: #555; margin: 5px 0; }
.matched { color: #070; font-weight: bold; }
.edit-btn { background: #ffc107; color: #212529; }
.edit-btn:hover { background: #e0a800; }
.editable { border: 1px solid #ddd; padding: 4px; border-radius: 3px; background: #f8f9fa; }
.editable:focus { outline: 2px solid #007bff; background: white; }
.modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
.modal-content { background-color: white; margin: 5% auto; padding: 20px; border-radius: 8px; width: 80%; max-width: 500px; }
.close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
.close:hover { color: black; }
.form-group { margin: 10px 0; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
.form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
</style>
</head>
<body>
<div class="header">
  <h1>Product Catalog - Editable</h1>
  <input id="q" type="search" placeholder="Search products..." oninput="f()" />
  <div class="controls">
    <button class="btn btn-success" onclick="showAddModal()">Add New Product</button>
    <button class="btn" onclick="exportData()">Export Data</button>
    <button class="btn" onclick="importData()">Import Data</button>
  </div>
  <p><span id="count"></span></p>
</div>

<div class="grid" id="grid"></div>

<!-- Add/Edit Product Modal -->
<div id="productModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeModal()">&times;</span>
    <h2 id="modalTitle">Add New Product</h2>
    <form id="productForm">
      <div class="form-group">
        <label for="editArticle">Article:</label>
        <input type="text" id="editArticle" name="article" />
      </div>
      <div class="form-group">
        <label for="editColour">Colour:</label>
        <input type="text" id="editColour" name="colour" />
      </div>
      <div class="form-group">
        <label for="editSize">Size:</label>
        <input type="text" id="editSize" name="size" />
      </div>
      <div class="form-group">
        <label for="editPair">Pair:</label>
        <input type="text" id="editPair" name="pair" />
      </div>
      <div class="form-group">
        <label for="editDescription">Description:</label>
        <input type="text" id="editDescription" name="description" />
      </div>
      <div class="form-group">
        <label for="editImage">Image File:</label>
        <input type="file" id="editImage" name="image" accept="image/*" />
      </div>
      <button type="button" class="btn btn-success" onclick="saveProduct()">Save Product</button>
      <button type="button" class="btn" onclick="closeModal()">Cancel</button>
    </form>
  </div>
</div>

<script>
let DATA = {{ data_json | safe }};
let editingIndex = -1;
const grid = document.getElementById('grid');
const q = document.getElementById('q');
const count = document.getElementById('count');

function render(items) {
  grid.innerHTML = '';
  items.forEach((it, index) => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <img src="${it.thumb || ''}" alt="${it.article || it.name || ''}" />
      <h3>${it.article || it.name || 'No Article'}</h3>
      <div class="meta">
        <strong>Colour:</strong> <span class="editable" contenteditable="true" data-field="colour" data-index="${index}">${it.colour || 'Not specified'}</span><br/>
        <strong>Size:</strong> <span class="editable" contenteditable="true" data-field="size" data-index="${index}">${it.size || 'Not specified'}</span><br/>
        <strong>Pair:</strong> <span class="editable" contenteditable="true" data-field="pair" data-index="${index}">${it.pair || 'Not specified'}</span><br/>
        ${it.code ? `<strong>Code:</strong> ${it.code}<br/>` : ''}
      </div>
      <p>${(it.description||'').slice(0,200)}</p>
      <div class="meta">Matched: <span class="${it.matched?'matched':''}">${it.matched?('Yes ('+(it.score||'')+')'):'No'}</span></div>
      <div style="margin-top: 10px;">
        <button class="btn edit-btn" onclick="editProduct(${index})">Edit</button>
        <button class="btn btn-danger" onclick="deleteProduct(${index})">Delete</button>
      </div>
    `;
    grid.appendChild(div);
  });
  count.textContent = `${items.length} items`;
  
  // Add event listeners for inline editing
  document.querySelectorAll('.editable').forEach(element => {
    element.addEventListener('blur', function() {
      const field = this.dataset.field;
      const index = parseInt(this.dataset.index);
      const value = this.textContent.trim();
      DATA[index][field] = value === 'Not specified' ? null : value;
      saveToLocalStorage();
    });
  });
}

function f() {
  const term = q.value.toLowerCase();
  const items = DATA.filter(it => (
    (it.article||it.name||'').toLowerCase().includes(term) ||
    (it.colour||'').toLowerCase().includes(term) ||
    (it.size||'').toLowerCase().includes(term) ||
    (it.pair||'').toLowerCase().includes(term) ||
    (it.description||'').toLowerCase().includes(term) ||
    (it.code||'').toLowerCase().includes(term)
  ));
  render(items);
}

function showAddModal() {
  editingIndex = -1;
  document.getElementById('modalTitle').textContent = 'Add New Product';
  document.getElementById('productForm').reset();
  document.getElementById('productModal').style.display = 'block';
}

function editProduct(index) {
  editingIndex = index;
  const product = DATA[index];
  document.getElementById('modalTitle').textContent = 'Edit Product';
  document.getElementById('editArticle').value = product.article || '';
  document.getElementById('editColour').value = product.colour || '';
  document.getElementById('editSize').value = product.size || '';
  document.getElementById('editPair').value = product.pair || '';
  document.getElementById('editDescription').value = product.description || '';
  document.getElementById('productModal').style.display = 'block';
}

function saveProduct() {
  const form = document.getElementById('productForm');
  const formData = new FormData(form);
  
  const product = {
    article: formData.get('article') || null,
    colour: formData.get('colour') || null,
    size: formData.get('size') || null,
    pair: formData.get('pair') || null,
    description: formData.get('description') || null,
    image: formData.get('image') ? formData.get('image').name : null,
    matched: false,
    score: null
  };
  
  if (editingIndex === -1) {
    // Add new product
    DATA.push(product);
  } else {
    // Update existing product
    DATA[editingIndex] = { ...DATA[editingIndex], ...product };
  }
  
  saveToLocalStorage();
  render(DATA);
  closeModal();
}

function deleteProduct(index) {
  if (confirm('Are you sure you want to delete this product?')) {
    DATA.splice(index, 1);
    saveToLocalStorage();
    render(DATA);
  }
}

function closeModal() {
  document.getElementById('productModal').style.display = 'none';
}

function exportData() {
  const dataStr = JSON.stringify(DATA, null, 2);
  const dataBlob = new Blob([dataStr], {type: 'application/json'});
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'catalog_data.json';
  link.click();
}

function importData() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = function(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          DATA = JSON.parse(e.target.result);
          saveToLocalStorage();
          render(DATA);
          alert('Data imported successfully!');
        } catch (error) {
          alert('Error importing data: ' + error.message);
        }
      };
      reader.readAsText(file);
    }
  };
  input.click();
}

function saveToLocalStorage() {
  localStorage.setItem('catalogData', JSON.stringify(DATA));
}

function loadFromLocalStorage() {
  const saved = localStorage.getItem('catalogData');
  if (saved) {
    try {
      DATA = JSON.parse(saved);
    } catch (error) {
      console.error('Error loading saved data:', error);
    }
  }
}

// Load saved data on page load
loadFromLocalStorage();
render(DATA);
</script>
</body>
</html>
"""


def write_csv(items: List[Dict], path: str) -> None:
	if not items:
		open(path, 'w', newline='', encoding='utf-8').close()
		return
	fieldnames = sorted({k for it in items for k in it.keys()})
	with open(path, 'w', newline='', encoding='utf-8') as f:
		w = csv.DictWriter(f, fieldnames=fieldnames)
		w.writeheader()
		for it in items:
			w.writerow(it)


def write_html(items: List[Dict], path: str) -> None:
	import json
	payload = [{k: v for k, v in it.items() if k != 'image_path'} for it in items]
	t = Template(_HTML)
	html = t.render(data_json=json.dumps(payload))
	with open(path, 'w', encoding='utf-8') as f:
		f.write(html)


