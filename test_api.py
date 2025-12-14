import requests
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create sample PDF files for testing
def create_sample_pdf(filename, pages=3):
    """Create a sample PDF for testing"""
    if os.path.exists(filename):
        return
    
    c = canvas.Canvas(filename, pagesize=letter)
    for i in range(pages):
        c.drawString(50, 750, f"Sample PDF - Page {i+1}")
        c.drawString(50, 700, "This is a test document for API testing.")
        c.drawString(50, 650, f"Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        c.showPage()
    c.save()
    print(f"✓ Created {filename}")

# Create sample files
print("Creating sample PDF files...")
create_sample_pdf('document.pdf', 5)
create_sample_pdf('file1.pdf', 2)
create_sample_pdf('file2.pdf', 2)

print("\n" + "="*60)
print("Testing PDF Toolkit APIs")
print("="*60)

# Test 1: PDF to Text conversion
print("\n1. Testing PDF to Text Conversion...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/api/pdf-to-text', files=files)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 2: Rotate PDF
print("\n2. Testing Rotate PDF (90°)...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        data = {'rotation': '90'}
        response = requests.post('http://localhost:5000/api/rotate', files=files, data=data)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 3: Merge PDFs
print("\n3. Testing Merge PDFs...")
try:
    with open('file1.pdf', 'rb') as f1, open('file2.pdf', 'rb') as f2:
        files = [('files', f1), ('files', f2)]
        response = requests.post('http://localhost:5000/api/merge', files=files)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 4: Remove Pages
print("\n4. Testing Remove Pages (remove pages 1,3)...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        data = {'pages': '1,3'}
        response = requests.post('http://localhost:5000/api/remove-pages', files=files, data=data)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 5: Split PDF
print("\n5. Testing Split PDF (pages 2-4)...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        data = {'start_page': '2', 'end_page': '4'}
        response = requests.post('http://localhost:5000/api/split', files=files, data=data)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 6: Compress PDF
print("\n6. Testing Compress PDF...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/api/compress', files=files)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 7: Add Watermark
print("\n7. Testing Add Watermark...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        data = {'watermark': 'CONFIDENTIAL'}
        response = requests.post('http://localhost:5000/api/watermark', files=files, data=data)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 8: Add Page Numbers
print("\n8. Testing Add Page Numbers...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/api/add-page-numbers', files=files)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

# Test 9: Repair PDF
print("\n9. Testing Repair PDF...")
try:
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/api/repair-pdf', files=files)
        result = response.json()
        if result.get('success'):
            print(f"   ✓ Success: {result['message']}")
            print(f"   ✓ Download: {result['download_url']}")
        else:
            print(f"   ✗ Error: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

print("\n" + "="*60)
print("API Testing Complete!")
print("="*60)
print("\nGenerated files are in the 'outputs' folder.")
