import os
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Instalando dependencias necesarias...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pillow', 'pytesseract'])
    from PIL import Image
    import pytesseract

# Configuracion
image_folder = r"D:\Libro_Juan\Nueva carpeta"
output_file = r"D:\Libro_Juan\Nueva carpeta\texto_extraido.txt"

# Extensiones de imagen soportadas
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

def extract_text_from_images(folder_path, output_path):
    # Obtener todas las imagenes en la carpeta
    image_files = []
    for file in os.listdir(folder_path):
        if Path(file).suffix.lower() in image_extensions:
            image_files.append(file)
    
    # Ordenar los archivos por nombre
    image_files.sort(key=lambda x: int(Path(x).stem) if Path(x).stem.isdigit() else Path(x).stem)
    
    if not image_files:
        print(f"No se encontraron imagenes en {folder_path}")
        return
    
    print(f"Se encontraron {len(image_files)} imagen(es)")
    print("Procesando imagenes...")
    
    # Abrir el archivo de salida
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, image_file in enumerate(image_files, 1):
            image_path = os.path.join(folder_path, image_file)
            print(f"\nProcesando {idx}/{len(image_files)}: {image_file}")
            
            try:
                # Abrir la imagen
                img = Image.open(image_path)
                
                # Extraer texto con pytesseract (idioma espaÃ±ol)
                text = pytesseract.image_to_string(img, lang='spa')
                
                # Escribir en el archivo
                f.write(f"{'='*80}\n")
                f.write(f"Imagen: {image_file}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
                f.write(f"\n\n")
                
                print(f"Texto extraido exitosamente")
                
            except Exception as e:
                print(f"Error procesando {image_file}: {str(e)}")
                f.write(f"Error procesando {image_file}: {str(e)}\n\n")
    
    print(f"\nProceso completado. Texto guardado en: {output_path}")

if __name__ == "__main__":
    try:
        pytesseract.get_tesseract_version()
    except Exception as e:
        print("\nADVERTENCIA: Tesseract OCR no esta instalado o no se encuentra en el PATH")
        print("\nPara instalar Tesseract:")
        print("1. Descarga el instalador desde: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Instala Tesseract en tu sistema")
        print("3. Asegurate de que esta en el PATH o configura la ruta manualmente")
        
    extract_text_from_images(image_folder, output_file)
