from cx_Freeze import setup, Executable

# Opções de compilação
build_exe_options = {
    "packages": ["sys", "PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui"],
    "include_files": ["logo.ico"],  
}

setup(
    name="Ferramenta de Corte de Chapas",
    version="0.1",
    description="Aplicativo para cálculo de corte de chapas",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",  
            base="Win32GUI",
            icon="logo.ico", 
            target_name="CorteChapasApp.exe"  
        )
    ]
)

# Para gerar o executável
# python setup.py build
