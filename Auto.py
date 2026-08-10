from github import Github

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Reemplaza 'tu_token_personal_aqui' con tu Personal Access Token de GitHub
TOKEN_GITHUB = "tu_token_personal_aqui"

# Nombre de tu repositorio tal cual aparece en GitHub (ej. "Edgaus/Web")
REPOSITORIO = "Edgaus/Web"

# Carpeta donde Zapier está guardando los borradores automáticos
CARPETA_BORRADORES = "_drafts"

# Carpeta oficial de tu página web estática donde se publica lo aceptado
CARPETA_PUBLICADOS = "_posts"
# ==========================================

def gestionar_borradores():
    # 1. Autenticación con GitHub
    g = Github(TOKEN_GITHUB)
    repo = g.get_repo(REPOSITORIO)

    print("Conectando con tu repositorio en GitHub...")

    try:
        # 2. Obtener la lista de archivos dentro de la carpeta de borradores
        archivos = repo.get_contents(CARPETA_BORRADORES)
    except Exception as e:
        print(f"No se pudo leer la carpeta {CARPETA_BORRADORES} o está vacía: {e}")
        return

    # Filtramos solo los archivos que terminan en .md
    borradores = [f for f in archivos if f.name.endswith(".md")]

    if not borradores:
        print("\nNo hay nuevos borradores pendientes en el baúl.")
        return

    print(f"\n¡Se encontraron {len(borradores)} borrador(es) en el baúl!\n")
    print("-" * 50)

    for archivo in borradores:
        print(f"Título / Archivo: {archivo.name}")
        
        # Pregunta interactiva para aceptar o rechazar
        respuesta = input("¿Deseas aceptar y publicar este artículo? (Y/N): ").strip().upper()

        if respuesta == 'Y':
            # Leer el contenido del borrador
            contenido_archivo = archivo.decoded_content
            
            # Definir la nueva ruta en la carpeta de publicados
            nueva_ruta = f"{CARPETA_PUBLICADOS}/{archivo.name}"

            # 3. Crear el archivo en la carpeta oficial _posts
            repo.create_file(
                path=nueva_ruta,
                message=f"Aprobación de artículo: {archivo.name}",
                content=contenido_archivo,
                branch="main"
            )

            # 4. Eliminar el archivo original de la carpeta _drafts para vaciar el baúl
            repo.delete_file(
                path=archivo.path,
                message=f"Moviendo borrador a publicados: {archivo.name}",
                sha=archivo.sha,
                branch="main"
            )

            print(f"¡Éxito! '{archivo.name}' ha sido aprobado, movido a _posts y se publicará en tu web.")
        else:
            print("Artículo rechazado o ignorado. Se mantiene en el baúl.")
        
        print("-" * 50)

if __name__ == "__main__":
    gestionar_borradores()