from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os
import re
import tempfile
import shutil
from pathlib import Path

app = Flask(__name__)

def sanitize_filename(filename):
    """Sanitiza el nombre del archivo removiendo caracteres no válidos"""
    # Remover caracteres no permitidos en nombres de archivo
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limitar longitud
    filename = filename[:100]
    return filename

def create_directory_if_not_exists(path):
    """Crea el directorio si no existe"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creando directorio: {e}")
        return False

def get_video_title(url):
    """Obtiene el título del video usando yt-dlp"""
    try:
        result = subprocess.run([
            'yt-dlp', '--get-title', '--no-warnings', url
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            title = result.stdout.strip()
            return sanitize_filename(title) if title else "audio_descargado"
        else:
            return "audio_descargado"
    except Exception:
        return "audio_descargado"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/check_path', methods=['POST'])
def check_path():
    """API para verificar si una ruta existe o puede ser creada"""
    data = request.get_json()
    path = data.get('path', '')
    
    if not path:
        return jsonify({'valid': False, 'message': 'Ruta no especificada'})
    
    try:
        # Verificar si la ruta existe
        if os.path.exists(path):
            if os.path.isdir(path):
                return jsonify({'valid': True, 'message': 'Carpeta encontrada'})
            else:
                return jsonify({'valid': False, 'message': 'La ruta especificada es un archivo, no una carpeta'})
        else:
            # Intentar crear la carpeta
            if create_directory_if_not_exists(path):
                return jsonify({'valid': True, 'message': 'Carpeta creada exitosamente'})
            else:
                return jsonify({'valid': False, 'message': 'No se pudo crear la carpeta. Verifique los permisos.'})
    except Exception as e:
        return jsonify({'valid': False, 'message': f'Error: {str(e)}'})

@app.route('/api/list_folders', methods=['POST'])
def list_folders():
    """API para listar carpetas en un directorio"""
    data = request.get_json()
    path = data.get('path', '')
    
    if not path:
        return jsonify({'success': False, 'message': 'Ruta no especificada'})
    
    try:
        # Verificar si la ruta existe y es un directorio
        if not os.path.exists(path):
            return jsonify({'success': False, 'message': 'La ruta no existe'})
        
        if not os.path.isdir(path):
            return jsonify({'success': False, 'message': 'La ruta especificada no es un directorio'})
        
        # Listar solo directorios (carpetas)
        folders = []
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                # Solo incluir directorios, no archivos
                if os.path.isdir(item_path):
                    # Filtrar carpetas del sistema y ocultas
                    if not item.startswith('.') and not item.startswith('$'):
                        folders.append(item)
            
            # Ordenar alfabéticamente
            folders.sort()
            
            return jsonify({
                'success': True, 
                'folders': folders,
                'path': path
            })
            
        except PermissionError:
            return jsonify({'success': False, 'message': 'Sin permisos para acceder a esta carpeta'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al leer el directorio: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/download', methods=['POST'])
def download():
    try:
        # Obtener datos del formulario
        url = request.form.get('url', '').strip()
        custom_filename = request.form.get('filename', '').strip()
        download_type = request.form.get('download_type', 'audio').strip()
        
        # Validaciones básicas
        if not url:
            return 'Por favor, ingrese una URL válida', 400
        
        # Obtener título del video si no se especifica nombre personalizado
        if custom_filename:
            filename = sanitize_filename(custom_filename)
        else:
            filename = get_video_title(url)
        
        # Crear ruta temporal para la descarga
        temp_dir = tempfile.mkdtemp()
        temp_output_path = os.path.join(temp_dir, f'{filename}.%(ext)s')
        
        try:
            if download_type == 'audio':
                # Comando para descargar solo audio (compatible con TikTok, Facebook, etc.)
                cmd = [
                    'yt-dlp',
                    '-x',  # Extraer audio
                    '--audio-format', 'mp3',
                    '--audio-quality', '192K',  # Calidad de audio
                    '--extractor-args', 'tiktok:webpage_url_basename=t',  # Para TikTok
                    '-o', temp_output_path,
                    '--no-playlist',  # Solo descargar el video especificado
                    url
                ]
                expected_extension = '.mp3'
                
            else:  # download_type == 'video'
                # Comando para descargar video completo (compatible con múltiples plataformas)
                cmd = [
                    'yt-dlp',
                    '-f', 'best',  # Mejor calidad disponible
                    '--format', 'best[ext=mp4]/best',  # Preferir MP4, sino el mejor disponible
                    '--extractor-args', 'tiktok:webpage_url_basename=t',  # Para TikTok
                    '-o', temp_output_path,
                    '--no-playlist',  # Solo descargar el video especificado
                    url
                ]
                expected_extension = '.mp4'
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # Más tiempo para videos
            
            if result.returncode != 0:
                return f'Error al descargar el {download_type}: {result.stderr}', 500
            
            # Buscar el archivo descargado en el directorio temporal
            downloaded_files = os.listdir(temp_dir)
            
            # Buscar archivos con las extensiones esperadas
            video_extensions = ['.mp4', '.webm', '.mkv', '.avi', '.mov']
            audio_extensions = ['.mp3', '.m4a', '.aac', '.ogg', '.wav']
            
            if download_type == 'audio':
                target_extensions = audio_extensions
            else:
                target_extensions = video_extensions
            
            found_file = None
            actual_extension = None
            
            for file in downloaded_files:
                for ext in target_extensions:
                    if file.endswith(ext):
                        found_file = file
                        actual_extension = ext
                        break
                if found_file:
                    break
            
            if not found_file:
                return f'No se pudo encontrar el archivo {download_type} descargado. Archivos encontrados: {downloaded_files}', 500
            
            temp_file_path = os.path.join(temp_dir, found_file)
            
            # Devolver el archivo directamente para descarga sin guardarlo en el servidor
            return send_file(temp_file_path, as_attachment=True, download_name=f'{filename}{actual_extension}')
            
        finally:
            # Limpiar archivos temporales
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    except subprocess.TimeoutExpired:
        return f'La descarga de {download_type} tardó demasiado tiempo. Por favor, inténtelo de nuevo.', 500
    except Exception as e:
        return f'Error inesperado: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)