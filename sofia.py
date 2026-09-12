import os
import sys
import argparse
import subprocess
import requests
import psutil
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
MODELO = "qwen2.5-coder:7b"
MAX_RAM_PERCENT = 80.0

def asegurar_entorno():
    """Checks if Ollama is running and the model is downloaded; provisions them if missing."""
    print("🔍 Checking Ollama status and installed models...")
    
    # 1. Check if Ollama responds on localhost
    try:
        requests.get("http://localhost:11434", timeout=2)
    except requests.exceptions.ConnectionError:
        print("⚠️ Ollama is not active. Attempting to launch Ollama service...")
        try:
            subprocess.Popen(["ollama", "serve"], shell=True)
            time.sleep(3)  # Wait for service to initialize
        except Exception as e:
            print(f"❌ Failed to start Ollama automatically: {e}")
            print("Please install or launch Ollama manually from https://ollama.com")
            sys.exit(1)

    # 2. Check if the specified model is installed
    try:
        res = requests.get(OLLAMA_TAGS_URL, timeout=5).json()
        modelos_instalados = [m.get('name', '') for m in res.get('models', [])]
        
        # Match model by exact name or tag prefix
        modelo_presente = any(MODELO in m for m in modelos_instalados)
        
        if not modelo_presente:
            print(f"📦 Model '{MODELO}' was not found locally.")
            print(f"📥 Pulling '{MODELO}' via Ollama (this may take a few minutes)...")
            subprocess.run(["ollama", "pull", MODELO], check=True, shell=True)
            print("✅ Model downloaded successfully.")
    except Exception as e:
        print(f"⚠️ Could not verify model availability: {e}")

def verificar_recursos():
    """Validates available RAM before triggering model inference."""
    ram_actual = psutil.virtual_memory().percent
    if ram_actual > MAX_RAM_PERCENT:
        print(f"🛑 RAM limit reached ({ram_actual}%). Operation aborted to prevent system freeze.")
        return False
    return True

def consultar_llm(prompt):
    """Sends inference request to Ollama with system instruction enforcement."""
    if not verificar_recursos():
        sys.exit(1)
        
    system_instruction = (
        "You are SOFIA, a local AI harness for software engineering. "
        "Your task is to generate or modify source code following best practices. "
        "Return EXCLUSIVELY the executable code, without explanations or introductory text."
    )
    
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "system": system_instruction,
        "stream": False,
        "options": {"num_ctx": 4096}
    }
    
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=120)
        res.raise_for_status()
        return res.json().get('response', '')
    except requests.exceptions.ConnectionError:
        print("❌ Error: Unable to communicate with Ollama service.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during inference: {e}")
        sys.exit(1)

def analizar_flutter(raiz_proyecto):
    """Executes 'flutter analyze' on the project root to validate code syntax."""
    res = subprocess.run(
        ["flutter", "analyze"],
        cwd=raiz_proyecto,
        capture_output=True,
        text=True,
        shell=True
    )
    return res.returncode == 0, res.stdout

def resolver_ruta_proyecto(ruta_archivo):
    """Finds project root by searching upwards for pubspec.yaml or fallbacks to CWD."""
    dir_actual = os.path.dirname(os.path.abspath(ruta_archivo))
    while dir_actual != os.path.dirname(dir_actual):
        if os.path.exists(os.path.join(dir_actual, "pubspec.yaml")):
            return dir_actual
        dir_actual = os.path.dirname(dir_actual)
        
    return os.getcwd()

def ejecutar_arnes(instruccion, ruta_archivo):
    """Main execution loop: code generation, disk writing, and auto-correction."""
    asegurar_entorno()
    
    ruta_abs = os.path.abspath(ruta_archivo)
    raiz_proyecto = resolver_ruta_proyecto(ruta_abs)
    
    print(f"\n⚡ [SOFIA Harness] Project detected at: {raiz_proyecto}")
    print(f"📄 Target file: {ruta_abs}")
    
    codigo_actual = ""
    if os.path.exists(ruta_abs):
        with open(ruta_abs, "r", encoding="utf-8") as f:
            codigo_actual = f.read()

    prompt = (
        f"Instruction: {instruccion}\n\n"
        f"Current file contents:\n{codigo_actual}\n\n"
        "Return EXCLUSIVELY the updated executable code:"
    )

    for intento in range(1, 3):
        print(f"\n🔄 Generating code with {MODELO} (Attempt {intento}/2)...")
        codigo_generado = consultar_llm(prompt)
        
        codigo_limpio = codigo_generado.strip()
        if codigo_limpio.startswith("```"):
            lineas = codigo_limpio.splitlines()
            if lineas[0].startswith("```"):
                lineas = lineas[1:]
            if lineas and lineas[-1].startswith("```"):
                lineas = lineas[:-1]
            codigo_limpio = "\n".join(lineas).strip()

        os.makedirs(os.path.dirname(ruta_abs), exist_ok=True)
        with open(ruta_abs, "w", encoding="utf-8") as f:
            f.write(codigo_limpio)

        print("🔍 Validating syntax...")
        exito, errores = analizar_flutter(raiz_proyecto)

        if exito:
            print("✅ Code successfully applied and verified by SOFIA!")
            return

        print("⚠️ Syntax issues detected. Retrying correction loop...")
        errores_resumidos = "\n".join(errores.splitlines()[:8])
        prompt = (
            f"The previously generated code produced these syntax errors:\n{errores_resumidos}\n\n"
            f"Faulty code:\n{codigo_limpio}\n\n"
            "Fix all syntax errors and return EXCLUSIVELY the complete valid code:"
        )

    print("\n❌ SOFIA could not resolve all syntax errors after 2 attempts.")
    print("The file contains the latest generated output. Please review remaining errors manually.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SOFIA - Local LLM Harness for Software Engineering")
    parser.add_argument("-i", "--instruction", required=True, help="Instruction specifying the code generation task")
    parser.add_argument("-f", "--file", required=True, help="Path to the target file to create or modify")

    args = parser.parse_args()
    ejecutar_arnes(args.instruction, args.file)
