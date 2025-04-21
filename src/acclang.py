# acclang.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os, subprocess, threading

# your existing imports for Lexer, Parser, etc.
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser
from src.packages.parser.semantic_analyzer import SemanticAnalyzer
from src.packages.codegen.ast_generator import ASTGenerator
from src.packages.codegen.code_generation import CodeGenerator

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# global handle to the running process
_process = None
_process_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('compile_and_run')
def handle_compile_and_run(data):
    global _process
    source_code = data.get('source_code', '')

    # --- 1) Lex / Parse / Semantic / Codegen exactly as before ---
    lex = Lexer(source_code)
    lex.start()
    tokens = [tup[0] for tup in lex.token_stream]
    error_log = ""
    if lex.log:
        error_log = "Lexical Error/s\n\n" + str(lex.log)

    if not error_log:
        parser = Parser(source_code, tokens)
        parser.start()
        if parser.log:
            error_log = "Syntax Error/s\n\n" + parser.log

    if not error_log:
        analyzer = SemanticAnalyzer(lex.token_stream)
        analyzer.analyze()
        if analyzer.log:
            error_log = "Semantic Error/s\n\n" + analyzer.log

    # 2) Send back tokens & errors
    emit('compile_result', {
        'tokens': tokens,
        'log': error_log
    })

    # 3) If any error, bail out here
    if error_log:
        return

    # 4) Otherwise generate + write compiled.py
    ast = ASTGenerator(lex.token_stream).generate()
    target_code = CodeGenerator().generate(ast)
    out_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'Files', 'compiled', 'compiled.py'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(target_code)

    # 5) Spawn child process under Popen for interactive I/O
    with _process_lock:
        if _process and _process.poll() is None:
            try:
                _process.terminate()  # Terminate any currently running process
                _process.wait(timeout=1)  # Wait for it to finish
            except Exception as e:
                emit('output', f"\n[!] Error terminating previous process: {e}\n")

        _process = subprocess.Popen(
            ['python', '-u', out_path],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        socketio.start_background_task(stream_output, _process)
        emit('output', f"[+] Running program.\n")

def stream_output(proc):
    """Emit every character so prompts without newline show up immediately."""
    global _process
    try:
        while True:
            ch = proc.stdout.read(1)
            if not ch:
                break
            socketio.emit('output', ch)
    except Exception as e:
        socketio.emit('output', f"\n[!] Stream error: {e}\n")
    finally:
        proc.stdout.close()
        with _process_lock:
            if _process is proc:
                _process = None
        socketio.emit('output', "\n[+] Program finished.\n")

@socketio.on('user_input')
def handle_user_input(data):
    global _process
    with _process_lock:
        if _process and _process.poll() is None:
            try:
                _process.stdin.write(data + '\n')
                _process.stdin.flush()
            except Exception as e:
                emit('output', f"\n[!] Failed to send input: {e}\n")
        else:
            emit('output', "\n[!] No program is running.\n")

if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5006)