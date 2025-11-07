import os
import sys
from pathlib import Path

# Configurar codificaciÃ³n para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("Verificando dependencias...")
try:
    from PIL import Image
    import easyocr
except ImportError:
    print("Instalando dependencias necesarias (esto puede tomar unos minutos)...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pillow', 'easyocr'])
    from PIL import Image
    import easyocr

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
    
    print(f"\nSe encontraron {len(image_files)} imagen(es)")
    print("Inicializando lector OCR (esto puede tomar un momento la primera vez)...")
    
    # Inicializar el lector de EasyOCR para espaÃ±ol (verbose=False para evitar errores de encoding)
    reader = easyocr.Reader(['es'], gpu=False, verbose=False)
    
    print("\nProcesando imagenes...\n")
    
    # Abrir el archivo de salida
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, image_file in enumerate(image_files, 1):
            image_path = os.path.join(folder_path, image_file)
            print(f"Procesando {idx}/{len(image_files)}: {image_file}")
            
            try:
                # Leer texto de la imagen con EasyOCR
                result = reader.readtext(image_path)
                
                # Extraer solo el texto de los resultados
                text_lines = [detection[1] for detection in result]
                text = '\n'.join(text_lines)
                
                # Escribir en el archivo
                f.write(f"{'='*80}\n")
                f.write(f"Imagen: {image_file}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
                f.write(f"\n\n")
                
                print(f"  -> Texto extraido exitosamente ({len(text_lines)} lineas)\n")
                
            except Exception as e:
                print(f"  -> Error procesando {image_file}: {str(e)}\n")
                f.write(f"Error procesando {image_file}: {str(e)}\n\n")
    
    print(f"===================================")
    print(f"Proceso completado exitosamente!")
    print(f"Texto guardado en: {output_path}")
    print(f"===================================")

if __name__ == "__main__":
    extract_text_from_images(image_folder, output_file)
