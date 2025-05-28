document.addEventListener('DOMContentLoaded', function () {
  const editor = document.querySelector('.editor');
  const lineNumbers = document.querySelector('.line-numbers');
  const themeSwitch = document.getElementById('theme-switch');

  const logo = document.getElementById('logo');
  const body = document.body;

  // Line numbers
  function updateLineNumbers() {
    const lineCount = editor.value.split('\n').length;
    lineNumbers.innerHTML = Array.from(
      { length: lineCount },
      (_, i) => i + 1
    ).join('<br>');
  }

  if (editor) {
    editor.addEventListener('input', updateLineNumbers);
    editor.addEventListener('scroll', () => {
      lineNumbers.scrollTop = editor.scrollTop;
    });
  }

  // Theme switch
  themeSwitch.addEventListener('change', () => {
    if (themeSwitch.checked) {
      body.classList.add('dark-mode');
      editor.setOption('theme', 'dracula');
      logo.src = '/static/assets/logo-light.png';
    } else {
      body.classList.remove('dark-mode');
      editor.setOption('theme', 'default');
      logo.src = '/static/assets/logo-dark.png';
    }
  });

  // Tab key
  if (editor) {
    editor.addEventListener('keydown', function (event) {
      if (event.key === 'Tab') {
        event.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const spaces = '     ';
        this.value =
          this.value.substring(0, start) + spaces + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + spaces.length;
      }
    });

    updateLineNumbers();
  }
});

// Save functionality
const saveButton = document.querySelector('.save-button');

saveButton.addEventListener('click', () => {
  const code = editor.getValue();

  let fileName = document.getElementById('file-name').textContent.trim();

  if (!fileName.endsWith('.txt')) {
    fileName = fileName.split('.')[0] + '.txt';
  }

  const blob = new Blob([code], { type: 'text/plain' });

  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = fileName;
  document.body.appendChild(link);
  link.click();

  document.body.removeChild(link);
  URL.revokeObjectURL(link.href);
});

