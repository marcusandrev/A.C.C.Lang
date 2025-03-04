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

  editor.addEventListener('input', updateLineNumbers);
  editor.addEventListener('scroll', () => {
    lineNumbers.scrollTop = editor.scrollTop;
  });

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

  // Replace all curly quotes with straight quotes
  editor.addEventListener('input', function () {
    this.value = this.value.replace(/“|”/g, '"');
  });

  // Tab key
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
});

//Codemirror
CodeMirror.defineMode("acclang", function(config, parserConfig) {
  var keywords = new Set(["eklabool", "anda", "andamhie", "chika", "pak", "ganern", "ganern pak", "versa", "betsung", "ditech", "forda", "keri", "keri lang", "amaccana", "gogogo", "givenchy", "serve", "kween", "shimenet", "push", "korik", "eme", "naur", "from", "to", "step"]);
  var operators = /[+\-*/%=&|!<>]+/;
  var numbers = /^[0-9]+/;
  var blockSymbols = /[(){}\[\]]/;
  
  return {
    startState: function() {
      return { inComment: false, inString: false };
    },
    token: function(stream, state) {
      if (state.inComment) {
        if (stream.match(/.*?\^\//)) {
          state.inComment = false;
          return "comment";
        }
        stream.skipToEnd();
        return "comment";
      }
      if (stream.match(/^\/\^/)) {
        state.inComment = true;
        return "comment";
      }
      
      if (state.inString) {
        if (stream.match(/.*?"/)) {
          state.inString = false;
          return "string";
        }
        stream.next();
        return "string";
      }
      if (stream.match(/^"/)) {
        state.inString = true;
        return "string";
      }
      
      if (stream.match(/^[(){}\[\]]/)) {
        return "block";
      }
      if (stream.match(/^[+\-*/%=&|!<>]/)) {
        return "operator";
      }
      if (stream.match(/^[0-9]+/)) {
        return "number";
      }
      
      if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
        var word = stream.current();
        if (keywords.has(word)) return "keyword";
      }
      
      // Handle single-character symbols separately
      var ch = stream.next();
      if (blockSymbols.test(ch)) return "block";
      if (operators.test(ch)) return "operator";
      
      return null;
    }
  };
});

var editor = CodeMirror.fromTextArea(document.getElementById("source-code"), {
  mode: "acclang",
  lineNumbers: true,
  theme: "default",
  indentUnit: 4,
  tabSize: 4,
  smartIndent: true,
  autoCloseBrackets: true,
  extraKeys: { "Ctrl-Space": "autocomplete" }
});

CodeMirror.registerHelper("hint", "acclang", function(editor) {
  var cur = editor.getCursor();
  var token = editor.getTokenAt(cur);
  var start = token.start;
  var end = token.end;
  var word = token.string;
  var keywords = ["eklabool", "anda", "andamhie", "chika", "pak", "ganern", "ganern pak", "versa", "betsung", "ditech", "forda", "keri", "keri lang", "amaccana", "gogogo", "givenchy", "serve", "kween", "shimenet", "push", "korik", "eme", "naur", "from", "to", "step"];
  var list = keywords.filter(function(k) { return k.startsWith(word); });
  return { list: list, from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end) };
});

editor.on("inputRead", function(cm, event) {
  if (!cm.state.completionActive) {
    CodeMirror.commands.autocomplete(cm, null, { completeSingle: false });
  }
});

function runLexer() {
  console.log('Run button clicked');
  const sourceCode = editor.getValue();
  fetch('/lex', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `source_code=${encodeURIComponent(sourceCode)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('compiler-log').textContent = data.error_log || 'No Errors';
    })
    .catch((error) => console.error('Error:', error));
}

document.getElementById('theme-switch').addEventListener('change', function () {
  if (this.checked) {
    document.body.classList.add('dark-mode');
    editor.setOption('theme', 'dracula');
    document.getElementById('logo').src = '/static/assets/logo-light.png';
  } else {
    document.body.classList.remove('dark-mode');
    editor.setOption('theme', 'default');
    document.getElementById('logo').src = '/static/assets/logo-dark.png';
  }
});
