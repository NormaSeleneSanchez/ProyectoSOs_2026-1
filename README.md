# ProyectoSOs_2026-1
Desarrollo de un monitor básico del sistema Implementa una herramienta sencilla que muestre información relevante del SO: uso de CPU, memoria, procesos, disco, red, etc.

# Equipo 05:

Jiménez Sánchez Emma Alicia

Salazar Gonzalez Pedro Yamil

Sánchez Cruz Norma Selene

Suárez Ortiz Joshua Daniel

# Requisitos previos:

Python 3.x

# Tecnologías
- Python 3.x
- `psutil` — acceso a métricas del sistema
- `textual` — TUI basada en Rich
- `virtualenv` / `venv`

# Como ejecutar nuestro proyecto:

 **Clonar el repositorio:**
```bash
git clone https://github.com/NormaSeleneSanchez/ProyectoSOs_2026-1.git
```

**Navegar en la carpeta del proyecto:**
```bash
cd ProyectoSOs_2026-1/Proyecto
```

**Crear un entorno virtual** 
```bash
python -m venv myenv
```

**Activar el entorno virtual** 

*en Windows* 
```bash
myenv\Scripts\activate
```

*en macOS y Linux* 
```bash
source myenv/bin/activate
```

**Instalar**
```bash
pip install textual psutil
```

**Ejecutar**
```bash
python main.py
```