CodeMirror.defineMode('acclang', function (config, parserConfig) {
  var keywords = new Set([
    'eklabool',
    'adele',
    'adelete',
    'anda',
    'andamhie',
    'chika',
    'pak',
    'ganern',
    'ganern pak',
    'versa',
    'betsung',
    'ditech',
    'forda',
    'keri',
    'keri lang',
    'amaccana',
    'gogogo',
    'givenchy',
    'serve',
    'kween',
    'shimenet',
    'push',
    'korik',
    'eme',
    'len',
    'naur',
    'from',
    'to',
    'step',
  ]);
  var operators = /[+\-*/%=&|!<>]+/;
  var numbers = /^[0-9]+/;
  var blockSymbols = /[(){}\[\]]/;

  return {
    startState: function () {
      return { inComment: false, inString: false };
    },
    token: function (stream, state) {
      if (state.inComment) {
        if (stream.match(/.*?\^\//)) {
          state.inComment = false;
          return 'comment';
        }
        stream.skipToEnd();
        return 'comment';
      }
      if (stream.match(/^\/\^/)) {
        state.inComment = true;
        return 'comment';
      }

      if (state.inString) {
        if (stream.match(/.*?"/)) {
          state.inString = false;
          return 'string';
        }
        stream.next();
        return 'string';
      }
      if (stream.match(/^"/)) {
        state.inString = true;
        return 'string';
      }

      if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
        var word = stream.current();
        if (keywords.has(word)) return 'keyword';
        return 'variable';
      }

      if (stream.match(/[(){}\[\]]/)) {
        return 'block';
      }

      if (stream.match(/[+\-*/%=&|!<>]/)) {
        return 'operator';
      }

      if (stream.match(numbers)) {
        return 'number';
      }

      stream.next();
      return null;
    },
  };
});

var editor = CodeMirror.fromTextArea(document.getElementById('source-code'), {
  mode: 'acclang',
  lineNumbers: true,
  theme: 'default',
  indentUnit: 4,
  tabSize: 4,
  smartIndent: true,
  autoCloseBrackets: true,
  matchBrackets: true,
  gutters: ['CodeMirror-linenumbers'],
  extraKeys: {
    'Ctrl-Space': 'autocomplete',
    'Ctrl-Q': function (cm) {
      cm.foldCode(cm.getCursor());
    },
    Tab: function (cm) {
      if (cm.somethingSelected()) {
        cm.indentSelection('add');
      } else {
        cm.replaceSelection('    ', 'end');
      }
    },
    'Shift-Tab': function (cm) {
      cm.indentSelection('subtract');
    },
    'Ctrl-Z': function (cm) {
      cm.undo();
    },
    'Cmd-Z': function (cm) {
      cm.undo();
    },
    'Ctrl-Y': function (cm) {
      cm.redo();
    },
    'Cmd-Y': function (cm) {
      cm.redo();
    },
    'Ctrl-/': function (cm) {
      toggleComment(cm);
    },
    'Cmd-/': function (cm) {
      toggleComment(cm);
    },
  },
});

editor.on('keydown', function (cm, event) {
  if ((event.ctrlKey || event.metaKey) && event.key === 'z') {
    event.preventDefault();
    cm.undo();
  }
  if (
    (event.ctrlKey || event.metaKey) &&
    (event.key === 'y' || (event.shiftKey && event.key === 'z'))
  ) {
    event.preventDefault();
    cm.redo();
  }
});

CodeMirror.registerHelper('hint', 'acclang', function (editor) {
  var cur = editor.getCursor();
  var token = editor.getTokenAt(cur);
  var start = token.start;
  var end = token.end;
  var word = token.string;
  var keywords = [
    'eklabool',
    'adele',
    'adelete',
    'len',
    'anda',
    'andamhie',
    'chika',
    'pak',
    'ganern',
    'ganern pak',
    'versa',
    'betsung',
    'ditech',
    'forda',
    'keri',
    'keri lang',
    'amaccana',
    'gogogo',
    'givenchy',
    'serve',
    'kween',
    'shimenet',
    'push',
    'korik',
    'eme',
    'naur',
    'from',
    'to',
    'step',
  ];
  var list = keywords.filter(function (k) {
    return k.startsWith(word);
  });
  return {
    list: list,
    from: CodeMirror.Pos(cur.line, start),
    to: CodeMirror.Pos(cur.line, end),
  };
});

editor.on('beforeChange', function (cm, change) {
  if (change.origin !== 'setValue') {
    change.text = change.text.map((line) =>
      line.replace(/[""]/g, '"').replace(/['']/g, "'")
    );
  }
});

editor.on('inputRead', function (cm, event) {
  if (!cm.state.completionActive) {
    CodeMirror.commands.autocomplete(cm, null, { completeSingle: false });
  }
});

// Terminal and Socket Handling
let socket = null;
let term = null;
let terminalInitialized = false;
let inputBuffer = '';

function initializeTerminal() {
  if (!terminalInitialized) {
    term = new Terminal({
      cursorBlink: true,
      fontFamily: 'monospace',
      fontSize: 14,
      cols: 100,
    });

    term.open(document.getElementById('terminal'));
    terminalInitialized = true;

    term.onData((e) => {
      if (e === '\r') {
        term.write('\r\n');
        socket.emit('user_input', inputBuffer);
        inputBuffer = '';
      } else if (e === '\u007F') {
        if (inputBuffer.length > 0) {
          inputBuffer = inputBuffer.slice(0, -1);
          term.write('\b \b');
        }
      } else {
        inputBuffer += e;
        term.write(e);
      }
    });
  }

  // Reset the terminal when it's initialized or reused
  inputBuffer = '';
  if (term) {
    term.clear();
  }
}

function runLexer() {
  // Always reset the logs and token display
  document.getElementById('token-stream').innerHTML = '';
  document.getElementById('compiler-log').innerText = '';

  // Hide the terminal initially
  document.getElementById('terminal').style.display = 'none';

  // If socket doesn't exist yet, create it
  if (!socket) {
    socket = io();

    // Set up listeners for terminal output
    socket.on('output', (data) => {
      if (terminalInitialized && term) {
        term.write(data.replace(/\n/g, '\r\n'));
      }
    });

    // Set up the compile_result handler
    socket.on('compile_result', (data) => {
      const tb = document.getElementById('token-stream');
      tb.innerHTML = '';
      data.tokens.forEach((tok) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${tok[0]}</td><td>${tok[1]}</td>`;
        tb.appendChild(row);
      });

      const logEl = document.getElementById('compiler-log');
      logEl.innerText = data.log.trim() || 'No Errors';

      // Only initialize terminal if there are no errors
      if (!data.log.trim()) {
        document.getElementById('terminal').style.display = 'block';
        initializeTerminal();
      }
    });
  }

  const source = editor.getValue();
  socket.emit('compile_and_run', { source_code: source });
}

function loadFile(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      editor.setValue(e.target.result, { historyPreserve: true });
      document.getElementById('file-name').textContent = file.name;
    };
    reader.readAsText(file);
  }
}

document.getElementById('theme-switch').addEventListener('change', function () {
  if (this.checked) {
    document.body.classList.add('dark-mode');
    editor.setOption('theme', 'dracula');
    document.getElementById('logo').src = '/static/assets/logo-light.png';
    style.innerHTML = `
      .cm-variable, .cm-def, .cm-identifier { color: white !important; }
    `;
  } else {
    document.body.classList.remove('dark-mode');
    editor.setOption('theme', 'default');
    document.getElementById('logo').src = '/static/assets/logo-dark.png';
    style.innerHTML = `
      .cm-variable, .cm-def, .cm-identifier { color: black !important; }
    `;
  }
});

const style = document.createElement('style');
document.head.appendChild(style);

function updateEditorTheme(isDarkMode) {
  if (isDarkMode) {
    style.innerHTML = `
      .cm-variable, .cm-def, .cm-identifier { color: white !important; }
    `;
  } else {
    style.innerHTML = `
      .cm-variable, .cm-def, .cm-identifier { color: black !important; }
    `;
  }
}

// Add some CSS to the page to handle terminal visibility
const terminalStyle = document.createElement('style');
terminalStyle.textContent = `
  #terminal {
    display: none;
    flex: 1;
    height: 200px;
    background: #000;
  }
`;
document.head.appendChild(terminalStyle);

// Define newCode to avoid the "newCode is not defined" error
const newCode = `/^ Welcome to A.C.C. Lang.^/
/^ Write your code below ^/

shimenet kween () {
    /^An A.C.C. Lang. program starts here^/
    serve("Hello, World!");
}`;

// Set the default value for the editor
if (editor.getValue().trim() === '') {
  editor.setValue(newCode);
}

// Add default code to the editor when the page loads
document.addEventListener('DOMContentLoaded', () => {
  const defaultCode = `/^ Welcome to A.C.C. Lang.^/
/^ Write your code below ^/

shimenet kween () {
    /^An A.C.C. Lang. program starts here^/
    serve("Hello, World!");
}`;

  if (editor.getValue().trim() === '') {
    editor.setValue(defaultCode);
  }
});

editor.setValue(newCode);
editor.clearHistory();

function toggleComment(cm) {
  if (cm.somethingSelected()) {
    const selections = cm.listSelections();
    cm.operation(() => {
      selections.forEach(({ anchor, head }) => {
        const from = cm.indexFromPos(anchor);
        const to = cm.indexFromPos(head);
        const start = Math.min(from, to);
        const end = Math.max(from, to);

        const selectedText = cm.getRange(
          cm.posFromIndex(start),
          cm.posFromIndex(end)
        );
        const isCommented =
          selectedText.startsWith('/^') && selectedText.endsWith('^/');

        if (isCommented) {
          const uncommentedText = selectedText.slice(2, -2).trim();
          cm.replaceRange(
            uncommentedText,
            cm.posFromIndex(start),
            cm.posFromIndex(end)
          );
        } else {
          cm.replaceRange(
            `/^ ${selectedText} ^/`,
            cm.posFromIndex(start),
            cm.posFromIndex(end)
          );
        }
      });
    });
  }
}
