# Guía de Instalación - Descargador de Audio o Video

## 📋 Requisitos Previos

### 1. Python 3.8 o superior
- Descarga Python desde: https://www.python.org/downloads/
- **IMPORTANTE**: Marca la casilla "Add Python to PATH" durante la instalación

### 2. yt-dlp (Descargador de videos)
- yt-dlp es la herramienta principal para descargar videos de YouTube, TikTok, Facebook, etc.

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar o descargar el proyecto
```bash
# Si tienes Git instalado:
git clone [URL_DEL_REPOSITORIO]

# O simplemente descarga y extrae el archivo ZIP
```

### Paso 2: Navegar a la carpeta del proyecto
```bash
cd DescargarMultimediaProyecto
```

### Paso 3: Instalar yt-dlp
```bash
pip install yt-dlp
```

### Paso 4: Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

### Paso 5: Ejecutar la aplicación
```bash
python app.py
```

### Paso 6: Abrir en el navegador
- Ve a: `http://localhost:5000`
- ¡Listo para usar!

## 🔧 Solución de Problemas

### Error: "yt-dlp no se reconoce como comando"
```bash
# Reinstalar yt-dlp
pip uninstall yt-dlp
pip install yt-dlp

# O instalar con pip3 si usas Python 3
pip3 install yt-dlp
```

### Error: "Flask no se encuentra"
```bash
# Reinstalar Flask
pip install Flask

# O instalar todas las dependencias
pip install -r requirements.txt
```

### Error: "Python no se reconoce"
- Asegúrate de que Python esté en el PATH del sistema
- Reinicia la terminal/consola después de instalar Python
- Prueba con `python3` en lugar de `python`

### Error: "Puerto 5000 en uso"
```bash
# Cambiar puerto en app.py (última línea):
app.run(debug=True, port=5001)  # Usar puerto 5001
```

## 📱 Plataformas Soportadas

### Videos:
- ✅ YouTube
- ✅ TikTok
- ✅ Facebook
- ✅ Instagram
- ✅ Twitter/X
- ✅ Vimeo
- ✅ Dailymotion
- ✅ Twitch
- ✅ Y muchas más...

### Formatos:
- **Audio**: MP3, M4A, AAC, OGG, WAV
- **Video**: MP4, WebM, MKV, AVI, MOV

## 🎯 Uso Rápido

1. **Abrir aplicación**: `http://localhost:5000`
2. **Pegar URL**: Cualquier URL de video
3. **Elegir tipo**: Audio (MP3) o Video (MP4)
4. **Descargar**: El navegador preguntará dónde guardar

## 🛠️ Configuración Avanzada

### Cambiar puerto:
```python
# En app.py, última línea:
app.run(debug=True, port=8080)  # Cambiar 5000 por el puerto que quieras
```

### Cambiar usuario por defecto:
```javascript
// En templates/index.html, línea ~258:
return 'TU_USUARIO';  // Cambiar 'USUARIO' por tu nombre de usuario
```

## 📞 Soporte

Si tienes problemas:
1. Verifica que Python esté instalado correctamente
2. Asegúrate de que yt-dlp esté instalado
3. Revisa que todas las dependencias estén instaladas
4. Verifica que el puerto 5000 esté libre

## 🔄 Actualización

Para actualizar las dependencias:
```bash
pip install --upgrade -r requirements.txt
pip install --upgrade yt-dlp
```

