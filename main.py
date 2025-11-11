#!/usr/bin/env python3
"""
ROM Renamer para Nintendo 3DS - Versión Flet GUI
Renombra automáticamente ROMs a formato .cci y extrae archivos comprimidos
"""

import os
import shutil
import zipfile
import py7zr
import rarfile
import threading # Necesario para evitar que la UI se congele
from pathlib import Path
from typing import List, Callable, Optional

# Importaciones de Flet
import flet as ft

# --- Lógica de Negocio (Modificada) ---

# Extensiones de ROMs de Nintendo 3DS
ROM_EXTENSIONS = {'.3ds', '.cia', '.3dsx', '.app'}

# Extensiones de archivos comprimidos
COMPRESSED_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}

# Extensión objetivo
TARGET_EXTENSION = '.cci'


class ROMRenamer:
    """
    Clase modificada para funcionar con una GUI.
    Elimina 'rich' y usa un 'update_callback' para enviar logs a la UI.
    """
    def __init__(self, directory: str, update_callback: Callable[[str], None]):
        self.directory = Path(directory).resolve()
        self.backup_dir = self.directory / 'archivos_comprimidos_backup'
        self.stats = {
            'renamed': 0,
            'extracted': 0,
            'moved': 0,
            'errors': 0
        }
        # Este callback es la función que actualiza la UI (el ListView)
        self.log = update_callback 
    
    def create_backup_dir(self):
        """Crea el directorio de respaldo si no existe"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            self.log(f"✓ Carpeta de respaldo creada: {self.backup_dir.name}")
    
    def find_files(self) -> tuple[List[Path], List[Path]]:
        """Encuentra archivos ROM y comprimidos en el directorio"""
        rom_files = []
        compressed_files = []
        
        for file in self.directory.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                if ext in ROM_EXTENSIONS:
                    rom_files.append(file)
                elif ext in COMPRESSED_EXTENSIONS:
                    compressed_files.append(file)
        
        return rom_files, compressed_files
    
    def rename_rom(self, file: Path) -> bool:
        """Renombra un archivo ROM a .cci"""
        try:
            new_name = file.with_suffix(TARGET_EXTENSION)
            if new_name.exists():
                self.log(f"⚠ Ya existe: {new_name.name}")
                return False
            
            file.rename(new_name)
            self.log(f"✓ Renombrado: {file.name} → {new_name.name}")
            self.stats['renamed'] += 1
            return True
        except Exception as e:
            self.log(f"✗ Error al renombrar {file.name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def extract_archive(self, archive: Path) -> List[Path]:
        """Extrae un archivo comprimido y retorna las ROMs encontradas"""
        extract_dir = self.directory / f"_temp_extract_{archive.stem}"
        rom_files = []
        
        try:
            extract_dir.mkdir(exist_ok=True)
            
            ext = archive.suffix.lower()
            if ext == '.zip':
                with zipfile.ZipFile(archive, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            elif ext == '.7z':
                with py7zr.SevenZipFile(archive, 'r') as sz_ref:
                    sz_ref.extractall(extract_dir)
            elif ext == '.rar':
                with rarfile.RarFile(archive, 'r') as rar_ref:
                    rar_ref.extractall(extract_dir)
            else:
                self.log(f"⚠ Formato no soportado: {ext}")
                return rom_files
            
            self.log(f"✓ Extraído: {archive.name}")
            self.stats['extracted'] += 1
            
            # Buscar ROMs en el directorio extraído (recursivamente)
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in ROM_EXTENSIONS:
                        dest = self.directory / file_path.name
                        counter = 1
                        while dest.exists():
                            dest = self.directory / f"{file_path.stem}_{counter}{file_path.suffix}"
                            counter += 1
                        
                        shutil.move(str(file_path), str(dest))
                        rom_files.append(dest)
                        self.log(f"→ ROM encontrada: {dest.name}")
            
            shutil.rmtree(extract_dir, ignore_errors=True)
            
        except Exception as e:
            self.log(f"✗ Error al extraer {archive.name}: {e}")
            self.stats['errors'] += 1
            if extract_dir.exists():
                shutil.rmtree(extract_dir, ignore_errors=True)
        
        return rom_files
    
    def move_to_backup(self, file: Path) -> bool:
        """Mueve un archivo a la carpeta de respaldo"""
        try:
            dest = self.backup_dir / file.name
            counter = 1
            while dest.exists():
                dest = self.backup_dir / f"{file.stem}_{counter}{file.suffix}"
                counter += 1
            
            shutil.move(str(file), str(dest))
            self.log(f"→ Movido a respaldo: {file.name}")
            self.stats['moved'] += 1
            return True
        except Exception as e:
            self.log(f"✗ Error al mover {file.name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def show_stats(self):
        """Muestra las estadísticas finales en la GUI"""
        self.log("\n--- Resumen de Operaciones ---")
        self.log(f"ROMs renombradas:   {self.stats['renamed']}")
        self.log(f"Archivos extraídos: {self.stats['extracted']}")
        self.log(f"Archivos respaldados: {self.stats['moved']}")
        self.log(f"Errores:            {self.stats['errors']}")
        self.log("---------------------------------")
    
    def run(self):
        """Ejecuta el proceso completo (sin 'rich' ni confirmación)"""
        
        self.log(f"Directorio de trabajo: {self.directory}\n")
        self.log("Escaneando directorio...")
        
        rom_files, compressed_files = self.find_files()
        
        self.log(f"\n→ ROMs encontradas: {len(rom_files)}")
        self.log(f"→ Archivos comprimidos: {len(compressed_files)}\n")
        
        if not rom_files and not compressed_files:
            self.log("No se encontraron archivos para procesar.")
            return

        # Eliminamos la confirmación, el botón "Iniciar" de la GUI es la confirmación.
        self.log("Iniciando proceso...\n")
        
        if compressed_files:
            self.create_backup_dir()
        
        if compressed_files:
            self.log("\nPaso 1/3: Extrayendo archivos comprimidos\n")
            extracted_roms = []
            for archive in compressed_files:
                roms = self.extract_archive(archive)
                extracted_roms.extend(roms)
            
            rom_files.extend(extracted_roms)
        
        if rom_files:
            self.log("\nPaso 2/3: Renombrando ROMs a .cci\n")
            for rom in rom_files:
                if rom.exists() and rom.suffix.lower() != TARGET_EXTENSION:
                    self.rename_rom(rom)
        
        if compressed_files:
            self.log("\nPaso 3/3: Moviendo archivos comprimidos a respaldo\n")
            for archive in compressed_files:
                if archive.exists():
                    self.move_to_backup(archive)
        
        self.show_stats()
        self.log("\n✓ Proceso completado exitosamente!\n")


# --- Aplicación Flet ---

def main(page: ft.Page):
    
    page.title = "ROM Renamer (3DS)"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 700
    page.window_height = 600

    # --- Funciones de la UI ---

    def log_to_gui(message: str):
        """Callback que recibe logs y los añade al ListView"""
        output_log.controls.append(ft.Text(message, selectable=True))
        output_log.update() # Actualiza el ListView

    def run_renamer_logic(directory: str):
        """Función que se ejecutará en un hilo separado"""
        try:
            # Crea la instancia del renamer y le pasa el callback
            renamer = ROMRenamer(directory, log_to_gui)
            renamer.run()
        except Exception as e:
            log_to_gui(f"Error crítico en el hilo: {e}")
        finally:
            # Al terminar, reactiva los botones y oculta el progreso
            progress_ring.visible = False
            start_button.disabled = False
            select_dir_button.disabled = False
            page.update() # Actualiza la página para reflejar los cambios

    def start_processing(e):
        """Inicia el proceso en un hilo cuando se presiona el botón"""
        if selected_dir_text.value:
            # Desactiva botones y muestra el progreso
            progress_ring.visible = True
            start_button.disabled = True
            select_dir_button.disabled = True
            output_log.controls.clear() # Limpia el log anterior
            log_to_gui("Iniciando...")
            page.update()
            
            # Inicia el hilo
            threading.Thread(
                target=run_renamer_logic,
                args=(selected_dir_text.value,),
                daemon=True # El hilo se cierra si la app se cierra
            ).start()
        else:
            log_to_gui("Error: Ninguna carpeta seleccionada.")

    def on_directory_selected(e: ft.FilePickerResultEvent):
        """Callback del FilePicker cuando se selecciona un directorio"""
        if e.path:
            selected_dir_text.value = e.path
            start_button.disabled = False # Activa el botón de inicio
        else:
            selected_dir_text.value = ""
            start_button.disabled = True
        page.update()

    # --- Controles de la UI ---

    # 1. File Picker (oculto en el overlay)
    file_picker = ft.FilePicker(on_result=on_directory_selected)
    page.overlay.append(file_picker)

    # 2. Texto para mostrar la carpeta seleccionada
    selected_dir_text = ft.TextField(
        label="Carpeta seleccionada",
        read_only=True,
        expand=True
    )

    # 3. Botón para abrir el selector de carpetas
    select_dir_button = ft.ElevatedButton(
        "Seleccionar Carpeta",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.get_directory_path(
            dialog_title="Selecciona la carpeta con tus ROMs"
        )
    )

    # 4. Botón para iniciar el proceso
    start_button = ft.ElevatedButton(
        "Iniciar Proceso",
        icon=ft.Icons.PLAY_ARROW,
        on_click=start_processing,
        disabled=True, # Deshabilitado hasta que se elija carpeta
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700
    )

    # 5. Indicador de progreso
    progress_ring = ft.ProgressRing(visible=False)

    # 6. Log de salida (el reemplazo de la consola)
    output_log = ft.ListView(
        expand=True,
        spacing=5,
        auto_scroll=True,
        divider_thickness=0.5
    )
    
    output_container = ft.Container(
        content=output_log,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=ft.border_radius.all(5),
        padding=10,
        expand=True
    )

    # --- Layout de la Aplicación ---
    
    page.add(
        ft.Text("ROM Renamer para 3DS", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Convierte ROMs a formato .cci y extrae archivos comprimidos."),
        
        ft.Row(
            [selected_dir_text, select_dir_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        
        ft.Row(
            [start_button, progress_ring],
            alignment=ft.MainAxisAlignment.START
        ),
        
        ft.Divider(),
        ft.Text("Registro de actividad:", weight=ft.FontWeight.BOLD),
        output_container # El ListView va dentro del contenedor expandido
    )

# Punto de entrada para Flet
if __name__ == "__main__":
    ft.app(target=main)
